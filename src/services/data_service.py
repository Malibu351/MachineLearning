"""
数据服务 - 简化版
负责数据的保存和导出
"""

import csv
import json
from datetime import datetime
from typing import List
from pathlib import Path

from ..models.halt_info import HaltInfo


class DataService:
    """数据服务类"""
    
    def __init__(self, data_dir: str = "data"):
        """
        初始化数据服务
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def save_to_csv(self, halts: List[HaltInfo], filename: str = None) -> str:
        """
        保存停牌信息到CSV文件
        
        Args:
            halts: 停牌信息列表
            filename: 文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"halt_info_{timestamp}.csv"
        
        filepath = self.data_dir / filename
        
        # 写入CSV文件
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            # 写入表头
            csvfile.write("股市｜信息获取时间｜股票代码｜股票信息｜停牌日期｜复牌日期\n")
            
            # 写入数据
            for halt in halts:
                csvfile.write(halt.to_csv_row() + "\n")
        
        print(f"数据已保存到: {filepath}")
        return str(filepath)
    
    def save_to_json(self, halts: List[HaltInfo], filename: str = None) -> str:
        """
        保存停牌信息到JSON文件
        
        Args:
            halts: 停牌信息列表
            filename: 文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"halt_info_{timestamp}.json"
        
        filepath = self.data_dir / filename
        
        # 转换为字典列表
        data = [halt.to_dict() for halt in halts]
        
        # 写入JSON文件
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到: {filepath}")
        return str(filepath)
    
    def print_summary(self, halts: List[HaltInfo]):
        """
        打印数据摘要
        
        Args:
            halts: 停牌信息列表
        """
        if not halts:
            print("没有获取到停牌信息")
            return
        
        print(f"\n=== 停牌信息摘要 ===")
        print(f"总数量: {len(halts)}")
        
        # 按市场统计
        market_stats = {}
        for halt in halts:
            market = halt.market
            if market not in market_stats:
                market_stats[market] = 0
            market_stats[market] += 1
        
        print("按市场统计:")
        for market, count in market_stats.items():
            print(f"  {market}: {count}条")
        
        print("\n前5条数据:")
        for i, halt in enumerate(halts[:5]):
            print(f"  {i+1}. {halt.to_csv_row()}")
        
        if len(halts) > 5:
            print(f"  ... 还有{len(halts)-5}条数据")