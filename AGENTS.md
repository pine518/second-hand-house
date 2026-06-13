# AGENTS.md

# 二手房数据爬取及可视化分析系统（Second-Hand House Analysis System）

---

## 1. 项目目标（Project Goal）

使用 Python 开发一个完整的二手房数据采集、清洗、存储、分析与可视化展示系统。

系统需要完成：

* 采集二手房网站公开房源数据
* 数据清洗与标准化处理
* 存储至 MySQL 8.0 数据库
* 对房价数据进行统计分析
* 提供 Web 页面进行数据展示
* 提供可视化图表分析房价趋势

本项目采用 **MVP（Minimum Viable Product）优先开发策略**。

第一阶段先保证系统可运行，再逐步扩展功能。

---

# 2. 技术架构（Technology Stack）

## 后端框架

必须使用：

* Python 3.11+
* FastAPI
* Uvicorn
* SQLAlchemy 2.x
* Pydantic v2
* Jinja2

禁止使用：

* Django
* Flask（除非特殊说明）

原因：

* 项目需要 API + 页面渲染
* FastAPI 性能更好
* 更适合 AI Agent 自动生成代码

---

## 数据库

固定使用：

* MySQL 8.0

数据库驱动：

* PyMySQL

ORM：

* SQLAlchemy

迁移工具：

* Alembic（可选）

禁止：

* SQLite
* PostgreSQL
* MongoDB

除非用户明确要求修改。

---

## 爬虫技术栈（Crawler Stack）

采用分层策略。

### 方案一：基础爬虫（默认方案）

优先使用：

* Requests
* BeautifulSoup4
* lxml

适用于：

* 静态网页
* HTML 页面解析
* MVP 阶段开发

---

### 方案二：工程化爬虫（可选）

可使用：

* Scrapy

适用于：

* 多页面采集
* 大规模数据采集
* 分布式采集

---

### 方案三：动态页面采集（可选）

优先：

* Playwright

备用：

* Selenium

适用于：

* JavaScript 渲染页面
* 异步加载页面
* SPA 单页面应用

---

### 方案四：AI 爬虫增强（可选）

允许使用：

* Firecrawl

官方：

