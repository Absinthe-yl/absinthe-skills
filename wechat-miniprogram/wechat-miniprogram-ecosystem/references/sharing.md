# Sharing + WebSocket + cross-platform snippets

## Sharing (chat + Moments)

```javascript
Page({
  onShareAppMessage() {
    return {
      title: '来看看这个好物',
      path: '/pages/product/product?id=123',
      imageUrl: 'https://cdn.example.com/share/cover.jpg',
    };
  },
  onShareTimeline() {
    return {
      title: '来看看这个好物',
      query: 'id=123',
      imageUrl: 'https://cdn.example.com/share/cover.jpg',
    };
  },
});
```

- `onShareAppMessage` controls the in-chat card (title/path/imageUrl).
- `onShareTimeline` controls Moments; no custom path image, use `query`.
- A page only becomes shareable if it defines `onShareAppMessage` (or the button sets `open-type="share"`).

## WebSocket skeleton

```javascript
let socket = null, heartbeat = null;
function connect(url, onMsg) {
  socket = wx.connectSocket({ url });
  socket.onOpen(() => {
    heartbeat = setInterval(() => socket.send({ data: 'ping' }), 25000);
  });
  socket.onMessage((res) => onMsg(res.data));
  socket.onClose(() => { clearInterval(heartbeat); reconnect(url, onMsg); });
  socket.onError((e) => { clearInterval(heartbeat); reconnect(url, onMsg); });
}
function reconnect(url, onMsg) {
  setTimeout(() => connect(url, onMsg), 3000); // backoff
}
```

## Official Account → Mini Program

- In OA admin: 小程序管理 → 关联小程序 (bind appid).
- Article embed: `<mp>` component or `appid` + `path` link → jumps to MP.
- MP → OA follow: `wx.openOfficialAccount({ url })` with the OA profile URL.

## Cross-platform (Taro / uni-app)

- Taro: `import Taro from '@tarojs/taro'`; use `Taro.request`, `Taro.login` — maps to `wx.*` on WeChat.
- uni-app: `uni.request`, `uni.login` — same cross-platform surface.
- Keep a `platform/` adapter for WeChat-only calls (subscribe message, payment) behind an interface.
