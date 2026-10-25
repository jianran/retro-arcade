# Automatic token purchases — setup guide

The arcade gets a server-side wallet: balances live in Supabase, and the Buy
button shows a live Alipay QR. When the payment lands, Alipay calls our
webhook and the player's tokens appear automatically. No codes, no manual steps.

## What you need to create (the only parts that need you)

### 1. Supabase project (free tier)

1. Go to https://supabase.com → sign up (GitHub login works) → **New project**
2. Name it anything (`retro-arcade`), pick a region near your players, set a database password
3. Once created: **Project Settings → API** → copy:
   - **Project URL** (`https://xxxx.supabase.co`)
   - **anon public** key
4. Paste both into `index.html` (`SUPABASE_URL`, `SUPABASE_ANON`)
   — or hand them to Claude and say "finish the setup"
5. **SQL Editor → New query** → paste the contents of `supabase/schema.sql` → **Run**
6. Deploy the functions (Claude can do this once you run `supabase login`):
   ```bash
   supabase secrets set --project-ref <your-project-ref> \
     ALIPAY_APP_ID=... \
     ALIPAY_APP_PRIVATE_KEY="..." \
     ALIPAY_PUBLIC_KEY="..." \
     ALIPAY_GATEWAY=https://openapi-sandbox.dl.alipaydev.com/gateway.do
   supabase functions deploy buy --project-ref <your-project-ref>
   supabase functions deploy alipay-notify --project-ref <your-project-ref>
   supabase functions deploy order-status --project-ref <your-project-ref>
   ```
   (`SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` secrets are set automatically
   by the CLI on deploy.)

### 2. Alipay 当面付 merchant app

1. Register a merchant Alipay account: https://open.alipay.com → 商家入驻
   (you need 支付宝商家/个体户 status — a personal collection QR cannot do this)
2. Create an app → enable **当面付** (alipay.trade.precreate)
3. Get from the app's keys page:
   - **app_id**
   - **应用私钥** (app private key, PKCS8/RSA2) — generate a keypair on that page
     and save the private key
   - **支付宝公钥** (Alipay public key)
4. First test with the **sandbox** (沙箱环境) — set `ALIPAY_GATEWAY` to
   `https://openapi-sandbox.dl.alipaydev.com/gateway.do` and use the sandbox
   app keys + 沙箱买家 test account. Pay with the sandbox wallet on your phone
   (no real money). Then switch `ALIPAY_GATEWAY` to
   `https://openapi.alipay.com/gateway.do` with production keys.

## How the flow works

```
player clicks Buy
   → browser → /functions/v1/buy → alipay.trade.precreate → QR shown in shop
player scans + pays
   → Alipay server → /functions/v1/alipay-notify (signed) → order=paid, +5 tokens
   → browser polls /functions/v1/order-status every 3s → sees paid → +5 tokens shown
```

Missed webhooks don't matter: the poll also asks Alipay directly
(`alipay.trade.query`) and settles the order.

## Offline fallback

If Supabase isn't configured or is unreachable, the arcade automatically falls
back to the old in-browser wallet: 5 tokens/day, and the owner's signed
top-up codes from `topup.html` still work.
