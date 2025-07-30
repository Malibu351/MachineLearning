"""
基础爬虫类 - 简化版
"""

import time
import requests
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from fake_useragent import UserAgent

from ..models.halt_info import HaltInfo


class BaseCrawler(ABC):
    """基础爬虫类"""
    
    def __init__(self, market_name: str):
        """
        初始化爬虫
        
        Args:
            market_name: 市场名称 (如: 美股、港股、A股、日股、欧股)
        """
        self.market_name = market_name
        self.session = requests.Session()
        self.ua = UserAgent()
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def get_page(self, url: str) -> str:
        """
        获取网页内容
        
        Args:
            url: 网页URL
            
        Returns:
            网页HTML内容
        """
        try:
            # 随机延迟，避免被反爬
            time.sleep(1)
            
            # 更新User-Agent
            self.session.headers['User-Agent'] = self.ua.random
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            return response.text
            
        except Exception as e:
            print(f"获取页面失败: {url}, 错误: {e}")
            return ""
    
    @abstractmethod
    def crawl_halts(self) -> List[HaltInfo]:
        """
        爬取停牌信息 - 子类必须实现
        
        Returns:
            停牌信息列表
        """
        pass
    
    def create_halt_info(self, symbol: str, company_name: str, halt_date: datetime, resume_date: datetime = None) -> HaltInfo:
        """
        创建停牌信息对象
        
        Args:
            symbol: 股票代码
            company_name: 公司名称
            halt_date: 停牌日期
            resume_date: 复牌日期
            
        Returns:
            停牌信息对象
        """
        return HaltInfo(
            market=self.market_name,
            fetch_time=datetime.now(),
            symbol=symbol,
            company_name=company_name,
            halt_date=halt_date,
            resume_date=resume_date
        )