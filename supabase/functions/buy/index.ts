// POST /functions/v1/buy  { device_id }
// Creates an Alipay face-to-face QR for ¥7 (5 tokens) and returns it.
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";
import { precreate } from "../_shared/alipay.ts";

const PRICE = "7.00"; // ¥7 = 5 tokens

Deno.serve(async (req) => {
  const cors = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "authorization, content-type",
  };
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

  const outTradeNo = `ARC${Date.now()}${Math.floor(Math.random() * 9000 + 1000)}`;

  let qrCode: string;
  try {
    qrCode = await precreate({
      outTradeNo,
      totalAmount: PRICE,
      subject: "Retro Arcade — 5 tokens",
      notifyUrl: `${Deno.env.get("SUPABASE_URL")}/functions/v1/alipay-notify`,
    });
  } catch (e) {
    console.error("precreate error:", e);
    return new Response(JSON.stringify({ error: "payment provider unavailable, try again later" }),
      { status: 502, headers: cors });
  }

  const { data: order, error } = await supabase
    .from("orders")
    .insert({ device_id: deviceId, out_trade_no: outTradeNo, amount: PRICE, status: "pending", qr_code: qrCode })
    .select("id")
    .single();

  if (error || !order) {
    console.error("order insert error:", error);
    return new Response(JSON.stringify({ error: "could not create order" }), { status: 500, headers: cors });
  }

  return new Response(JSON.stringify({ order_id: order.id, qr_code: qrCode }),
    { status: 200, headers: { ...cors, "Content-Type": "application/json" } });
});
