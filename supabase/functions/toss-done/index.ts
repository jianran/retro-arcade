// GET /functions/v1/toss-done?order=<uuid>&paymentKey=...&orderId=...&amount=...
// Toss redirects here after the widget payment. Confirms with the server key,
// credits tokens, and sends the player back to the arcade (which is polling).
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

const ARCADE_URL = "https://jianran.github.io/retro-arcade/";

Deno.serve(async (req) => {
  const url = new URL(req.url);
  const orderId = url.searchParams.get("order");
  const paymentKey = url.searchParams.get("paymentKey");
  const tossOrderId = url.searchParams.get("orderId");
  const amount = url.searchParams.get("amount");

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  const redirect = (ok: boolean) =>
    new Response(null, { status: 302, headers: { Location: `${ARCADE_URL}#${ok ? "paid" : "payfail"}` } });

  if (!orderId || !paymentKey || !tossOrderId || !amount) return redirect(false);

  try {
    const auth = btoa(`${Deno.env.get("TOSS_SECRET_KEY")}:`);
    const res = await fetch("https://api.tosspayments.com/v1/payments/confirm", {
      method: "POST",
      headers: { Authorization: `Basic ${auth}`, "Content-Type": "application/json" },
      body: JSON.stringify({ paymentKey, orderId: tossOrderId, amount: Number(amount) }),
    });
    if (!res.ok) {
      console.error("toss confirm failed:", res.status, await res.text());
      return redirect(false);
    }
    const payment = await res.json();

    if (payment.status === "DONE") {
      // Idempotent settle: only the first PAID transition credits tokens
      await supabase
        .from("orders")
        .update({ status: "paid", paid_at: new Date().toISOString() })
        .eq("id", orderId)
        .eq("status", "pending");
      const { data: order } = await supabase.from("orders").select("device_id").eq("id", orderId).single();
      if (order) {
        const { error: creditErr } = await supabase.rpc("credit_tokens", {
          p_device: order.device_id,
          p_amount: 5,
        });
        if (creditErr) console.error("credit failed:", creditErr);
      }
      return redirect(true);
    }
  } catch (e) {
    console.error("toss-done error:", e);
  }
  return redirect(false);
});
