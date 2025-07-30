#!/usr/bin/env python3
"""
简单的测试程序
"""

from datetime import datetime
from src.models.halt_info import HaltInfo

def main():
    print("=== GlobalMarketHalt 测试程序 ===")
    
    # 创建测试数据
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
    
    # 打印数据
    print("\n=== 停牌信息 ===")
    print("股市｜信息获取时间｜股票代码｜股票信息｜停牌日期｜复牌日期")
    for halt in test_halts:
        print(halt.to_csv_row())
    
    print(f"\n总共 {len(test_halts)} 条停牌信息")
    print("=== 测试完成 ===")

if __name__ == "__main__":
    main()