# 二手房数据爬取及可视化分析系统

基于 Python + FastAPI + MySQL 的二手房数据采集、清洗、存储、分析与可视化展示系统。

当前版本为第一阶段 MVP，目标是先跑通本地闭环：爬虫采集或样例数据写入、清洗入库、API 查询、页面展示、ECharts 图表分析。

## 技术栈

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- Pydantic v2
- MySQL 8.0
- PyMySQL
- Requests
- BeautifulSoup4
- Jinja2
- Bootstrap 5
- ECharts

## 目录结构

```text
second-hand-house/
├── app/
│   ├── core/          # 配置、数据库、日志
│   ├── models/        # SQLAlchemy 模型
│   ├── schemas/       # Pydantic 响应模型
│   ├── crud/          # 数据访问
│   ├── routers/       # 页面和 API 路由
│   ├── services/      # 清洗和分析服务
│   ├── crawlers/      # 爬虫模块
│   ├── templates/     # Jinja2 页面
│   └── static/        # CSS、JavaScript
├── scripts/
│   ├── init_db.sql
│   └── run_crawler.py
├── tests/
├── .env.example
├── main.py
├── requirements.txt
└── README.md
```

## 本地部署

### 1. 准备 Python 环境

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

如 PowerShell 阻止激活脚本，可临时执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 2. 准备 MySQL 8.0

登录 MySQL 后执行：

```sql
CREATE DATABASE second_hand_house
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

也可以直接执行初始化脚本：

```powershell
mysql -u root -p < scripts\init_db.sql
```

### 3. 配置环境变量

复制配置模板：

```powershell
Copy-Item .env.example .env
```

编辑 `.env`：

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=second_hand_house
DB_CHARSET=utf8mb4
```

爬虫目标地址可配置为带 `{page}` 的分页 URL：

```env
CRAWLER_BASE_URL=https://example.com/list?page={page}
CRAWLER_CITY=上海
```

如果暂时没有可采集目标，可先使用样例数据跑通本地系统。

### 4. 启动 Web 系统

```powershell
uvicorn main:app --reload
```

访问地址：

- 首页：http://127.0.0.1:8000/
- 房源列表：http://127.0.0.1:8000/houses
- 数据分析：http://127.0.0.1:8000/analysis
- API 文档：http://127.0.0.1:8000/docs

### 5. 运行爬虫

使用真实目标网站：

```powershell
python scripts\run_crawler.py --pages 5 --city 上海
```

使用本地样例数据验证完整闭环：

```powershell
python scripts\run_crawler.py --sample --city 上海
```

样例模式会写入 120 条确定性房源数据，用于验证列表、详情和图表页面。

## API

### 房源接口

- `GET /api/houses`
- `GET /api/houses/{house_id}`

支持查询参数：

- `city`
- `district`
- `min_price`
- `max_price`
- `min_area`
- `max_area`
- `room_count`
- `page`
- `page_size`

### 分析接口

- `GET /api/analysis/summary`
- `GET /api/analysis/avg-price-by-district`
- `GET /api/analysis/count-by-district`
- `GET /api/analysis/price-range`
- `GET /api/analysis/area-price-scatter`

分析接口返回 ECharts 可直接消费的数据结构。

## 数据清洗规则

- 总价统一为“万元”数值。
- 单价统一为“元/平”数值。
- 面积统一为平方米数值。
- 户型解析为 `room_count` 和 `hall_count`。
- 建筑年代解析为四位年份。
- 缺失标题或来源 URL 的数据会被跳过。
- `source_url` 唯一索引用于重复采集去重。

## 测试

```powershell
pytest
```

当前测试覆盖：

- 数据清洗。
- 样例数据结构。
- API 分页响应包装。
- 分析接口响应包装。

## 常见问题

### MySQL 连接失败

检查 `.env` 中的 `DB_HOST`、`DB_PORT`、`DB_USER`、`DB_PASSWORD`、`DB_NAME` 是否正确，并确认 MySQL 服务已启动。

### 启动时报表不存在

先执行：

```powershell
mysql -u root -p < scripts\init_db.sql
```

应用启动时也会尝试通过 SQLAlchemy 自动创建表。

### 没有房源数据

先运行：

```powershell
python scripts\run_crawler.py --sample --city 上海
```

再刷新 `/houses` 和 `/analysis`。

### 在线爬虫没有数据

目标网站 HTML 结构可能与默认解析规则不同。需要在 `app/crawlers/requests_crawler.py` 中按目标网站结构调整选择器。

### ECharts 无法加载

当前页面使用 CDN 加载 Bootstrap 和 ECharts。离线环境需要改成本地静态文件。

## 执行风险

- 目标网站可能存在 robots 规则、访问频率限制或反爬机制，必须控制请求频率。
- 页面结构变化会导致解析失败，需要通过日志定位失败页面。
- 本地 MySQL 权限、字符集或端口配置错误会导致系统无法启动。
- 首次数据量较少时，图表分析价值有限，但页面和接口应保持可用。

## 下一步

1. 配置 `.env` 并初始化 MySQL。
2. 使用 `python scripts\run_crawler.py --sample --city 上海` 写入样例数据。
3. 启动 `uvicorn main:app --reload` 后访问系统页面。
