# Performance optimization patterns

## setData batching + path update

```javascript
// Bad: two bridge crossings
this.setData({ loading: false });
this.setData({ 'product.price': price });

// Good: one crossing, targeted path
this.setData({ loading: false, 'product.price': price });

// Trim payload — render only what's needed
this.setData({
  product: {
    id: p.id,
    title: p.title,
    price: p.price,
    images: p.images.slice(0, 5), // defer rest
  },
});
```

## Pure-data fields (no serialization to native for non-render state)

```javascript
Component({
  options: { pureDataPattern: /^_/ }, // fields starting with _ are pure
  data: { _scrollTop: 0, visible: true },
});
```

## Subpackage + preload

```json
// app.json
{
  "subpackages": [
    { "root": "subpackages/user-center", "pages": ["profile/profile"] }
  ],
  "preloadRule": {
    "pages/index/index": { "network": "all", "packages": ["subpackages/user-center"] }
  }
}
```

## Virtual list (recycle-view style)

```xml
<recycle-view batch="{{batchSetRecycleData}}" id="recycleId">
  <recycle-item wx:for="{{list}}" wx:key="id">{{item.title}}</recycle-item>
</recycle-view>
```

## Image lazy load

```xml
<image src="{{item.cover}}" lazy-load mode="aspectFill" />
```

## Request cache (TTL)

```javascript
function cachedGet(key, fetcher, ttl = 60000) {
  const hit = wx.getStorageSync(key);
  if (hit && Date.now() - hit.t < ttl) return Promise.resolve(hit.v);
  return fetcher().then((v) => { wx.setStorageSync(key, { t: Date.now(), v }); return v; });
}
```

## Audit targets

- Startup < 1.5s (mid Android), DevTools perf score > 90.
- Main package < 1.5MB target; hard limit 2MB. Total with subpackages ≤ 20MB.
- Crash rate < 0.1% across supported base libraries.
