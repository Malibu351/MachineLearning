"""
停牌信息数据模型 - 简化版
"""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class HaltInfo:
    """停牌信息数据类"""
    market: str              # 股市 (如: 美股、港股、A股、日股、欧股)
    fetch_time: datetime     # 信息获取时间
    symbol: str              # 股票代码
    company_name: str        # 股票信息（公司名称）
    halt_date: datetime      # 停牌日期
    resume_date: Optional[datetime] = None  # 复牌日期（可选）
    
    def to_csv_row(self) -> str:
        """转换为CSV格式"""
        resume_str = self.resume_date.strftime('%Y-%m-%d') if self.resume_date else ''
        return f"{self.market}｜{self.fetch_time.strftime('%Y-%m-%d %H:%M:%S')}｜{self.symbol}｜{self.company_name}｜{self.halt_date.strftime('%Y-%m-%d')}｜{resume_str}"
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'market': self.market,
            'fetch_time': self.fetch_time.strftime('%Y-%m-%d %H:%M:%S'),
            'symbol': self.symbol,
            'company_name': self.company_name,
            'halt_date': self.halt_date.strftime('%Y-%m-%d'),
            'resume_date': self.resume_date.strftime('%Y-%m-%d') if self.resume_date else ''
        }