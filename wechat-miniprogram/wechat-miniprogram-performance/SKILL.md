---
name: wechat-miniprogram-performance
description: This skill should be used when optimizing WeChat Mini Program (微信小程序) performance: startup time, rendering, setData efficiency, package size and subpackage strategy, image/network optimization, and virtual lists. Trigger it when diagnosing slow first-open, janky scroll, large setData payloads, main-package over-size, or low WeChat DevTools audit scores.
description_zh: 微信小程序性能优化
description_en: WeChat Mini Program Performance
disable: false
agent_created: true
---

# WeChat Mini Program Performance

## When to use

Trigger this skill when the user asks to:

- Reduce Mini Program startup time (target < 1.5s on mid-range Android).
- Optimize `setData` calls (frequency, payload size, path updates).
- Plan main-package vs subpackage sizing (main < 2MB, total < 20MB).
- Optimize images (CDN, WebP, lazy load, sizing).
- Add request caching, prefetch, or offline resilience.
- Implement virtual lists / long-list rendering.
- Use pure-data fields, `observers`, or worklet (Skyline) animations.

## Core workflow

1. Optimize startup.
   - Keep the main package lean; move non-entry pages to subpackages.
   - Defer non-critical init (analytics, third-party SDKs) until after first render.
   - Use `preloadRule` to warm likely-next subpackages.
2. Optimize `setData`.
   - Every `setData` crosses the JS↔native bridge; batch multiple updates into one call.
   - Patch only changed fields using path syntax: `this.setData({ 'product.price': newPrice })` instead of the whole object.
   - Trim payloads: send only what the view renders (slice arrays, drop unused fields).
   - Avoid `setData` inside `onScroll`/`onTouchMove` hot paths; throttle or use pure-data fields.
3. Manage package size.
   - Audit with `WeChat DevTools → 代码依赖分析`. Remove unused npm packages.
   - Prefer CDN for large static assets over bundling them.
   - Use subpackages + `preloadRule`; consider independent subpackages if they don't share code.
4. Optimize images.
   - Serve from CDN with WebP; request appropriately sized variants (don't download 2000px for a 200px view).
   - Lazy-load below-the-fold images (`lazy-load` on `<image>`); fade-in placeholders.
5. Optimize network.
   - Cache GET responses (storage with TTL); prefetch list data when entering a page likely to need it.
   - Show cached content instantly, then update — don't blank the screen waiting on network.
6. Render long lists.
   - Use `recycle-view` / `virtual-list` for lists > 100 items; never render thousands of nodes at once.
   - For WebView renderer: throttle scroll-driven `setData`.

## Critical constraints

- `setData` is the most expensive common operation — treat it as a scarce resource.
- Main package > 2MB blocks upload; plan subpackages before adding features.
- No DOM access; pure-data fields (`options.pureDataPattern`) avoid setData serialization cost for non-render data.
- Skyline renderer enables worklet animations off the main JS thread — prefer it for gesture-heavy UIs.

## Output patterns

When optimizing, give a concrete change (e.g. "replace this setData with a path update", "move X to subpackage Y") plus the expected metric impact. When auditing, reference the DevTools performance score (>90 target).

## Pitfalls

- Don't `setData` the entire `data` object on every change.
- Don't render huge lists without virtualization.
- Don't bundle large assets in the main package.
- Don't block first paint on analytics/SDK init.
- Don't setData inside scroll/touch handlers without throttling.
