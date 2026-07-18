---
name: wechat-miniprogram-scaffold
description: This skill should be used when building, initializing, or restructuring a WeChat Mini Program (微信小程序) project. It provides the standard project structure, app.json configuration, a unified wx.request wrapper with auth/token handling, the WeChat login flow, custom component patterns, and lifecycle conventions. Use it whenever scaffolding a new Mini Program, setting up the request/network layer, implementing wx.login + session exchange, or establishing component and global-data conventions.
description_zh: 微信小程序项目脚手架与基础架构
description_en: WeChat Mini Program Scaffold
disable: false
agent_created: true
---

# WeChat Mini Program Scaffold

## When to use

Trigger this skill when the user asks to:

- Create a new WeChat Mini Program project or restructure an existing one.
- Define `app.json` (pages, tabBar, window, subpackages, permissions) or `project.config.json`.
- Build the unified network layer (`wx.request` wrapper) with token injection, 401 refresh, and error handling.
- Implement the WeChat login flow (`wx.login` → server session → access token).
- Write a custom component (properties / events / slots / `observers`).
- Decide package-size strategy (main package vs subpackages) or set up global state (`app.globalData`).

## Core workflow

1. Establish the project skeleton.
   - Create `app.js`, `app.json`, `app.wxss`, `project.config.json`, `sitemap.json`.
   - Place pages under `pages/`, reusable components under `components/`, utilities under `utils/`, business logic under `services/`.
   - See `references/project-structure.md` for the full tree and the purpose of each file.
2. Configure `app.json`.
   - Register all page routes under `pages`, the tab bar under `tabBar`, global window style under `window`.
   - Declare `permission` (e.g. `scope.userLocation`) and `requiredPrivateInfos` for any private API used.
   - Plan subpackages before the main package exceeds ~1.5MB. See `references/app-json.md` for templates.
3. Build the request wrapper (`utils/request.js`).
   - Wrap callback-based `wx.request` in Promises; inject `Authorization` from storage; handle 401 by refreshing token; reject with a structured error.
   - Use `HTTPS` only and rely on domains whitelisted in the MP backend (see `wechat-miniprogram-review-compliance`).
   - Use the template in `references/request-wrapper.md`.
4. Implement the login + session flow (`utils/auth.js`).
   - Call `wx.login()` to get `code`, exchange it for `access_token`/`refresh_token` on the server, persist tokens in storage.
   - On 401, call backend refresh endpoint with `refresh_token`; queue/retry the original request after success.
   - Use the template in `references/auth-flow.md`.
5. Write custom components with the standard contract.
   - Define `properties` (with `type`/`value`/`observer`), `methods`, `data`, and `options.externalClasses` as needed.
   - Emit changes via `triggerEvent`; support `slot` for composition.
   - Minimize `setData` payloads by passing only what the view needs.
6. Manage global state.
   - Prefer `app.globalData` for simple shared state; graduate to `mobx-miniprogram` or a custom store for complex apps.
   - Avoid storing large objects in global data (it crosses the JS↔native bridge on every `setData`).

## Critical constraints

- No DOM manipulation: Mini Programs use a dual-thread model; never access `document`/`window`.
- `wx.request` must target HTTPS domains whitelisted in the MP admin console.
- Main package must stay under 2MB; use subpackages (up to 20MB total) for non-entry features.
- Wrap all `wx.*` callback APIs in Promises for readable async code.
- Respect lifecycle: `App()` (onLaunch/onShow/onHide), `Page()` (onLoad/onShow/onReady/onHide/onUnload), `Component()`.

## Output patterns

When scaffolding, produce the directory tree plus the key files (`app.json`, `utils/request.js`, `utils/auth.js`). When extending an existing project, modify only the affected files and keep the request/auth contract consistent.

## Pitfalls

- Do not call `wx.request` directly across the codebase; always go through the wrapper to keep token and error handling centralized.
- Do not store tokens in `globalData` only; persist to storage so sessions survive cold starts.
- Do not put marketing/secondary pages in the main package; move them to subpackages early.
- Do not `setData` the whole `data` object; patch only changed fields.
- Do not request sensitive scopes (`userInfo`, `location`) without a visible, justified use case on the page.
