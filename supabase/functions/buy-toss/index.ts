// POST /functions/v1/buy-toss  { device_id }
// Creates a Toss Payments order for Korean players (₩1,400 = 5 tokens)
// and returns the URL of our hosted checkout page (toss-page).
// Env secrets: TOSS_CLIENT_KEY, TOSS_SECRET_KEY, TOSS_AMOUNT (default "1400")
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, content-type",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return new Response("method not allowed", { status: 405, headers: cors });

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  let deviceId: string;
  try {
    ({ device_id: deviceId } = await req.json());
  } catch {
    return new Response(JSON.stringify({ error: "bad request" }), { status: 400, headers: cors });
  }
  if (!deviceId || !/^[0-9a-f-]{36}$/i.test(deviceId)) {
    return new Response(JSON.stringify({ error: "invalid device_id" }), { status: 400, headers: cors });
  }

  await supabase.from("players").insert({ device_id: deviceId }, { ignoreDuplicates: true });

  const amount = Deno.env.get("TOSS_AMOUNT") || "1400";
  // Toss orderId: 6–64 chars, alphanumeric and dashes only
  const tossOrderId = `ARC-${Date.now()}-${Math.floor(Math.random() * 9000 + 1000)}`;

  const { data: order, error } = await supabase
    .from("orders")
    .insert({
      device_id: deviceId,
      out_trade_no: tossOrderId,
      amount: amount,
      status: "pending",
      provider: "toss",
      external_ref: tossOrderId,
    })
    .select("id")
    .single();

  if (error || !order) {
    console.error("order insert error:", error);
    return new Response(JSON.stringify({ error: "could not create order" }), { status: 500, headers: cors });
  }

  const checkoutUrl = `${Deno.env.get("SUPABASE_URL")}/functions/v1/toss-page?order=${order.id}`;

  return new Response(JSON.stringify({ order_id: order.id, checkout_url: checkoutUrl }),
    { status: 200, headers: { ...cors, "Content-Type": "application/json" } });
});
