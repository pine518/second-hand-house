# 第一阶段 MVP 开发计划书

项目：二手房数据爬取及可视化分析系统  
计划状态：待确认，确认前不进入代码构建  
参考文档：`docs/二手房数据爬取及可视化分析系统开发路线图.docx`

---

## 1. 第一阶段目标

第一阶段目标不是完成全部长期路线图，而是交付一个可本地部署、可运行、可访问使用的 MVP 版本。

系统需要跑通完整闭环：

```text
MySQL 初始化
  -> 基础爬虫采集
  -> 数据清洗
  -> 房源入库
  -> API 查询
  -> Jinja2 页面展示
  -> ECharts 图表分析
```

第一阶段完成后，用户应能够：

- 按 README 在本地完成安装、配置、数据库初始化与启动。
- 运行爬虫脚本采集单网站、单城市、少量页面的二手房数据。
- 通过浏览器访问系统首页、房源列表页、房源详情页、数据分析页。
- 在房源列表中分页浏览并按基础条件筛选。
- 查看区域均价、区域房源数量、价格区间、面积价格关系等图表。

---

## 2. 第一阶段范围

### 2.1 必须实现

- 项目基础结构与配置文件。
- FastAPI 应用启动入口。
- MySQL 8.0 连接配置。
- SQLAlchemy 模型：`House`、`CrawlLog`。
- 数据库初始化 SQL。
- Requests + BeautifulSoup 基础爬虫。
- 数据清洗服务。
- 房源数据入库、URL 去重、批量保存。
- 房源查询 API、详情 API。
- 基础分析 API。
- Jinja2 + Bootstrap 5 页面。
- 淡绿色、清新大气风格的系统界面。
- ECharts 图表。
- README 本地安装部署说明。
- 基础测试用例，覆盖清洗、CRUD、API、分析核心逻辑。

### 2.2 暂不实现

- 用户登录、权限系统。
- Docker、docker-compose。
- Redis、Celery、消息队列。
- 分布式爬虫。
- 多网站采集。
- Playwright 动态页面采集。
- Firecrawl 增强采集。
- Vue、React、Angular 等复杂前端框架。

这些能力放入后续阶段，避免第一阶段范围失控。

---

## 3. 技术方案

### 3.1 后端

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- Pydantic v2
- PyMySQL
- Jinja2
- python-dotenv

### 3.2 数据库

- MySQL 8.0
- 字符集：`utf8mb4`
- 存储引擎：`InnoDB`
- `house.source_url` 设置唯一索引，用于去重。

### 3.3 爬虫

- Requests
- BeautifulSoup4
- lxml

第一阶段只实现基础静态页面采集，保留 `BaseCrawler` 抽象，方便后续扩展 Scrapy、Playwright、Firecrawl。

### 3.4 数据分析

- Pandas
- NumPy
- SQLAlchemy 聚合查询

优先使用数据库聚合完成常规统计；Pandas 用于复杂清洗和补充分析。

### 3.5 前端页面

- Jinja2 Template Engine
- Bootstrap 5
- 原生 JavaScript
- ECharts

不引入 Vue、React、Angular。

---

## 4. 页面与视觉设计要求

### 4.1 页面结构

第一阶段页面包括：

- 首页：展示系统概览、核心指标、入口导航。
- 房源列表页：展示分页列表、筛选条件、关键字段。
- 房源详情页：展示单套房源完整信息。
- 数据分析页：展示 ECharts 图表和统计摘要。

### 4.2 风格要求

- 主色：淡绿色。
- 辅色：白色、浅灰、深绿色文本。
- 风格：清新、大气、简洁。
- 布局：顶部导航 + 内容区 + 统计卡片 + 图表区域。
- 控件：表单、按钮、卡片、分页样式统一。
- 响应式：桌面端优先，兼顾常见笔记本宽度。

### 4.3 交互要求

- 列表页支持城市、区域、价格区间、面积区间、户型筛选。
- 分页控件清晰可用。
- 图表数据来自后端 API，不使用硬编码假数据。
- 空数据时页面显示友好提示。
- API 或图表加载失败时显示错误提示。

---

## 5. 模块计划

### 5.1 项目初始化

交付文件：

- `requirements.txt`
- `.env.example`
- `main.py`
- `app/core/config.py`
- `app/core/logger.py`
- `app/core/database.py`

任务：

- 建立项目目录。
- 配置环境变量读取。
- 配置统一日志。
- 配置 FastAPI 应用与路由注册。
- 配置静态文件与模板目录。

验收标准：

- `uvicorn main:app --reload` 能启动。
- Swagger 文档可访问。
- 配置不硬编码数据库密码。

可复用性：

- `config.py` 统一管理所有配置，后续模块复用。

可测试性：

