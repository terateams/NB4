# Branding assets

把自定义 logo 文件放在此目录下。

## 当前方案：覆盖左上角原生 Logo

`docker-compose.override.yml` 已配置将本目录的 `company-logo.svg` 挂载覆盖 NetBox 内置静态图片：

- 深色主题 → `/opt/netbox/netbox/static/logo_netbox_dark_teal.svg`
- 浅色主题 → `/opt/netbox/netbox/static/logo_netbox_bright_teal.svg`

## 替换 Logo

1. 将新 logo 覆盖本目录的 `company-logo.svg`。
2. 重启服务：`docker compose up -d --force-recreate netbox netbox-worker`。
3. 浏览器强制刷新（Cmd+Shift+R / Ctrl+Shift+R）清除缓存。
