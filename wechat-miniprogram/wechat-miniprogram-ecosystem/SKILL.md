---
name: wechat-miniprogram-ecosystem
description: This skill should be used when integrating a WeChat Mini Program (微信小程序) with the broader WeChat ecosystem: sharing to chat and Moments (onShareAppMessage/onShareTimeline), Official Account (公众号) binding, WeChat Channels (视频号) commerce links, Enterprise WeChat (企业微信) flows, WebSocket real-time features, and cross-platform frameworks (Taro/uni-app). Trigger it for social distribution, OA+MP traffic, live-commerce links, IM/customer-service, real-time updates, and write-once-deploy multi-platform builds.
description_zh: 微信小程序生态集成
description_en: WeChat Mini Program Ecosystem
disable: false
agent_created: true
---

# WeChat Mini Program Ecosystem

## When to use

Trigger this skill when the user asks to:

- Add sharing: `onShareAppMessage` (chat) and `onShareTimeline` (Moments/朋友圈).
- Bind or deep-link with an Official Account (公众号) — article → MP, MP → subscribe.
- Embed Mini Program links in WeChat Channels (视频号) short video / live commerce.
- Build Enterprise WeChat (企业微信) customer flows or internal tools.
- Add real-time features via WebSocket (chat, live updates, collaborative).
- Choose or scaffold a cross-platform framework (Taro / uni-app / Remax).
- Integrate native plugins (maps, live video, AR) or adapter layers.

## Core workflow

1. Sharing (social distribution).
   - Define `onShareAppMessage` (title/path/imageUrl) on pages; set `onShareAppMessage` `imageUrl` for a better card.
   - Add `onShareTimeline` for Moments; note it has no custom path image — provide `query` + `imageUrl`.
   - Sharing opt-in is highest right after a meaningful action; never force it (review risk).
   - See `references/sharing.md`.
2. Official Account binding.
   - Link MP in the OA admin ("小程序管理") to mutual-jump: OA article → MP via `<mp>` component / `appid` link; MP → OA via `wx.navigateTo`/`wx.openOfficialAccount` for follow.
   - Pass `scene`/`query` to attribute traffic.
3. WeChat Channels (视频号) commerce.
   - Use `live-player` / `channels` open APIs to jump from a live room or video to the MP product page.
   - Embed MP path in the Channels product card; keep the path consistent with the MP route.
4. Enterprise WeChat (企业微信).
   - For customer service: `wx.openCustomerServiceChat` to open the enterprise session from the MP.
   - For internal tools: build an MP bound to the corp; use `corp` identity and JS-SDK where needed.
5. Real-time via WebSocket.
   - Establish `wx.connectSocket`; handle `onOpen/onMessage/onClose/onError`; reconnect with backoff.
   - Heartbeat to keep alive; serialize messages; never block UI on socket state.
   - See `references/websocket.md`.
6. Cross-platform frameworks.
   - Taro: React/Vue syntax, deploys to WeChat/Alipay/Baidu/ByteDance. Good for teams with web background.
   - uni-app: Vue-based, large plugin market, strong WeChat optimization.
   - Keep a WeChat-specific adapter layer for API differences; isolate `wx.*` calls.
   - See `references/cross-platform.md`.

## Critical constraints

- `onShareTimeline` requires the page to also define `onShareAppMessage`; Moments shares can't carry custom path images.
- Forced/induced sharing violates review policy — keep sharing voluntary.
- WebSocket must reconnect gracefully; WeChat may kill idle sockets.
- Channels/live commerce paths must match existing MP routes or jump fails.
- Cross-platform: always wrap platform APIs; don't assume `wx.*` exists on non-WeChat targets.

## Output patterns

When adding sharing, deliver both `onShareAppMessage` and `onShareTimeline` with `query`. When wiring OA/Channels, deliver the jump path + the `appid`/component needed. When adding WebSocket, deliver connect + reconnect + heartbeat skeleton.

## Pitfalls

- Don't force share-for-reward (rejection).
- Don't forget `onShareAppMessage` when adding `onShareTimeline` (timeline won't fire).
- Don't skip heartbeat/reconnect on WebSocket.
- Don't hardcode `wx.*` across a Taro/uni-app codebase — use the framework's cross-platform API.
