"""
GlobalMarketHalt 主程序入口
"""

import sys
import os
import yaml
import click
from pathlib import Path
from loguru import logger
from typing import Dict, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.crawlers import USMarketCrawler, HKMarketCrawler, CNMarketCrawler
from src.services.halt_service import HaltService
from src.api.app import create_app


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    if config_path is None:
        config_path = project_root / "config" / "config.yaml"
    
    if not os.path.exists(config_path):
        logger.error(f"配置文件不存在: {config_path}")
        sys.exit(1)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info(f"成功加载配置文件: {config_path}")
        return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        sys.exit(1)


def setup_logging(config: Dict[str, Any]):
    """
    设置日志配置
    
    Args:
        config: 配置字典
    """
    log_config = config.get('logging', {})
    
    # 移除默认的日志处理器
    logger.remove()
    
    # 添加控制台日志
    logger.add(
        sys.stdout,
        level=log_config.get('level', 'INFO'),
        format=log_config.get('format', "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    )
    
    # 添加文件日志
    log_file = log_config.get('file', 'logs/global_market_halt.log')
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_file,
        level=log_config.get('level', 'INFO'),
        format=log_config.get('format', "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"),
        rotation=log_config.get('rotation', '1 day'),
        retention=log_config.get('retention', '30 days'),
        compression=log_config.get('compression', 'zip')
    )


@click.group()
def cli():
    """GlobalMarketHalt 命令行工具"""
    pass


@cli.command()
@click.option('--config', '-c', help='配置文件路径')
@click.option('--market', '-m', help='指定市场 (us, hk, cn, all)', default='all')
def crawl(config, market):
    """爬取停牌信息"""
    # 加载配置
    config_data = load_config(config)
    setup_logging(config_data)
    
    logger.info("开始爬取停牌信息")
    
    # 创建服务
    halt_service = HaltService(config_data)
    
    # 选择市场
    markets = []
    if market == 'all':
        markets = ['us', 'hk', 'cn']
    else:
        markets = [market]
    
    # 爬取数据
    for market_code in markets:
        if not config_data.get('markets', {}).get(market_code, {}).get('enabled', False):
            logger.warning(f"市场 {market_code} 未启用，跳过")
            continue
        
        try:
            logger.info(f"开始爬取 {market_code} 市场停牌信息")
            
            # 创建对应的爬虫
            if market_code == 'us':
                crawler = USMarketCrawler(market_code, config_data)
            elif market_code == 'hk':
                crawler = HKMarketCrawler(market_code, config_data)
            elif market_code == 'cn':
                crawler = CNMarketCrawler(market_code, config_data)
            else:
                logger.error(f"不支持的市场: {market_code}")
                continue
            
            # 爬取数据
            halts = crawler.get_all_halts()
            
            # 保存数据
            if halts:
                saved_count = halt_service.save_halts(halts)
                logger.info(f"{market_code} 市场保存了 {saved_count} 条停牌信息")
            else:
                logger.info(f"{market_code} 市场没有新的停牌信息")
            
            # 关闭爬虫
            crawler.close()
            
        except Exception as e:
            logger.error(f"爬取 {market_code} 市场时发生错误: {e}")
    
    logger.info("停牌信息爬取完成")


@cli.command()
@click.option('--config', '-c', help='配置文件路径')
@click.option('--host', default='0.0.0.0', help='API服务主机')
@click.option('--port', default=8000, help='API服务端口')
@click.option('--reload', is_flag=True, help='开发模式自动重载')
def api(config, host, port, reload):
    """启动API服务"""
    # 加载配置
    config_data = load_config(config)
    setup_logging(config_data)
    
    logger.info(f"启动API服务: http://{host}:{port}")
    
    # 创建FastAPI应用
    app = create_app(config_data)
    
    # 启动服务
    import uvicorn
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        log_level=config_data.get('logging', {}).get('level', 'info').lower()
    )


@cli.command()
@click.option('--config', '-c', help='配置文件路径')
def scheduler(config):
    """启动定时任务调度器"""
    # 加载配置
    config_data = load_config(config)
    setup_logging(config_data)
    
    logger.info("启动定时任务调度器")
    
    # 这里应该启动Celery或其他任务调度器
    # 暂时只是占位
    logger.info("定时任务调度器功能待实现")


@cli.command()
@click.option('--config', '-c', help='配置文件路径')
def init_db(config):
    """初始化数据库"""
    # 加载配置
    config_data = load_config(config)
    setup_logging(config_data)
    
    logger.info("初始化数据库")
    
    # 创建数据库表
    from src.services.database_service import DatabaseService
    db_service = DatabaseService(config_data)
    db_service.init_database()
    
    logger.info("数据库初始化完成")


@cli.command()
@click.option('--config', '-c', help='配置文件路径')
def test(config):
    """运行测试"""
    # 加载配置
    config_data = load_config(config)
    setup_logging(config_data)
    
    logger.info("运行测试")
    
    # 运行pytest
    import pytest
    test_dir = project_root / "tests"
    pytest.main([str(test_dir), "-v"])


if __name__ == "__main__":
    cli()