// GET /functions/v1/order-status?order_id=<uuid>
// The player's browser polls this. Returns { status, tokens }.
// If the notify was missed, an active Alipay query settles the order here.
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
    .select("device_id, out_trade_no, status")
    .eq("id", orderId)
    .single();

  if (error || !order) return new Response(JSON.stringify({ error: "order not found" }), { status: 404, headers: cors });

  if (order.status !== "paid") {
    // Notify may not have arrived yet (or at all) — ask Alipay directly.
    const tradeStatus = await queryTrade(order.out_trade_no);
    if (tradeStatus === "TRADE_SUCCESS" || tradeStatus === "TRADE_FINISHED") {
      const { error: updErr } = await supabase
        .from("orders")
        .update({ status: "paid", paid_at: new Date().toISOString() })
        .eq("id", orderId)
        .eq("status", "pending");
      if (updErr) console.error("order update failed:", updErr);
      else {
        const { error: creditErr } = await supabase.rpc("credit_tokens", {
          p_device: order.device_id,
          p_amount: 5,
        });
        if (creditErr) console.error("credit failed:", creditErr);
      }
    } else if (tradeStatus === "TRADE_CLOSED") {
      await supabase.from("orders").update({ status: "closed" }).eq("id", orderId).eq("status", "pending");
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
