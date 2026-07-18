# app.json templates

## Minimal

```json
{
  "pages": [
    "pages/index/index",
    "pages/product/product",
    "pages/order/order"
  ],
  "window": {
    "navigationBarTitleText": "小程序",
    "navigationBarBackgroundColor": "#ffffff",
    "navigationBarTextStyle": "black",
    "backgroundColor": "#f5f5f5"
  },
  "style": "v2",
  "sitemapLocation": "sitemap.json"
}
```

## With tabBar

```json
{
  "tabBar": {
    "color": "#999999",
    "selectedColor": "#07c160",
    "backgroundColor": "#ffffff",
    "list": [
      { "pagePath": "pages/index/index", "text": "首页", "iconPath": "assets/tab/home.png", "selectedIconPath": "assets/tab/home-active.png" },
      { "pagePath": "pages/order/order", "text": "订单", "iconPath": "assets/tab/order.png", "selectedIconPath": "assets/tab/order-active.png" }
    ]
  }
}
```

## With subpackages + permission (location example)

```json
{
  "pages": ["pages/index/index", "pages/product/product"],
  "subpackages": [
    { "root": "subpackages/user-center", "pages": ["profile/profile", "address/address"] },
    { "root": "subpackages/marketing-pages", "pages": ["activity/activity"] }
  ],
  "preloadRule": {
    "pages/index/index": { "network": "all", "packages": ["subpackages/user-center"] }
  },
  "permission": {
    "scope.userLocation": { "desc": "用于在地图上展示你的位置" }
  },
  "requiredPrivateInfos": ["getLocation", "chooseLocation"]
}
```

## Notes

- `preloadRule` warms subpackages on a designated entry page to cut first-open delay.
- `requiredPrivateInfos` is mandatory for private APIs since base library 2.27+; omitting it triggers review rejection.
- Order of `pages[0]` is the launch page.
