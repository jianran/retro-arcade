// GET /functions/v1/order-status?order_id=<uuid>
// The player's browser polls this. Returns { status, tokens }.
// For pending orders it asks the provider directly (PayPal REST / Alipay
// trade.query) so a missed webhook can't strand a payment.
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";
import { queryTrade } from "../_shared/alipay.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, content-type",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  const url = new URL(req.url);
  const orderId = url.searchParams.get("order_id");
  if (!orderId) return new Response(JSON.stringify({ error: "missing order_id" }), { status: 400, headers: cors });

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  const { data: order, error } = await supabase
    .from("orders")
    .select("device_id, out_trade_no, status, provider, external_ref")
    .eq("id", orderId)
    .single();

  if (error || !order) return new Response(JSON.stringify({ error: "order not found" }), { status: 404, headers: cors });

  const settle = async () => {
    // Idempotent: only the first PAID transition credits tokens.
    const { error: updErr } = await supabase
      .from("orders")
      .update({ status: "paid", paid_at: new Date().toISOString() })
      .eq("id", orderId)
      .eq("status", "pending");
    if (updErr) return;
    const { error: creditErr } = await supabase.rpc("credit_tokens", {
      p_device: order.device_id,
      p_amount: 5,
    });
    if (creditErr) console.error("credit failed:", creditErr);
  };

  if (order.status !== "paid") {
    try {
      if (order.provider === "paypal" && order.external_ref) {
        const auth = btoa(`${Deno.env.get("PAYPAL_CLIENT_ID")}:${Deno.env.get("PAYPAL_SECRET")}`);
        const headers = { Authorization: `Basic ${auth}`, "Content-Type": "application/json" };
        const res = await fetch(`${Deno.env.get("PAYPAL_API_BASE")}/v2/checkout/orders/${order.external_ref}`, { headers });
        const pp = await res.json();
        let st = pp.status;
        if (st === "APPROVED") {
          // intent=CAPTURE orders may still need an explicit capture
          const capRes = await fetch(`${Deno.env.get("PAYPAL_API_BASE")}/v2/checkout/orders/${order.external_ref}/capture`,
            { method: "POST", headers });
          if (capRes.ok) {
            const cap = await capRes.json();
            st = cap.status ?? st;
          }
        }
        if (st === "COMPLETED") await settle();
        else if (st === "VOIDED" || st === "PAYER_ACTION_REQUIRED") {
          await supabase.from("orders").update({ status: "closed" }).eq("id", orderId).eq("status", "pending");
        }
      } else if (order.provider === "toss" && order.external_ref) {
        // Toss: check the payment order for a DONE payment
        const auth = btoa(`${Deno.env.get("TOSS_SECRET_KEY")}:`);
        const res = await fetch(`https://api.tosspayments.com/v1/payments/orders/${order.external_ref}`,
          { headers: { Authorization: `Basic ${auth}` } });
        const d = await res.json();
        if ((d.payments ?? []).some((p: any) => p.status === "DONE")) {
          await settle();
        }
      } else {
        // Alipay (or legacy rows without provider)
        const tradeStatus = await queryTrade(order.out_trade_no);
        if (tradeStatus === "TRADE_SUCCESS" || tradeStatus === "TRADE_FINISHED") {
          await settle();
        } else if (tradeStatus === "TRADE_CLOSED") {
          await supabase.from("orders").update({ status: "closed" }).eq("id", orderId).eq("status", "pending");
        }
      }
    } catch (e) {
      console.error("provider status check failed:", e);
    }
  }

  const { data: player } = await supabase
    .from("players")
    .select("tokens")
    .eq("device_id", order.device_id)
    .single();
  const tokens = player?.tokens ?? 0;

  const { data: fresh } = await supabase.from("orders").select("status").eq("id", orderId).single();
  return new Response(JSON.stringify({ status: fresh?.status ?? "pending", tokens }),
    { status: 200, headers: { ...cors, "Content-Type": "application/json" } });
});
