"""
GlobalMarketHalt 主程序入口 - 简化版
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.crawlers.base_crawler import BaseCrawler
from src.services.data_service import DataService


def main():
    """主程序"""
    print("=== GlobalMarketHalt 停牌信息爬取系统 ===")
    
    # 初始化数据服务
    data_service = DataService()
    
    # 这里需要你提供5个股市的爬虫类
    # 示例：创建爬虫实例并爬取数据
    all_halts = []
    
    # 示例：美股爬虫
    # us_crawler = USCrawler("美股")
    # us_halts = us_crawler.crawl_halts()
    # all_halts.extend(us_halts)
    
    # 示例：港股爬虫
    # hk_crawler = HKCrawler("港股")
    # hk_halts = hk_crawler.crawl_halts()
    # all_halts.extend(hk_halts)
    
    # 示例：A股爬虫
    # cn_crawler = CNCrawler("A股")
    # cn_halts = cn_crawler.crawl_halts()
    # all_halts.extend(cn_halts)
    
    # 示例：日股爬虫
    # jp_crawler = JPCrawler("日股")
    # jp_halts = jp_crawler.crawl_halts()
    # all_halts.extend(jp_halts)
    
    # 示例：欧股爬虫
    # eu_crawler = EUCrawler("欧股")
    # eu_halts = eu_crawler.crawl_halts()
    # all_halts.extend(eu_halts)
    
    # 临时测试数据
    from datetime import datetime
    from src.models.halt_info import HaltInfo
    
    # 创建一些测试数据
    test_halts = [
        HaltInfo(
            market="美股",
            fetch_time=datetime.now(),
            symbol="AAPL",
            company_name="苹果公司",
            halt_date=datetime(2024, 1, 15),
            resume_date=datetime(2024, 1, 16)
        ),
        HaltInfo(
            market="港股",
            fetch_time=datetime.now(),
            symbol="0700",
            company_name="腾讯控股",
            halt_date=datetime(2024, 1, 15)
        )
    ]
    all_halts = test_halts
    
    # 打印摘要
    data_service.print_summary(all_halts)
    
    # 保存数据
    if all_halts:
        csv_file = data_service.save_to_csv(all_halts)
        json_file = data_service.save_to_json(all_halts)
        print(f"\n数据已保存:")
        print(f"CSV文件: {csv_file}")
        print(f"JSON文件: {json_file}")
    
    print("\n=== 爬取完成 ===")


if __name__ == "__main__":
    main()