- 配置加载逻辑可独立测试。

说明文档：

- README 增加 Python 环境、依赖安装、`.env` 配置说明。

### 5.2 数据库建模与初始化

交付文件：

- `app/models/house.py`
- `app/models/crawl_log.py`
- `scripts/init_db.sql`

任务：

- 设计 `house` 表。
- 设计 `crawl_log` 表。
- 编写 SQLAlchemy 模型。
- 编写数据库初始化 SQL。
- 提供自动建表能力。

验收标准：

- 能连接 MySQL 8.0。
- 能创建核心表。
- `house.source_url` 存在唯一索引。

可复用性：

- 模型字段与后续 CRUD、API、分析模块共用。

可测试性：

- 可通过测试数据库验证建表、唯一索引和基础写入。

说明文档：

- README 增加数据库创建、初始化 SQL、连接配置说明。

### 5.3 基础爬虫 MVP

交付文件：

- `app/crawlers/base_crawler.py`
- `app/crawlers/requests_crawler.py`
- `scripts/run_crawler.py`

任务：

- 定义爬虫统一返回结构。
- 支持请求头配置。
- 支持分页采集。
- 支持请求间隔。
- 支持异常重试。
- 支持采集日志。
- 采集标题、城市、区域、小区、总价、单价、面积、户型、楼层、朝向、装修、建筑年代、来源 URL。

验收标准：

- 能采集至少 100 条房源数据。
- 单条解析异常不影响整体任务。
- 请求频率可配置。
- 爬虫异常写入日志。

可复用性：

- `BaseCrawler` 保留统一接口，后续 Playwright、Firecrawl 可复用清洗和入库流程。

可测试性：

- 解析逻辑可用本地 HTML 样例测试。

说明文档：

- README 增加爬虫运行命令、采集目标配置、注意事项。

### 5.4 数据清洗与入库

交付文件：

- `app/services/clean_service.py`
- `app/crud/house_crud.py`

任务：

- 清洗总价、单价、面积。
- 解析户型为室、厅数量。
- 解析楼层和建筑年代。
- 处理空值和异常值。
- 基于 `source_url` 去重。
- 支持批量插入和已有数据更新。

验收标准：

- `total_price`、`unit_price`、`area` 为数值。
- `room_count`、`hall_count` 可解析。
- 重复 URL 不重复入库。
- 异常数据不会导致整批任务失败。

可复用性：

- 清洗服务不绑定具体爬虫，任何爬虫输出统一数据结构后均可复用。

可测试性：

- 覆盖价格、面积、户型、年代、异常值测试。

说明文档：

- README 简述数据清洗规则。

### 5.5 后端 API

交付文件：

- `app/schemas/house_schema.py`
- `app/routers/api_router.py`
- `app/routers/analysis_router.py`
- `app/services/analysis_service.py`

任务：

- `GET /api/houses`
- `GET /api/houses/{id}`
- `GET /api/analysis/avg-price-by-district`
- `GET /api/analysis/count-by-district`
- `GET /api/analysis/price-range`
- `GET /api/analysis/area-price-scatter`
- 支持城市、区域、总价区间、面积区间、户型、页码、每页数量筛选。

验收标准：

- API 返回 JSON。
- 支持分页。
- 支持基础筛选。
- 分析接口返回 ECharts 可直接使用的数据格式。
- Swagger 文档可访问。

可复用性：

- 查询条件封装为可复用函数，页面和 API 共用。

可测试性：

- API 使用测试客户端验证状态码、返回结构、分页逻辑。

说明文档：

- README 增加 API 文档入口说明。

### 5.6 页面开发

交付文件：

- `app/routers/page_router.py`
- `app/templates/base.html`
- `app/templates/index.html`
- `app/templates/house_list.html`
- `app/templates/house_detail.html`
- `app/templates/analysis.html`
- `app/static/css/style.css`

任务：

- 创建统一基础模板。
- 实现首页、列表页、详情页、分析页。
- 列表页支持筛选和分页。
- 详情页展示完整字段。
- 应用淡绿色清新视觉风格。

验收标准：

- 浏览器可访问页面。
- 页面无明显错位。
- 筛选、分页、详情跳转可用。
- 空数据状态可读。

可复用性：

- `base.html`、导航、卡片、筛选表单样式可复用。

可测试性：

- 页面路由可用测试客户端验证状态码和关键内容。

说明文档：

- README 增加访问地址和页面功能说明。

### 5.7 ECharts 图表

交付文件：

- `app/static/js/charts.js`
- `app/static/js/analysis.js`

任务：

- 区域均价柱状图。
- 区域房源数量饼图。
- 总价区间分布图。
- 面积与总价散点图。
- 可选房价趋势折线图，若第一阶段数据缺少时间维度则仅保留接口和页面占位说明。

