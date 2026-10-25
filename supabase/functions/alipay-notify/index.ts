// POST /functions/v1/alipay-notify   (form-encoded, called by Alipay's server)
// Verifies the RSA2 signature, marks the order paid, credits 5 tokens.
// Must reply with the literal text "success" so Alipay stops retrying.
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";
import { verifyNotify } from "../_shared/alipay.ts";

const PAID_STATUSES = ["TRADE_SUCCESS", "TRADE_FINISHED"];

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("success");

  let params: URLSearchParams;
  try {
    params = new URLSearchParams(await req.text());
  } catch {
    return new Response("success");
  }

  if (!(await verifyNotify(params))) {
    console.error("notify signature verification failed");
    return new Response("failure");
  }

  const outTradeNo = params.get("out_trade_no");
  const tradeStatus = params.get("trade_status");
  if (!outTradeNo || !PAID_STATUSES.includes(tradeStatus ?? "")) {
    return new Response("success"); // nothing to do (e.g. TRADE_CLOSED)
  }

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  // Idempotent: only the first PAID transition credits tokens.
  const { data: order, error } = await supabase
    .from("orders")
    .select("device_id, status")
    .eq("out_trade_no", outTradeNo)
    .single();

  if (error || !order) {
    console.error("order lookup failed:", error);
    return new Response("success");
  }
  if (order.status !== "pending") {
    return new Response("success"); // already handled
  }

  const { error: updErr } = await supabase
    .from("orders")
    .update({ status: "paid", paid_at: new Date().toISOString() })
    .eq("out_trade_no", outTradeNo)
    .eq("status", "pending"); // guard against concurrent notifies

  if (updErr) {
    console.error("order update failed:", updErr);
    return new Response("success");
  }

  const { error: creditErr } = await supabase.rpc("credit_tokens", {
    p_device: order.device_id,
    p_amount: 5,
  });
  if (creditErr) console.error("credit failed:", creditErr);

  return new Response("success");
});
