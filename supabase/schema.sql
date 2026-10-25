-- Retro Arcade — Supabase schema
-- Run this in the Supabase SQL editor (Dashboard → SQL → New query).

create table if not exists public.players (
  device_id  uuid primary key,
  tokens     integer not null default 0,
  last_daily date,
  created_at timestamptz not null default now()
);

create table if not exists public.orders (
  id           uuid primary key default gen_random_uuid(),
  device_id    uuid not null references public.players(device_id) on delete cascade,
  out_trade_no text unique not null,
  amount       numeric(10,2) not null,
  status       text not null default 'pending' check (status in ('pending','paid','closed')),
  qr_code      text,
  created_at   timestamptz not null default now(),
  paid_at      timestamptz
);

-- Daily grant: first contact of a new day adds 5 tokens (unused ones stack).
-- Returns the current balance.
create or replace function public.get_balance(p_device uuid)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare bal integer;
begin
  insert into players(device_id, tokens, last_daily)
  values (p_device, 5, current_date)
  on conflict (device_id) do update set
    tokens = players.tokens + case when players.last_daily is distinct from current_date then 5 else 0 end,
    last_daily = current_date;
  select tokens into bal from players where device_id = p_device;
  return bal;
end $$;

-- Spend tokens server-side. Returns the new balance, or -1 if not enough.
create or replace function public.spend_tokens(p_device uuid, p_cost integer)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare bal integer;
begin
  if p_cost <= 0 then
    return -1; -- never allow negative costs to credit tokens
  end if;
  insert into players(device_id, tokens, last_daily)
  values (p_device, 5, current_date)
  on conflict (device_id) do update set
    tokens = players.tokens + case when players.last_daily is distinct from current_date then 5 else 0 end,
    last_daily = current_date;
  update players set tokens = tokens - p_cost
    where device_id = p_device and tokens >= p_cost;
  if not found then
    return -1;
  end if;
  select tokens into bal from players where device_id = p_device;
  return bal;
end $$;

-- Credit 5 tokens to a device (used by the webhook function, service role only).
create or replace function public.credit_tokens(p_device uuid, p_amount integer)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare bal integer;
begin
  insert into players(device_id, tokens, last_daily)
  values (p_device, p_amount, current_date)
  on conflict (device_id) do update set
    tokens = players.tokens + p_amount,
    last_daily = coalesce(players.last_daily, current_date);
  select tokens into bal from players where device_id = p_device;
  return bal;
end $$;

-- Client-facing tables are private; all access goes through the RPCs above
-- and through edge functions (which use the service role).
alter table public.players enable row level security;
alter table public.orders  enable row level security;
revoke all on public.players from anon, authenticated;
revoke all on public.orders  from anon, authenticated;

grant execute on function public.get_balance(uuid)            to anon, authenticated;
grant execute on function public.spend_tokens(uuid, integer)  to anon, authenticated;
