# 番茄小说 API (PHP 7.4/8.0 兼容版)

> **非官方 API 封装服务** | 仅供学习研究使用

基于 PHP 7.4/8.0 的番茄小说 API 封装，支持字体解密（PUA → 真实文字）。

## 部署要求

- PHP >= 7.4（推荐 8.0+）
- curl 扩展
- mbstring 扩展
- Apache/Nginx + mod_rewrite

## 快速部署

```bash
git clone https://github.com/h13637404183-hub/fanqie-api.git
cd fanqie-api/php
```

将 `php/` 文件夹放到 Web 服务器目录（如 `/var/www/html/`）。

### Apache 重写

`.htaccess` 已包含，确保 `AllowOverride All` 已启用。

### Nginx 配置

```nginx
location / {
    try_files $uri $uri/ /index.php?$query_string;
}
```

## 接口列表

| 接口 | 端点 | 参数 |
|------|------|------|
| 热门书籍 | `GET /api/books/top` | `limit`, `offset` |
| 推荐书籍 | `GET /api/books/recommend` | `type`, `limit`, `offset` |
| 分类榜单 | `GET /api/books/rank` | `category_id`, `gender`, `rank_mold` |
| 最近更新 | `GET /api/books/recent` | `limit`, `offset` |
| Banner | `GET /api/books/banner` | `location` |
| 热门作者 | `GET /api/authors/top` | `limit`, `offset` |
| 书籍详情 | `GET /api/book/{book_id}` | — |
| 章节内容 | `GET /api/chapter/{chapter_id}` | — |
| 搜索 | `GET /api/search?q=` | `q`, `page` |

## 字体解密

章节内容自动检测并解密 PUA 字符，返回 `encrypted: true/false` 标识。

## 自定义 Cookie

修改 `config.php` 中的 `$cookie` 以使用你自己的有效 Cookie。

## 许可证

MIT License
