# GlobalMarketHalt

全球股市盘前停牌信息爬取系统

## 项目简介

GlobalMarketHalt 是一个专门用于爬取和监控不同国家股市盘前停牌信息的系统。该系统支持多个主要股票市场，包括美股、港股、A股等，提供实时的停牌信息获取、存储和分析功能。

## 功能特性

- 🌍 **多市场支持**：支持美股、港股、A股、日股、欧股等主要市场
- ⏰ **实时监控**：盘前实时获取停牌信息
- 📊 **数据存储**：支持多种数据库存储（MySQL、PostgreSQL、MongoDB）
- 🔔 **通知提醒**：支持邮件、钉钉、企业微信等通知方式
- 📈 **数据分析**：提供停牌数据统计和分析功能
- 🛡️ **反爬虫处理**：智能处理反爬虫机制
- 🔄 **定时任务**：支持定时爬取和更新

## 支持的市场

- **美股**：NYSE、NASDAQ
- **港股**：港交所
- **A股**：上交所、深交所
- **日股**：东京证券交易所
- **欧股**：伦敦证券交易所、法兰克福证券交易所

## 技术栈

- **Python 3.8+**
- **Scrapy** - 爬虫框架
- **Selenium** - 动态页面处理
- **BeautifulSoup** - HTML解析
- **SQLAlchemy** - 数据库ORM
- **FastAPI** - API服务
- **Celery** - 异步任务队列
- **Redis** - 缓存和消息队列

## 项目结构

```
GlobalMarketHalt/
├── src/                    # 源代码目录
│   ├── crawlers/          # 爬虫模块
│   ├── parsers/           # 数据解析模块
│   ├── models/            # 数据模型
│   ├── services/          # 业务逻辑服务
│   ├── api/               # API接口
│   └── utils/             # 工具函数
├── config/                # 配置文件
├── data/                  # 数据存储
├── logs/                  # 日志文件
├── tests/                 # 测试文件
├── docs/                  # 文档
├── requirements.txt       # 依赖包
├── docker-compose.yml     # Docker配置
└── README.md             # 项目说明
```

## 快速开始

### 环境要求

- Python 3.8+
- Redis
- MySQL/PostgreSQL (可选)

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd GlobalMarketHalt
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp config/config.example.yaml config/config.yaml
# 编辑配置文件
```

5. 启动服务
```bash
python src/main.py
```

## 使用说明

### 基本使用

```python
from src.crawlers.us_market import USMarketCrawler
from src.crawlers.hk_market import HKMarketCrawler

# 爬取美股停牌信息
us_crawler = USMarketCrawler()
us_halts = us_crawler.get_premarket_halts()

# 爬取港股停牌信息
hk_crawler = HKMarketCrawler()
hk_halts = hk_crawler.get_premarket_halts()
```

### API接口

启动API服务后，可以通过以下接口获取数据：

- `GET /api/v1/halts` - 获取所有停牌信息
- `GET /api/v1/halts/{market}` - 获取指定市场停牌信息
- `GET /api/v1/halts/today` - 获取今日停牌信息

## 配置说明

主要配置项包括：

- **数据库配置**：连接字符串、连接池设置
- **爬虫配置**：请求间隔、超时时间、重试次数
- **通知配置**：邮件服务器、钉钉机器人等
- **日志配置**：日志级别、输出格式

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目维护者：[Your Name]
- 邮箱：[your.email@example.com]
- 项目地址：[GitHub Repository URL]

## 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 支持美股、港股停牌信息爬取
- 基础API接口
- 数据存储功能
