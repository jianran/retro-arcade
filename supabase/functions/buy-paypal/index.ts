// POST /functions/v1/buy-paypal  { device_id }
// Creates a PayPal order ($1 = 5 tokens) and returns its approval URL.
// Env secrets: PAYPAL_CLIENT_ID, PAYPAL_SECRET, PAYPAL_API_BASE
//   (sandbox: https://api-m.sandbox.paypal.com  |  prod: https://api-m.paypal.com)
//   PAYPAL_AMOUNT (default "1.00"), PAYPAL_CURRENCY (default "USD")
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

const ARCADE_URL = "https://jianran.github.io/retro-arcade/";
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

  const amount = Deno.env.get("PAYPAL_AMOUNT") || "1.00";
  const currency = Deno.env.get("PAYPAL_CURRENCY") || "USD";
  const auth = btoa(`${Deno.env.get("PAYPAL_CLIENT_ID")}:${Deno.env.get("PAYPAL_SECRET")}`);

  let pp;
  try {
    const res = await fetch(`${Deno.env.get("PAYPAL_API_BASE")}/v2/checkout/orders`, {
      method: "POST",
      headers: { Authorization: `Basic ${auth}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        intent: "CAPTURE",
        purchase_units: [{
          amount: { currency_code: currency, value: amount },
        }],
        application_context: {
          brand_name: "Retro Arcade",
          user_action: "PAY_NOW",
          return_url: ARCADE_URL,
          cancel_url: ARCADE_URL,
        },
      }),
    });
    pp = await res.json();
    if (!res.ok || !pp.id) throw new Error(`PayPal order failed: ${pp.message || pp.error || res.status}`);
  } catch (e) {
    console.error("paypal create error:", e);
    return new Response(JSON.stringify({ error: "payment provider unavailable: " + (e as Error).message }),
      { status: 502, headers: cors });
  }

  const outTradeNo = `PP${Date.now()}${Math.floor(Math.random() * 9000 + 1000)}`;
  const { data: order, error } = await supabase
    .from("orders")
    .insert({
      device_id: deviceId,
      out_trade_no: outTradeNo,
      amount: amount,
      status: "pending",
      provider: "paypal",
      external_ref: pp.id,
    })
    .select("id")
    .single();

  if (error || !order) {
    console.error("order insert error:", error);
    return new Response(JSON.stringify({ error: "could not create order" }), { status: 500, headers: cors });
  }

  const payUrl = (pp.links ?? []).find((l: any) => l.rel === "approve")?.href || "";

  return new Response(JSON.stringify({ order_id: order.id, pay_url: payUrl }),
    { status: 200, headers: { ...cors, "Content-Type": "application/json" } });
});
