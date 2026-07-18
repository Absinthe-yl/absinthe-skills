# utils/request.js — unified network wrapper

```javascript
const BASE_URL = 'https://api.example.com/miniapp/v1';

const request = (options) => {
  return new Promise((resolve, reject) => {
    const token = wx.getStorageSync('access_token');
    wx.request({
      url: `${BASE_URL}${options.url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
        ...options.header,
      },
      success: (res) => {
        if (res.statusCode === 401) {
          return refreshTokenAndRetry(options).then(resolve).catch(reject);
        }
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject({ code: res.statusCode, message: res.data.message || 'Request failed' });
        }
      },
      fail: (err) => {
        reject({ code: -1, message: 'Network error', detail: err });
      },
    });
  });
};

let refreshing = null;
function refreshTokenAndRetry(options) {
  if (!refreshing) {
    refreshing = doRefresh().catch((e) => { refreshing = null; throw e; });
  }
  return refreshing.then(() => request(options));
}

function doRefresh() {
  const refreshToken = wx.getStorageSync('refresh_token');
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${BASE_URL}/auth/refresh`,
      method: 'POST',
      data: { refresh_token: refreshToken },
      success: (res) => {
        if (res.statusCode === 200) {
          wx.setStorageSync('access_token', res.data.access_token);
          resolve(res.data);
        } else {
          // Force re-login
          wx.removeStorageSync('access_token');
          reject(res.data);
        }
      },
      fail: reject,
    });
  });
}

module.exports = { request };
```

# utils/auth.js — login + session

```javascript
const { request } = require('./request');

const login = async () => {
  const { code } = await wx.login();
  const { data } = await request({
    url: '/auth/wechat-login',
    method: 'POST',
    data: { code },
  });
  wx.setStorageSync('access_token', data.access_token);
  wx.setStorageSync('refresh_token', data.refresh_token);
  return data.user;
};

module.exports = { login };
```

## Rules

- HTTPS only; domain must be whitelisted in MP backend.
- Centralize token logic here; never inline `wx.getStorageSync('access_token')` in pages.
- `refreshing` guard prevents concurrent refresh storms on 401.