验收标准：

- 图表正常渲染。
- 图表数据来自数据库。
- 图表可随筛选条件更新。
- 无硬编码假数据。

可复用性：

- 图表初始化、加载、错误处理封装为通用方法。

可测试性：

- 后端分析接口可测试；前端通过浏览器手工验收。

说明文档：

- README 增加图表功能说明。

### 5.8 README 安装部署说明

交付文件：

- `README.md`

必须包含：

- 项目简介。
- 技术栈。
- 目录结构。
- Python 版本要求。
- MySQL 8.0 安装与数据库创建说明。
- `.env` 配置说明。
- 依赖安装命令。
- 数据库初始化命令。
- 启动 Web 系统命令。
- 运行爬虫命令。
- 页面访问地址。
- API 文档地址。
- 常见问题与排查方式。

验收标准：

- 新用户按 README 能完成本地部署。
- 本地可访问 Web 页面。
- 能运行爬虫并看到数据展示。

---

## 6. 第一阶段实施顺序

1. 初始化目录、依赖、环境变量、日志和 FastAPI 启动入口。
2. 实现 MySQL 配置、SQLAlchemy 连接、核心模型和初始化 SQL。
3. 实现基础爬虫抽象和 Requests 爬虫。
4. 实现数据清洗服务和房源 CRUD。
5. 实现爬虫运行脚本，完成采集、清洗、入库闭环。
6. 实现房源查询 API 和分析 API。
7. 实现 Jinja2 页面、淡绿色主题样式、房源列表和详情。
8. 实现 ECharts 图表和分析页面。
9. 补充基础测试。
10. 完善 README 安装部署说明。
11. 进行本地联调和问题修复。

---

## 7. 验收清单

### 7.1 功能验收

- FastAPI 服务可启动。
- MySQL 可连接。
- 数据表可初始化。
- 爬虫可运行。
- 房源可清洗并入库。
- 房源列表可访问。
- 房源详情可访问。
- 房源列表支持分页和基础筛选。
- 分析 API 可返回数据。
- ECharts 图表可渲染。
- README 可指导本地部署运行。

### 7.2 质量验收

- 代码符合 PEP8。
- 不使用 `print()` 作为业务日志。
- 配置不硬编码。
- 所有数据库操作通过 SQLAlchemy。
- 异常有捕获和日志。
- 模块边界清晰，`main.py` 不堆积业务逻辑。

### 7.3 测试验收

- 清洗服务测试通过。
- CRUD 基础测试通过。
- API 查询测试通过。
- 分析服务测试通过。

---

## 8. 执行风险与错误提示

### 8.1 爬虫合规风险

目标网站可能有反爬、访问频率限制或 robots 规则。第一阶段需要控制请求间隔、设置合理 User-Agent，并避免高频采集。

### 8.2 页面结构变化风险

目标网站 HTML 结构可能变化，导致解析失败。需要将解析逻辑集中在爬虫模块，并用日志记录失败 URL。

### 8.3 MySQL 环境风险

本地 MySQL 版本、字符集、账号权限、端口配置可能导致连接失败。README 需要提供明确排查步骤。

### 8.4 数据质量风险

房源字段可能缺失、格式不统一或存在异常价格。清洗服务必须容错，不能让单条异常数据中断整批入库。

### 8.5 图表数据不足风险

如果初始采集数据量较少，部分图表展示效果可能不明显。第一阶段仍保证图表可用，后续通过增加采集量优化分析价值。

### 8.6 本地部署差异风险

Windows PowerShell、Python 版本、依赖安装源、MySQL 权限均可能影响部署。README 需要写清楚命令和常见错误。

---

## 9. 第一阶段不做的决策说明

- 不使用 Docker：第一阶段优先保证本地直接运行，降低构建复杂度。
- 不使用 Redis：MVP 使用 MySQL 唯一索引完成 URL 去重。
- 不使用 Playwright：先验证静态页面采集闭环，动态采集后续扩展。
- 不使用 Firecrawl：只作为后期增强，不作为基础采集依赖。
- 不引入前端框架：Jinja2 + Bootstrap + ECharts 足够满足第一阶段页面展示。

---

## 10. 确认后产出物

确认本计划后，将按顺序构建以下内容：

```text
requirements.txt
.env.example
README.md
main.py
app/core/
app/models/
app/schemas/
app/crud/
app/routers/
app/services/
app/crawlers/
app/templates/
app/static/
scripts/
tests/
```

---

## 11. 下一步

1. 用户确认本 `PLAN.md` 是否作为第一阶段执行计划。
2. 如需调整，先修改范围、页面风格或验收标准。
3. 确认后开始构建第一阶段 MVP，不再扩展第二阶段能力。
