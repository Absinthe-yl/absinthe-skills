# Subscription message

Subscription messages (订阅消息) replaced template messages. The user must opt in; the server sends within the granted window.

## Client: request authorization at the right moment

```javascript
const requestSubscription = (templateIds) => {
  return new Promise((resolve) => {
    wx.requestSubscribeMessage({
      tmplIds: templateIds,
      success: (res) => {
        const accepted = templateIds.filter((id) => res[id] === 'accept');
        resolve({ accepted, result: res });
      },
      fail: () => resolve({ accepted: [], result: {} }),
    });
  });
};

// Best trigger: right after order placed / action completed
const afterPlaceOrder = async () => {
  const { accepted } = await requestSubscription([
    'TEMPLATE_ID_ORDER_SHIP',
    'TEMPLATE_ID_ORDER_DONE',
  ]);
  // Send accepted templates to server so it can push later
  await request({ url: '/user/subscription', method: 'POST', data: { templates: accepted } });
};
```

## Server: send the message

```
POST https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=ACCESS_TOKEN
{
  "touser": "<openid>",
  "template_id": "<tmplId>",
  "page": "pages/order/order?id=123",
  "data": {
    "thing1": { "value": "已发货" },
    "time2": { "value": "2026-07-18 12:00" }
  }
}
```

## Rules

- Each `requestSubscribeMessage` call can ask for multiple templates at once (up to the limit).
- A user decision is one-time: `accept` grants a send window; `reject`/`ban` will not re-prompt until the user changes settings.
- The server must hold a valid `access_token` (cached, refreshed before expiry).
- `data` field keys/values must match the template's parameter list exactly.
