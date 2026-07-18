---
name: wechat-miniprogram
description: "This is the umbrella skill for building WeChat Mini Programs (微信小程序). It covers the full development lifecycle: project scaffolding and architecture, the unified network/login layer, WeChat Pay and subscription messages, performance optimization, review submission and compliance (privacy, domains, content security), and ecosystem integration (sharing, Official Account, Channels, Enterprise WeChat, WebSocket, cross-platform). Route to the matching sub-module under this folder based on the task."
---

# WeChat Mini Program (umbrella skill)

This skill bundles the complete WeChat Mini Program development capability. It is organized as a single skill with focused sub-modules so context stays lean — load only the sub-module relevant to the current task.

## When to use

Use this skill (and the relevant sub-module) when the user asks to build, optimize, or ship a WeChat Mini Program, including:

- Scaffolding a project, configuring `app.json`, building the request/login layer, or writing custom components → `wechat-miniprogram-scaffold`
- Implementing WeChat Pay or subscription messages → `wechat-miniprogram-payment`
- Optimizing startup, `setData`, package size, images, or network → `wechat-miniprogram-performance`
- Submitting for review, handling privacy/domain/compliance, or diagnosing rejections → `wechat-miniprogram-review-compliance`
- Integrating sharing, Official Account, Channels, Enterprise WeChat, WebSocket, or cross-platform frameworks → `wechat-miniprogram-ecosystem`

## Sub-module index

| Sub-module | Path | Covers |
|---|---|---|
| Scaffold | `wechat-miniprogram-scaffold/` | Project structure, `app.json` config, unified `wx.request` wrapper, `wx.login` + token/session, component patterns, global state |
| Payment | `wechat-miniprogram-payment/` | `wx.requestPayment`, server-side prepay signing, payment result handling, refunds, subscription messages |
| Performance | `wechat-miniprogram-performance/` | Startup time, `setData` efficiency, subpackage/size strategy, image & network optimization, virtual lists |
| Review & Compliance | `wechat-miniprogram-review-compliance/` | Domain whitelist, privacy authorization, PIPL, content security (`msgSecCheck`/`imgSecCheck`), submission checklist & common rejections |
| Ecosystem | `wechat-miniprogram-ecosystem/` | `onShareAppMessage`/`onShareTimeline`, Official Account binding, Channels commerce, Enterprise WeChat, WebSocket, Taro/uni-app |

## How to use

1. Identify which sub-module matches the task from the index above.
2. Read that sub-module's `SKILL.md` and its `references/` for templates and code.
3. Apply the constraints called out in the sub-module (and the shared ones below).

## Shared constraints (apply to all sub-modules)

- **Dual-thread model**: no DOM access; wrap callback `wx.*` APIs in Promises.
- **Network**: HTTPS only; all domains must be whitelisted in the MP backend.
- **Package size**: main package < 2MB, total with subpackages ≤ 20MB.
- **setData is the hot path**: batch updates, patch by path, minimize payload.
- **Privacy & compliance**: request sensitive scopes only with a visible, justified use case; gate private APIs behind the Privacy API consent.
- **Payment safety**: the merchant key never ships to the client; treat client `success` as "submitted", verify via server notify callback.

## Critical rules

- Do not call `wx.request` directly across the codebase — route through the scaffold's wrapper.
- Do not store tokens in `globalData` only; persist to storage.
- Do not force or induce sharing (review rejection).
- Do not skip content security for user-generated content.
- Do not block first paint on non-critical init (analytics/SDKs).
