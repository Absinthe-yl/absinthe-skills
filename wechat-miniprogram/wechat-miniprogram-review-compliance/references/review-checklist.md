# Review checklist + common rejections

## Pre-submission checklist

- [ ] All request/upload/download/socket domains whitelisted (HTTPS only).
- [ ] `permission` scopes declared with clear, truthful `desc`.
- [ ] `requiredPrivateInfos` lists every private API actually used.
- [ ] Privacy popup wired via `wx.requirePrivacyAuthorize`; privacy policy page exists and is reachable.
- [ ] Personal data collected minimally; retention/disclosure documented (PIPL).
- [ ] UGC flows call `msgSecCheck`/`imgSecCheck` before publish.
- [ ] Service category matches features (esp. if accepting payment).
- [ ] WeChat Pay configured with correct category if selling goods/services.
- [ ] No placeholder/test content, no debug accounts or internal URLs visible.
- [ ] `sitemap.json` correct (or intentionally closed for non-indexed pages).
- [ ] Main package < 2MB; subpackages within limits.

## Common rejection reasons → fix

| Rejection | Cause | Fix |
|---|---|---|
| 位置信息接口未说明用途 | `scope.userLocation` without visible use | Add `permission.scope.userLocation.desc` tied to a real map/nearby feature |
| 隐私接口未授权 | Called private API before consent | Integrate Privacy API popup; gate the call on `requirePrivacyAuthorize` |
| 类目与功能不符 | Selling without retail/paid category | Apply correct service category; configure WeChat Pay |
| 内容安全风险 | UGC not moderated | Add `msgSecCheck`/`imgSecCheck` server-side; add report flow |
| 诱导分享 | Forced share for rewards | Remove mandatory-share gating; sharing must be voluntary |
| 账号信息不完整 | Missing contact/qualification | Complete MP profile, upload licenses if required |
| 虚拟支付违规 | Paid digital content without rules | Use allowed models; don't sell virtual goods outside policy |

## Privacy API minimal wiring

```javascript
// app.js onLaunch
wx.getPrivacySetting({
  success: (res) => {
    if (res.needAuthorization) {
      wx.requirePrivacyAuthorize({
        success: () => { /* proceed with private APIs */ },
        fail: () => { /* guide user to settings */ },
      });
    }
  },
});
```

## Content security (server-side, pseudocode)

```
POST https://api.weixin.qq.com/wxa/msg_sec_check?access_token=TOKEN
{ "content": "<user text>", "version": 2, "scene": 1 }
// response: errcode 0 = ok, 87014 = risky -> reject publish
```
