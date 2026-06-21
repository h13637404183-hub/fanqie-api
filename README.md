# 番茄小说 API (FanQie Novel API)

> **非官方 API 封装服务** | 仅供学习研究使用

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## 项目简介

本项目是一个基于 Python/Flask 的番茄小说 API 封装服务，通过逆向分析番茄小说网站公开的 PC 端 API 和网页结构，提供统一的 RESTful API 接口。

**数据来源**: [番茄小说官网](https://fanqienovel.com)

## 功能特性

- 获取热门书籍列表
- 获取推荐书籍列表（男/女生）
- 获取分类榜单（完结榜、阅读榜、新书榜）
- 获取最近更新书籍
- 获取 Banner 列表
- 获取书籍详情和章节列表
- 获取章节内容
- 支持 Docker 部署
- 跨域支持 (CORS)

## 技术栈

- Python 3.8+
- Flask 2.3+
- Flask-CORS
- lxml (HTML 解析)
- Gunicorn (生产环境)

## 快速开始

### 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/h13637404183-hub/fanqie-api.git
cd fanqie-api

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python app.py
```

服务将在 `http://localhost:5000` 启动。

### Docker 部署

```bash
# 构建镜像
docker build -t fanqie-api .

# 运行容器
docker run -d -p 5000:5000 --name fanqie-api fanqie-api
```

### Docker Compose

```bash
docker-compose up -d
```

## API 文档

### 基础信息

- **Base URL**: `http://localhost:5000`
- **Response Format**: `application/json`
- **CORS**: 已启用，支持所有来源

### 接口列表

#### 1. 获取热门书籍

```
GET /api/books/top
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | int | 否 | 返回数量，默认 20 |
| offset | int | 否 | 分页偏移量，默认 0 |

**示例**:

```bash
curl "http://localhost:5000/api/books/top?limit=10&offset=0"
```

---

#### 2. 获取推荐书籍

```
GET /api/books/recommend
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | int | 否 | 2=男生推荐, 3=女生推荐，默认 2 |
| limit | int | 否 | 返回数量，默认 10 |
| offset | int | 否 | 分页偏移量，默认 0 |

---

#### 3. 获取分类榜单

```
GET /api/books/rank
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category_id | int | 否 | 分类 ID，默认 1 |
| gender | int | 否 | 1=男频, 2=女频，默认 1 |
| rank_mold | int | 否 | 1=完结榜, 2=阅读榜, 3=新书榜，默认 2 |
| limit | int | 否 | 返回数量，默认 20 |
| offset | int | 否 | 分页偏移量，默认 0 |

---

#### 4. 获取最近更新

```
GET /api/books/recent
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | int | 否 | 返回数量，默认 20 |
| offset | int | 否 | 分页偏移量，默认 0 |

---

#### 5. 获取 Banner 列表

```
GET /api/books/banner
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| location | int | 否 | Banner 位置，默认 1 |

---

#### 6. 获取书籍详情

```
GET /api/book/{book_id}
```

**路径参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| book_id | string | 是 | 书籍 ID |

**返回字段**:

- `book_id`: 书籍 ID
- `title`: 书名
- `author`: 作者
- `cover`: 封面图片 URL
- `category`: 分类
- `status`: 连载状态
- `abstract`: 简介
- `word_count`: 字数
- `chapters`: 章节列表

---

#### 7. 获取章节内容

```
GET /api/chapter/{chapter_id}
```

**路径参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| chapter_id | string | 是 | 章节 ID |

**返回字段**:

- `chapter_id`: 章节 ID
- `title`: 章节标题
- `content`: 章节正文
- `word_count`: 字数

---

#### 8. 搜索书籍

```
GET /api/search?q={keyword}
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 搜索关键词 |
| page | int | 否 | 页码，默认 1 |

> **注意**: 搜索功能需要移动端 API 签名，当前版本返回提示信息。建议通过已知书籍 ID 访问详情。

## 响应示例

### 热门书籍

```json
{
  "book_list": [
    {
      "author": "作者名",
      "book_id": "7276384138653862966",
      "book_name": "书名",
      "category": "都市脑洞",
      "creation_status": 0,
      "thumb_url": "https://..."
    }
  ],
  "code": 0,
  "message": "ok"
}
```

### 书籍详情

```json
{
  "book_id": "7143038691944959011",
  "title": "十日终焉",
  "author": "杀虫队队员",
  "cover": "https://...",
  "category": "悬疑脑洞",
  "status": "连载中",
  "abstract": "简介内容...",
  "word_count": "359.6万字",
  "chapters": [
    {
      "chapter_id": "7143038691944959012",
      "title": "第1章 骗经"
    }
  ]
}
```

### 章节内容

```json
{
  "chapter_id": "7143038691944959012",
  "title": "第1章 骗经",
  "content": "章节正文内容...",
  "word_count": 2048
}
```

## 注意事项

1. **版权提醒**: 本项目仅供学习研究使用，请尊重原作者版权，通过正规渠道支持创作者。
2. **免责声明**: 本项目不对数据的完整性、时效性及合法性做任何保证。
3. **请求限制**: 请合理控制请求频率，避免对番茄小说服务器造成压力。
4. **搜索限制**: 移动端搜索 API 需要字节跳动的签名参数（msToken、a_bogus），当前版本暂未实现签名生成，搜索功能受限。

## 项目结构

```
fanqie-api/
├── app.py              # Flask 应用入口
├── fanqie_api.py       # 核心 API 客户端
├── requirements.txt    # Python 依赖
├── Dockerfile          # Docker 构建文件
├── docker-compose.yml  # Docker Compose 配置
├── README.md           # 项目文档
└── LICENSE             # 许可证
```

## 技术实现

### 数据来源

| 功能 | 实现方式 | 说明 |
|------|----------|------|
| 热门书籍 | PC 端公开 API | 无需签名 |
| 推荐列表 | PC 端公开 API | 无需签名 |
| 分类榜单 | PC 端公开 API | 无需签名 |
| 书籍详情 | 网页 HTML 解析 | 解析 JSON-LD + DOM |
| 章节列表 | 网页 HTML 解析 | 解析 DOM 结构 |
| 章节内容 | API + 网页解析 | 带 Cookie 访问 |

### 反爬处理

- 使用浏览器 User-Agent
- 模拟正确的 Referer
- 随机生成 `novel_web_id` Cookie
- 请求超时控制
- 异常处理与降级

## 开发计划

- [ ] 实现移动端 API 签名生成
- [ ] 完善搜索功能
- [ ] 添加缓存机制 (Redis)
- [ ] 添加速率限制
- [ ] 添加 API 认证
- [ ] 支持批量内容获取
- [ ] 支持听书/音频接口

## 贡献指南

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT License

## 致谢

- [番茄小说](https://fanqienovel.com) - 数据来源
- [PyFQWeb](https://github.com/MeoProject/PyFQWeb) - 接口参考
- [fanqienovel-downloader](https://github.com/ying-ck/fanqienovel-downloader) - 实现参考

---

> **声明**: 本项目与番茄小说官方无任何关联，所有数据版权归原平台所有。
