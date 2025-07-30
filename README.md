# GlobalMarketHalt

全球股市停牌信息爬取系统 - 简化版

## 项目简介

GlobalMarketHalt 是一个专门用于爬取不同国家股市停牌信息的系统。该系统支持多个主要股票市场，提供简单的数据获取和导出功能。

## 功能特性

- 🌍 **多市场支持**：支持美股、港股、A股、日股、欧股等主要市场
- 📊 **数据导出**：支持CSV和JSON格式导出
- 🛡️ **反爬虫处理**：智能处理反爬虫机制
- 📈 **数据摘要**：提供数据统计和摘要信息

## 项目结构

```
GlobalMarketHalt/
├── src/
│   ├── crawlers/          # 爬虫模块
│   │   ├── base_crawler.py    # 基础爬虫类
│   │   └── example_crawler.py # 示例爬虫
│   ├── models/
│   │   └── halt_info.py       # 停牌信息数据模型
│   ├── services/
│   │   └── data_service.py    # 数据存储服务
│   └── main.py                # 主程序入口
├── data/                  # 数据存储目录
├── requirements.txt       # 依赖包
└── README.md             # 项目说明
```

## 数据格式

最终输出格式：
```
股市｜信息获取时间｜股票代码｜股票信息｜停牌日期｜复牌日期
```

示例：
```
美股｜2024-01-15 10:30:00｜AAPL｜苹果公司｜2024-01-15｜2024-01-16
港股｜2024-01-15 10:30:00｜0700｜腾讯控股｜2024-01-15｜
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行程序

```bash
python src/main.py
```

### 3. 查看结果

程序会在 `data/` 目录下生成：
- `halt_info_YYYYMMDD_HHMMSS.csv` - CSV格式数据
- `halt_info_YYYYMMDD_HHMMSS.json` - JSON格式数据

## 如何添加新的股市爬虫

### 1. 创建爬虫类

```python
# src/crawlers/us_crawler.py
from .base_crawler import BaseCrawler
from ..models.halt_info import HaltInfo

class USCrawler(BaseCrawler):
    def __init__(self):
        super().__init__("美股")
        self.url = "https://your-us-market-url.com"
    
    def crawl_halts(self):
        # 实现具体的爬取逻辑
        # 1. 获取网页内容
        html = self.get_page(self.url)
        
        # 2. 解析HTML，提取停牌信息
        # 3. 返回 HaltInfo 对象列表
        pass
```

### 2. 在主程序中注册

```python
# src/main.py
from src.crawlers.us_crawler import USCrawler

# 创建爬虫实例
us_crawler = USCrawler()
us_halts = us_crawler.crawl_halts()
all_halts.extend(us_halts)
```

## 技术栈

- **Python 3.8+**: 主要开发语言
- **Requests**: HTTP请求库
- **BeautifulSoup**: HTML解析
- **Fake-UserAgent**: 随机User-Agent
- **Pandas**: 数据处理

## 注意事项

1. **反爬虫处理**: 程序已包含基本的反爬虫措施，如随机延迟和User-Agent轮换
2. **数据准确性**: 需要根据具体网站调整解析逻辑
3. **法律合规**: 请确保爬取行为符合相关法律法规
4. **网站变化**: 目标网站可能改变结构，需要及时更新爬虫

## 开发计划

1. **第一阶段**: 实现基础爬虫框架 ✅
2. **第二阶段**: 添加具体股市爬虫
3. **第三阶段**: 优化数据解析和错误处理
4. **第四阶段**: 添加更多功能和优化

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 许可证

本项目采用MIT许可证。
