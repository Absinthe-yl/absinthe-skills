# Project Structure

```
.
├── app.js                 # App lifecycle + globalData
├── app.json               # Global config: pages, window, tabBar, subpackages, permission
├── app.wxss               # Global styles
├── project.config.json    # IDE + project settings (appid, compileType, etc.)
├── sitemap.json           # WeChat search index config
├── pages/
│   ├── index/             # Home (index.js/.json/.wxml/.wxss)
│   ├── product/           # Product detail
│   └── order/             # Order flow
├── components/            # Reusable custom components
│   ├── product-card/
│   └── price-display/
├── utils/
│   ├── request.js         # Unified network wrapper (auth + errors)
│   ├── auth.js            # Login + token management
│   └── analytics.js       # Event tracking
├── services/              # Business logic / API calls
└── subpackages/           # Subpackages for size management
    ├── user-center/
    └── marketing-pages/
```

## File responsibilities

- **app.js** — `App({ onLaunch, onShow, onHide, globalData })`. Boot once; put app-level init here.
- **app.json** — single source of route/style truth. Adding a page = add to `pages[]`.
- **utils/request.js** — every network call flows through here. Never call `wx.request` directly elsewhere.
- **utils/auth.js** — owns `login()`, `refreshToken()`, token storage keys.
- **services/** — domain functions (e.g. `services/payment.js`, `services/user.js`) built on `request`.
- **components/** — each is a self-contained folder with `.js/.json/.wxml/.wxss`.
