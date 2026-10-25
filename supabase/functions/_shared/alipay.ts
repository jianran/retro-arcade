// Alipay 当面付 (alipay.trade.precreate) helpers — shared by edge functions.
// Env vars (set with `supabase secrets set`):
//   ALIPAY_APP_ID           merchant app id
//   ALIPAY_APP_PRIVATE_KEY  merchant app private key (PKCS8 PEM, RSA2)
//   ALIPAY_PUBLIC_KEY       Alipay's public key (PEM) for verifying notify signatures
//   ALIPAY_GATEWAY          https://openapi-sandbox.dl.alipaydev.com/gateway.do (sandbox)
//                           or https://openapi.alipay.com/gateway.do (production)

function pemToBytes(pem: string): Uint8Array {
  const b64 = pem
    .replace(/-----BEGIN [^-]+-----/g, "")
    .replace(/-----END [^-]+-----/g, "")
    .replace(/\s+/g, "");
  const bin = atob(b64);
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
}

export async function rsaSign(signStr: string, privateKeyPem: string): Promise<string> {
  const key = await crypto.subtle.importKey(
    "pkcs8",
    pemToBytes(privateKeyPem),
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign("RSASSA-PKCS1-v1_5", key, new TextEncoder().encode(signStr));
  return btoa(String.fromCharCode(...new Uint8Array(sig)));
}

export async function rsaVerify(content: string, signatureB64: string, publicKeyPem: string): Promise<boolean> {
  try {
    const key = await crypto.subtle.importKey(
      "spki",
      pemToBytes(publicKeyPem),
      { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
      false,
      ["verify"],
    );
    const sigBytes = Uint8Array.from(atob(signatureB64), (c) => c.charCodeAt(0));
    return await crypto.subtle.verify("RSASSA-PKCS1-v1_5", key, sigBytes, new TextEncoder().encode(content));
  } catch {
    return false;
  }
}

function alipayTimestamp(): string {
  // Alipay wants "yyyy-MM-dd HH:mm:ss" in GMT+8
  const d = new Date(Date.now() + 8 * 3600 * 1000);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getUTCFullYear()}-${p(d.getUTCMonth() + 1)}-${p(d.getUTCDate())} ${p(d.getUTCHours())}:${p(d.getUTCMinutes())}:${p(d.getUTCSeconds())}`;
}

interface GateParams { [k: string]: string }

async function gatewayCall(method: string, bizContent: object, notifyUrl?: string): Promise<any> {
  const params: GateParams = {
    app_id: Deno.env.get("ALIPAY_APP_ID")!,
    method,
    format: "JSON",
    charset: "utf-8",
    sign_type: "RSA2",
    timestamp: alipayTimestamp(),
    version: "1.0",
    biz_content: JSON.stringify(bizContent),
  };
  if (notifyUrl) params.notify_url = notifyUrl;

  const signStr = Object.keys(params)
    .filter((k) => params[k] !== undefined)
    .sort()
    .map((k) => `${k}=${params[k]}`)
    .join("&");
  params.sign = await rsaSign(signStr, Deno.env.get("ALIPAY_APP_PRIVATE_KEY")!);

  const body = new URLSearchParams(params).toString();
  const res = await fetch(Deno.env.get("ALIPAY_GATEWAY")!, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded;charset=utf-8" },
    body,
  });
  return await res.json();
}

const RESP_KEY: { [m: string]: string } = {
  "alipay.trade.precreate": "alipay_trade_precreate_response",
  "alipay.trade.query": "alipay_trade_query_response",
};

export async function precreate(args: {
  outTradeNo: string;
  totalAmount: string;
  subject: string;
  notifyUrl: string;
}): Promise<string> {
  const data = await gatewayCall(
    "alipay.trade.precreate",
    {
      out_trade_no: args.outTradeNo,
      total_amount: args.totalAmount,
      subject: args.subject,
      timeout_express: "10m",
    },
    args.notifyUrl,
  );
  const r = data[RESP_KEY["alipay.trade.precreate"]];
  if (!r || r.code !== "10000") {
    throw new Error(`precreate failed: ${r?.code} ${r?.msg} ${r?.sub_msg ?? ""}`.trim());
  }
  return r.qr_code as string;
}

// Returns trade_status: WAIT_BUYER_PAY | TRADE_SUCCESS | TRADE_FINISHED | TRADE_CLOSED
export async function queryTrade(outTradeNo: string): Promise<string | null> {
  const data = await gatewayCall("alipay.trade.query", { out_trade_no: outTradeNo });
  const r = data[RESP_KEY["alipay.trade.query"]];
  if (!r || r.code !== "10000") return null;
  return (r.trade_status as string) ?? null;
}

// Verify an async notify (form-encoded params from Alipay).
// Returns true when the signature is valid and the payment succeeded.
export async function verifyNotify(params: URLSearchParams): Promise<boolean> {
  const sign = params.get("sign");
  if (!sign) return false;
  const keys = [...params.keys()].filter((k) => k !== "sign" && k !== "sign_type");
  keys.sort();
  const content = keys.map((k) => `${k}=${params.get(k)}`).join("&");
  return await rsaVerify(content, sign, Deno.env.get("ALIPAY_PUBLIC_KEY")!);
}
