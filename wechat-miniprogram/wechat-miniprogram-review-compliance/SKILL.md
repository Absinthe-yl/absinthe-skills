---
name: wechat-miniprogram-review-compliance
description: This skill should be used when preparing a WeChat Mini Program (微信小程序) for review submission, handling compliance, privacy authorization, domain whitelisting, content security, or diagnosing review rejections. Trigger it for sitemap/permission config, privacy API consent, PIPL data handling, common rejection reasons, wx.serviceMarket or msgSecCheck usage, and the first-submission pass-rate workflow.
description_zh: 微信小程序审核与合规
description_en: WeChat Mini Program Review & Compliance
disable: false
agent_created: true
---

# WeChat Mini Program Review & Compliance

## When to use

Trigger this skill when the user asks to:

- Prepare a Mini Program for submission to WeChat review.
- Configure domain whitelist (request / upload / download / socket) in the MP backend.
- Implement privacy authorization (Privacy API / `wx.requirePrivacyAuthorize`) before sensitive APIs.
- Handle personal information per PIPL (个人信息保护法) and WeChat privacy guidelines.
- Use content security APIs (`msgSecCheck`, `imgSecCheck`) for user-generated content.
- Diagnose and avoid common review rejections (location scope, payment category, private info, content).
- Write the privacy policy and declare `requiredPrivateInfos`.

## Core workflow

1. Whitelist all network domains (backend, mandatory).
   - Register request/upload/download/socket domains; only HTTPS is allowed.
   - During dev, `project.config.json` `urlCheck: false` disables checks locally, but production still requires whitelisting.
2. Declare permissions + private-info usage.
   - Add `permission` with a clear `desc` for each scope used (e.g. `scope.userLocation`).
   - Add `requiredPrivateInfos` for private APIs (getLocation, chooseLocation, chooseAddress, etc.).
   - The `desc` must describe a real, visible use case on the page — vague text triggers rejection.
3. Implement privacy consent before sensitive calls.
   - Use the Privacy API: show the privacy popup and call `wx.requirePrivacyAuthorize` before using `wx.getUserProfile`, location, etc.
   - Ship a privacy policy page and link it from the popup and the profile.
4. Handle personal data per PIPL.
   - Collect minimally; disclose purpose and retention; provide delete/withdraw paths.
   - Never log or transmit raw user identifiers to third parties without consent.
5. Moderate user-generated content.
   - Before publishing text/images, call `msgSecCheck` / `imgSecCheck` (cloud or server-side) — do not rely on client-only checks.
   - Provide report/block mechanisms for UGC.
6. Pre-submission checklist.
   - All domains whitelisted; permissions justified; privacy popup wired; policy page present; no placeholder/test content; category matches features; payment configured if selling.
   - See `references/review-checklist.md` for the full list and common rejection fixes.

## Critical constraints

- Domains must be HTTPS and whitelisted before any production request works.
- Sensitive scopes need a visible, justified use case or review rejects.
- Privacy API consent is required before private APIs (base library 2.27+).
- UGC must be content-secured (msgSecCheck/imgSecCheck) or the MP is at risk of takedown.
- Payment category must match the Mini Program service category.

## Output patterns

When submitting, produce the privacy/policy config, the domain list to whitelist, and the pre-submission checklist with pass/fail per item. When a rejection occurs, map the rejection reason to the matching fix in `references/review-checklist.md`.

## Pitfalls

- Don't whitelist `*` or localhost for production.
- Don't request `scope.userInfo` on load — it's deprecated and rejected; use `wx.getUserProfile` with consent, or phone/avatar components.
- Don't ship a privacy policy that doesn't match actual data use.
- Don't skip msgSecCheck for UGC "because it's small scale".
- Don't submit with test/placeholder copy or debug accounts visible.
