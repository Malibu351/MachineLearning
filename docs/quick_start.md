# GlobalMarketHalt 快速开始指南

## 项目简介

GlobalMarketHalt 是一个专门用于爬取和监控不同国家股市盘前停牌信息的系统。本指南将帮助你快速搭建和运行项目。

## 环境要求

### 系统要求
- **操作系统**: Linux, macOS, Windows
- **Python版本**: 3.8+
- **内存**: 至少4GB RAM
- **磁盘空间**: 至少10GB可用空间

### 软件依赖
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: 2.0+

## 快速开始

### 方法一：使用Docker (推荐)

#### 1. 克隆项目
```bash
git clone <repository-url>
cd GlobalMarketHalt
```

#### 2. 配置环境
```bash
# 复制配置文件
cp config/config.example.yaml config/config.yaml

# 编辑配置文件 (根据需要修改数据库密码等)
vim config/config.yaml
```

#### 3. 启动服务
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f app
```

#### 4. 访问服务
- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **Flower监控**: http://localhost:5555
- **Nginx**: http://localhost:80

### 方法二：本地开发环境

#### 1. 克隆项目
```bash
git clone <repository-url>
cd GlobalMarketHalt
```

#### 2. 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

#### 3. 安装依赖
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Chrome和ChromeDriver (用于Selenium)
# Linux
sudo apt-get install google-chrome-stable
# macOS
brew install --cask google-chrome
# Windows: 下载并安装Chrome
```

#### 4. 配置数据库
```bash
# 启动MySQL (使用Docker)
docker run -d \
  --name mysql \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=global_market_halt \
  -p 3306:3306 \
  mysql:8.0

# 启动Redis
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7-alpine

# 启动MongoDB
docker run -d \
  --name mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -p 27017:27017 \
  mongo:6
```

#### 5. 配置项目
```bash
# 复制配置文件
cp config/config.example.yaml config/config.yaml

# 编辑配置文件
vim config/config.yaml
```

#### 6. 初始化数据库
```bash
# 初始化数据库表
python src/main.py init-db
```

#### 7. 运行项目
```bash
# 启动API服务
python src/main.py api --reload

# 运行爬虫 (新终端)
python src/main.py crawl --market us

# 启动定时任务 (新终端)
python src/main.py scheduler
```

## 配置说明

### 主要配置项

#### 数据库配置
```yaml
database:
  main:
    type: mysql
    host: localhost
    port: 3306
    username: root
    password: password
    database: global_market_halt
```

#### 爬虫配置
```yaml
crawler:
  request:
    timeout: 30
    retry_times: 3
  anti_crawler:
    random_delay: true
    delay_range: [1, 5]
```

#### 市场配置
```yaml
markets:
  us:
    enabled: true
    name: "美国股市"
    timezone: "America/New_York"
```

## 使用示例

### 1. 爬取停牌信息

```bash
# 爬取所有市场
python src/main.py crawl --market all

# 爬取指定市场
python src/main.py crawl --market us
python src/main.py crawl --market hk
python src/main.py crawl --market cn
```

### 2. 查询API接口

```bash
# 获取所有停牌信息
curl http://localhost:8000/api/v1/halts

# 获取指定市场停牌信息
curl http://localhost:8000/api/v1/halts/us

# 获取今日停牌信息
curl http://localhost:8000/api/v1/halts/today
```

### 3. 使用Python SDK

```python
from src.crawlers import USMarketCrawler
from src.services.halt_service import HaltService

# 创建爬虫实例
crawler = USMarketCrawler('us', config)

# 爬取停牌信息
halts = crawler.get_premarket_halts()

# 保存到数据库
service = HaltService(config)
service.save_halts(halts)
```

## 常见问题

### 1. Docker服务启动失败

**问题**: 端口被占用
```bash
# 检查端口占用
netstat -tulpn | grep :8000

# 停止占用端口的服务
sudo systemctl stop <service-name>
```

**问题**: 内存不足
```bash
# 增加Docker内存限制
# 在Docker Desktop中设置内存限制为4GB+
```

### 2. 爬虫无法获取数据

**问题**: 网络连接问题
```bash
# 检查网络连接
ping www.google.com

# 配置代理 (如果需要)
# 在config.yaml中配置代理设置
```

**问题**: 反爬虫限制
```bash
# 增加延迟时间
# 修改config.yaml中的delay_range
```

### 3. 数据库连接失败

**问题**: 数据库服务未启动
```bash
# 检查数据库服务状态
docker-compose ps

# 重启数据库服务
docker-compose restart mysql
```

**问题**: 数据库密码错误
```bash
# 检查配置文件中的数据库密码
cat config/config.yaml | grep password
```

## 开发指南

### 添加新的市场爬虫

1. 创建爬虫类
```python
# src/crawlers/new_market.py
from .base_crawler import BaseCrawler

class NewMarketCrawler(BaseCrawler):
    def get_premarket_halts(self):
        # 实现盘前停牌爬取逻辑
        pass
    
    def get_regular_halts(self):
        # 实现常规交易时间停牌爬取逻辑
        pass
    
    def get_aftermarket_halts(self):
        # 实现盘后停牌爬取逻辑
        pass
```

2. 注册爬虫
```python
# src/crawlers/__init__.py
from .new_market import NewMarketCrawler

__all__ = [
    'NewMarketCrawler',
    # ... 其他爬虫
]
```

3. 添加配置
```yaml
# config/config.yaml
markets:
  new_market:
    enabled: true
    name: "新市场"
    timezone: "Asia/Shanghai"
    data_sources:
      - name: "数据源名称"
        url: "数据源URL"
        type: "web"
```

### 添加新的API接口

1. 创建路由
```python
# src/api/routes/halts.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/custom-endpoint")
async def custom_endpoint():
    return {"message": "Custom endpoint"}
```

2. 注册路由
```python
# src/api/app.py
from .routes import halts

app.include_router(halts.router, prefix="/api/v1")
```

## 监控和维护

### 日志查看

```bash
# 查看应用日志
docker-compose logs -f app

# 查看爬虫日志
docker-compose logs -f crawler

# 查看数据库日志
docker-compose logs -f mysql
```

### 性能监控

```bash
# 查看系统资源使用
docker stats

# 查看API性能
curl http://localhost:8000/health
```

### 数据备份

```bash
# 备份数据库
docker-compose exec mysql mysqldump -u root -p global_market_halt > backup.sql

# 恢复数据库
docker-compose exec -T mysql mysql -u root -p global_market_halt < backup.sql
```

## 技术支持

### 获取帮助

1. **查看文档**: 阅读项目文档
2. **查看日志**: 检查错误日志
3. **提交Issue**: 在GitHub上提交问题
4. **社区讨论**: 参与社区讨论

### 贡献代码

1. Fork项目
2. 创建功能分支
3. 提交代码
4. 创建Pull Request

## 许可证

本项目采用MIT许可证，详见LICENSE文件。