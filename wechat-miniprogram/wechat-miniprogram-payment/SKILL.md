---
name: wechat-miniprogram-payment
description: This skill should be used when implementing WeChat Pay (微信支付) in a Mini Program, handling order creation, payment signature verification, refunds, or subscription message (订阅消息) authorization and delivery. Use it for wx.requestPayment integration, server-side prepay parameter generation, payment-result handling, wx.requestSubscribeMessage opt-in flows, and template-message replacement patterns.
description_zh: 微信小程序支付与订阅消息
description_en: WeChat Mini Program Payment
disable: false
agent_created: true
---

# WeChat Mini Program Payment

## When to use

Trigger this skill when the user asks to:

- Integrate WeChat Pay (`wx.requestPayment`) into a Mini Program.
- Create an order, obtain prepay parameters from the server, and invoke payment.
- Handle payment success / cancellation / failure and sync order status.
- Implement refunds (server-side) and the refund status callback.
- Request subscription message authorization (`wx.requestSubscribeMessage`) and send template messages after opt-in.
- Understand the difference between deprecated template messages and the current subscription message model.

## Core workflow

1. Create the order server-side, then pay client-side.
   - The server creates the order and calls WeChat Pay `unifiedorder` (JSAPI) to get `prepay_id`.
   - The server signs `timeStamp`, `nonceStr`, `package`, `signType`, `paySign` and returns them to the Mini Program. **Never sign or hold the merchant key on the client.**
   - The client invokes `wx.requestPayment` with those parameters. See `references/payment-flow.md`.
2. Handle payment outcomes.
   - `success` → treat as "payment submitted", then poll the server order status (do not trust client success alone; verify via payment notify callback).
   - `fail` with `errMsg` containing `cancel` → user cancelled; allow retry.
   - Other `fail` → payment failed; show reason, no order state change.
3. Verify payment via the notify callback (server).
   - WeChat Pay pushes an async notify to the server; verify the signature and `result_code`, then mark order paid.
   - Return the required success XML `<xml><return_code><![CDATA[SUCCESS]]></return_code></xml>` to stop retries.
4. Implement refunds server-side.
   - Refunds are always server-initiated (merchant API). The Mini Program only shows status.
   - Listen for the refund notify callback to update the order/refund state.
5. Use subscription messages for post-pay / service notifications.
   - Request authorization at the moment of highest intent (e.g. right after placing an order): `wx.requestSubscribeMessage({ tmplIds })`.
   - Send the message from the server within the granted validity window using the template ID.
   - The user can only be asked once per template per call; accepted templates are valid for a limited time (check current base-library docs).
   - See `references/subscription-message.md`.

## Critical constraints

- `wx.requestPayment` parameters must be server-signed; the merchant API key (`APIv3 key`) never ships to the client.
- Payment success on the client is not proof of payment — always confirm via the server notify callback.
- Subscription messages replaced template messages; do not build new template-message flows.
- Respect the one-time opt-in: calling `requestSubscribeMessage` again does not re-prompt for an already-decided template.
- All payment/notify endpoints must be HTTPS and whitelisted.

## Output patterns

When implementing payment, deliver: the server-side order/prepay pseudocode (or note to implement server-side), the client `requestPayment` call, and the result-handling branch. When implementing subscription messages, deliver the `requestSubscribeMessage` trigger point plus the server send note.

## Pitfalls

- Do not store or sign the merchant key in the Mini Program.
- Do not mark the order "paid" on client `success` alone; wait for the notify callback.
- Do not request subscription authorization on page load; ask at the action moment or users decline.
- Do not assume permanent subscription; templates expire — re-request when the user re-engages.
- Do not ignore `cancel` — it is not an error, it is a user choice.
