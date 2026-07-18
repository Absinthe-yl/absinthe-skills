# Payment flow

## Client: services/payment.js

```javascript
const { request } = require('../../utils/request');

const createOrder = async (orderData) => {
  const prepayResult = await request({
    url: '/orders/create',
    method: 'POST',
    data: {
      items: orderData.items,
      address_id: orderData.addressId,
      coupon_id: orderData.couponId,
    },
  });

  return new Promise((resolve, reject) => {
    wx.requestPayment({
      timeStamp: prepayResult.timeStamp,
      nonceStr: prepayResult.nonceStr,
      package: prepayResult.package,   // "prepay_id=xxx"
      signType: prepayResult.signType, // 'RSA' or 'MD5'
      paySign: prepayResult.paySign,
      success: (res) => {
        resolve({ success: true, orderId: prepayResult.orderId });
      },
      fail: (err) => {
        if (err.errMsg && err.errMsg.includes('cancel')) {
          resolve({ success: false, reason: 'cancelled' });
        } else {
          reject({ success: false, reason: 'payment_failed', detail: err });
        }
      },
    });
  });
};

module.exports = { createOrder };
```

## Server responsibilities (pseudocode)

1. Create local order (status = `pending`), amount in cents.
2. Call WeChat Pay `unifiedorder` (JSAPI) with `openid` + `notify_url`.
3. Receive `prepay_id`; build sign package:
   - fields: `appId, timeStamp, nonceStr, package="prepay_id=xxx", signType`
   - `paySign` = sign with merchant APIv3 key (RSA or HMAC-SHA256/MD5 per `signType`).
4. Return sign package + `orderId` to client.
5. Provide `notify_url`:
   - verify callback signature, idempotently mark order `paid`, return SUCCESS XML.

## Refund (server-only)

- Call merchant refund API with `out_trade_no` / `out_refund_no`, `refund`, `total`.
- Handle `refund.notify_url` callback to set order/refund status.
- Never expose refund capability to the client.
