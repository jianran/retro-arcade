// GET /functions/v1/toss-page?order=<our order uuid>
// Hosted Toss Payment Widget page: the player pays with card/Toss here,
// then Toss redirects to toss-done which confirms and credits the tokens.
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

Deno.serve(async (req) => {
  const url = new URL(req.url);
  const orderId = url.searchParams.get("order");
  if (!orderId) return new Response("missing order", { status: 400 });

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );
  const { data: order } = await supabase
    .from("orders")
    .select("out_trade_no, amount, device_id")
    .eq("id", orderId)
    .single();

  if (!order) return new Response("order not found", { status: 404 });

  const clientKey = Deno.env.get("TOSS_CLIENT_KEY")!;
  const amount = Number(order.amount);
  const successUrl = `${Deno.env.get("SUPABASE_URL")}/functions/v1/toss-done?order=${orderId}`;
  const failUrl = successUrl;

  const html = `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Retro Arcade — 결제</title>
<style>
  body{font-family:-apple-system,sans-serif;background:#07060f;color:#ece9ff;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
  .box{width:min(420px,92vw);background:#141126;border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:24px}
  h1{font-size:18px;margin:0 0 6px}
  p{color:#9a93c2;font-size:13px;margin:0 0 16px}
  button{width:100%;padding:13px;border:0;border-radius:10px;background:#4ade80;color:#06210f;font-weight:800;font-size:15px;cursor:pointer}
  button:disabled{opacity:.5}
</style>
</head>
<body>
<div class="box">
  <h1>🎮 Retro Arcade</h1>
  <p>5 tokens — ₩${amount.toLocaleString()}</p>
  <div id="payment-method"></div>
  <div id="agreement"></div>
  <button id="payment-button" disabled>결제하기</button>
</div>
<script src="https://js.tosspayments.com/v1/payment-widget"></script>
<script>
  const clientKey = ${JSON.stringify(clientKey)};
  const customerKey = ${JSON.stringify("arcade-" + order.device_id)};
  const paymentWidget = PaymentWidget(clientKey, customerKey);
  paymentWidget.renderPaymentMethods("#payment-method", { value: ${amount} });
  paymentWidget.renderAgreement("#agreement", { variantKey: "AGREEMENT" });
  const btn = document.getElementById("payment-button");
  btn.disabled = false;
  btn.addEventListener("click", () => {
    paymentWidget.requestPayment({
      orderId: ${JSON.stringify(order.out_trade_no)},
      orderName: "Retro Arcade tokens x5",
      successUrl: ${JSON.stringify(successUrl)},
      failUrl: ${JSON.stringify(failUrl)},
    });
  });
</script>
</body>
</html>`;

  return new Response(html, { headers: { "Content-Type": "text/html; charset=utf-8" } });
});