* [Firecrawl Official Website](https://www.firecrawl.dev?utm_source=chatgpt.com)

用途：

* 网页内容自动提取
* 自动转换 Markdown
* JSON 结构化提取
* AI Agent 自动解析网页内容

注意：

Firecrawl 仅作为增强模块。

禁止将 Firecrawl 作为唯一爬虫方案。

优先级：

Requests > BeautifulSoup > Scrapy > Playwright > Firecrawl

环境变量：

```env
FIRECRAWL_API_KEY=your_api_key
```

---

## 数据分析

使用：

* Pandas
* NumPy

用于：

* 房价统计
* 数据聚合
* 数据清洗
* 数据透视分析

---

## 可视化

前端图表：

* ECharts

Python图表（可选）：

* Pyecharts
* Matplotlib

禁止：

* Plotly（非必要不要引入）

---

## 前端技术

使用：

* HTML5
* CSS3
* JavaScript
* Bootstrap 5
* Jinja2 Template Engine

禁止：

* Vue
* React
* Angular

第一阶段不允许引入复杂前端框架。

---

# 3. 项目目录结构

```text
second_hand_house/

├── AGENTS.md
├── README.md
├── requirements.txt
├── .env.example
├── main.py

├── app/

│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── logger.py

│   ├── models/
│   │   ├── house.py
│   │   └── crawl_log.py

│   ├── schemas/
│   │   └── house_schema.py

│   ├── crud/
│   │   └── house_crud.py

│   ├── routers/
│   │   ├── page_router.py
│   │   ├── api_router.py
│   │   └── analysis_router.py

│   ├── services/
│   │   ├── analysis_service.py
│   │   ├── clean_service.py
│   │   └── chart_service.py

│   ├── crawlers/
│   │   ├── base_crawler.py
│   │   ├── requests_crawler.py
│   │   ├── scrapy_crawler.py
│   │   ├── playwright_crawler.py
│   │   └── firecrawl_crawler.py

│   ├── templates/
│   │   ├── index.html
│   │   ├── house_list.html
│   │   └── analysis.html

│   └── static/
│       ├── css/
│       ├── js/
│       └── images/

├── scripts/
│   ├── init_db.sql
│   └── run_crawler.py

└── tests/
    └── test_house.py
```

---

# 4. 核心功能模块

必须实现：

## 数据采集模块

功能：

* 房源列表采集
* 房源详情采集
* 分页采集
* 请求频率控制
* 数据去重
* 异常重试
* 日志记录

---

## 数据清洗模块

功能：

* 价格格式统一
* 面积格式统一
* 户型解析
* 楼层解析
* 去除空值
* 去除异常数据

---

## 数据存储模块

功能：

* 保存 MySQL 8.0
* URL 去重
* 批量插入
* 数据更新

---

## 数据分析模块

必须实现：

* 区域均价分析
* 房源数量统计
* 面积区间统计
* 户型价格统计
* 单价排序分析
* 总价区间统计

---

## 可视化模块

必须实现：

* 区域均价柱状图
* 房源数量饼图
* 面积与价格散点图
* 房价趋势折线图

使用：

* ECharts

---

# 5. 数据库规范

固定：

* MySQL 8.0

字符集：

```sql
utf8mb4
```

存储引擎：

```sql
InnoDB
```

---

必须包含数据表：

## house 表

字段：

* id
* title
* city
* district
* community
* total_price
* unit_price
* area
* room_count
* hall_count
* floor
* orientation
* decoration
* build_year
* source_url
* crawl_time
* created_at

source_url 必须唯一索引。

---

## crawl_log 表

字段：

* task_name
* start_time
* end_time
* success_count
* fail_count
* status
* error_message

---

# 6. 开发原则（Important Rules）

AI Agent 必须遵守。

## 原则 1

优先实现 MVP。

禁止一次生成复杂系统。

---

## 原则 2

先开发后端。

顺序：

```text
数据库 → 爬虫 → API → 页面 → 图表
```

禁止直接开发前端页面。

---

## 原则 3

所有配置必须放入：

```text
.env
```

禁止：

```python
password="123456"
```

硬编码。

---

## 原则 4

代码必须模块化。

禁止：

```text
main.py 写 3000 行代码
```

---

## 原则 5

每个模块单独开发。

禁止一次生成整个项目。

推荐：

* 先数据库
* 再爬虫
* 再数据清洗
* 再 API
* 再前端

---

## 原则 6

所有异常必须处理。

例如：

```python
try:
    ...
except Exception:
    ...
```

禁止忽略异常。

---

## 原则 7

必须写日志。

统一使用：

```text
logging
```

禁止：

```python
print()
```

---

# 7. requirements.txt

```txt
fastapi
uvicorn
sqlalchemy
pymysql
jinja2
python-dotenv

requests
beautifulsoup4
lxml

scrapy

playwright

firecrawl-py

pandas
numpy

pyecharts
matplotlib

pytest
```

---

# 8. 开发阶段

## Phase 1

项目初始化

---

## Phase 2

数据库建模

---

## Phase 3

基础爬虫开发（Requests）

---

## Phase 4

数据清洗与入库

---

## Phase 5

API 开发

---

## Phase 6

页面开发

---

## Phase 7

ECharts 图表开发

---

## Phase 8

增加 Firecrawl 增强爬虫

---

# 9. AI Agent Coding Rules

AI 编码助手必须遵守：

* 不允许擅自修改数据库类型
* 不允许引入大型前端框架
* 不允许一次生成整个项目代码
* 每次修改必须说明改动原因
* 代码必须符合 PEP8
* 每个模块代码独立
* 所有函数必须添加注释
* 所有 SQL 操作必须通过 SQLAlchemy
* 先实现 MVP 再扩展功能

---

# 10. 当前 MVP 范围

第一阶段只实现：

* 单网站采集
* 房源数据入库
* 房源列表展示
* 区域均价统计
* 房源数量统计
* ECharts 图表展示

禁止开发：

* 用户系统
* Docker
* 微服务
* Redis
* Celery
* 消息队列
* 分布式爬虫

全部放到第二阶段。

---
