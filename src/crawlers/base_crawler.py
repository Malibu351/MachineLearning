"""
基础爬虫类
定义所有爬虫的通用接口和功能
"""

import time
import random
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import requests
from fake_useragent import UserAgent
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..models.halt_info import HaltInfoCreate


class BaseCrawler(ABC):
    """基础爬虫类"""
    
    def __init__(self, market: str, config: Dict[str, Any]):
        """
        初始化爬虫
        
        Args:
            market: 市场代码
            config: 配置信息
        """
        self.market = market
        self.config = config
        self.session = requests.Session()
        self.ua = UserAgent()
        self.driver = None
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        logger.info(f"初始化 {market} 市场爬虫")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
    
    def close(self):
        """关闭资源"""
        if self.driver:
            self.driver.quit()
        if self.session:
            self.session.close()
    
    def get_random_delay(self) -> float:
        """获取随机延迟时间"""
        delay_range = self.config.get('crawler', {}).get('anti_crawler', {}).get('delay_range', [1, 5])
        return random.uniform(delay_range[0], delay_range[1])
    
    def request_with_retry(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """
        带重试的请求
        
        Args:
            url: 请求URL
            method: 请求方法
            **kwargs: 其他参数
            
        Returns:
            Response对象或None
        """
        retry_times = self.config.get('crawler', {}).get('request', {}).get('retry_times', 3)
        retry_delay = self.config.get('crawler', {}).get('request', {}).get('retry_delay', 5)
        
        for attempt in range(retry_times):
            try:
                # 随机延迟
                if self.config.get('crawler', {}).get('anti_crawler', {}).get('random_delay', True):
                    time.sleep(self.get_random_delay())
                
                # 更新User-Agent
                self.session.headers['User-Agent'] = self.ua.random
                
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                
                logger.debug(f"请求成功: {url}")
                return response
                
            except requests.RequestException as e:
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{retry_times}): {url}, 错误: {e}")
                if attempt < retry_times - 1:
                    time.sleep(retry_delay)
                else:
                    logger.error(f"请求最终失败: {url}")
                    return None
    
    def init_selenium_driver(self, headless: bool = True) -> webdriver.Chrome:
        """
        初始化Selenium WebDriver
        
        Args:
            headless: 是否无头模式
            
        Returns:
            Chrome WebDriver实例
        """
        options = Options()
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument(f'--user-agent={self.ua.random}')
        
        # 禁用图片加载以提高速度
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=options)
        return self.driver
    
    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        """
        等待元素出现
        
        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间
            
        Returns:
            元素对象
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    @abstractmethod
    def get_premarket_halts(self) -> List[HaltInfoCreate]:
        """
        获取盘前停牌信息
        
        Returns:
            停牌信息列表
        """
        pass
    
    @abstractmethod
    def get_regular_halts(self) -> List[HaltInfoCreate]:
        """
        获取常规交易时间停牌信息
        
        Returns:
            停牌信息列表
        """
        pass
    
    @abstractmethod
    def get_aftermarket_halts(self) -> List[HaltInfoCreate]:
        """
        获取盘后停牌信息
        
        Returns:
            停牌信息列表
        """
        pass
    
    def get_all_halts(self) -> List[HaltInfoCreate]:
        """
        获取所有停牌信息
        
        Returns:
            停牌信息列表
        """
        all_halts = []
        
        try:
            # 获取盘前停牌
            premarket_halts = self.get_premarket_halts()
            all_halts.extend(premarket_halts)
            logger.info(f"获取到 {len(premarket_halts)} 条盘前停牌信息")
            
            # 获取常规交易时间停牌
            regular_halts = self.get_regular_halts()
            all_halts.extend(regular_halts)
            logger.info(f"获取到 {len(regular_halts)} 条常规交易时间停牌信息")
            
            # 获取盘后停牌
            aftermarket_halts = self.get_aftermarket_halts()
            all_halts.extend(aftermarket_halts)
            logger.info(f"获取到 {len(aftermarket_halts)} 条盘后停牌信息")
            
        except Exception as e:
            logger.error(f"获取停牌信息时发生错误: {e}")
        
        return all_halts
    
    def is_trading_time(self, session_type: str = 'regular') -> bool:
        """
        检查是否为交易时间
        
        Args:
            session_type: 交易时段类型 (premarket, regular, aftermarket)
            
        Returns:
            是否为交易时间
        """
        # 这里应该根据具体市场的交易时间来判断
        # 暂时返回True，具体实现由子类重写
        return True
    
    def parse_datetime(self, date_str: str, format_str: str = None) -> Optional[datetime]:
        """
        解析日期时间字符串
        
        Args:
            date_str: 日期时间字符串
            format_str: 格式字符串
            
        Returns:
            datetime对象或None
        """
        try:
            if format_str:
                return datetime.strptime(date_str, format_str)
            else:
                # 尝试常见格式
                formats = [
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d %H:%M',
                    '%Y-%m-%d',
                    '%m/%d/%Y %H:%M:%S',
                    '%m/%d/%Y %H:%M',
                    '%m/%d/%Y',
                ]
                
                for fmt in formats:
                    try:
                        return datetime.strptime(date_str, fmt)
                    except ValueError:
                        continue
                
                logger.warning(f"无法解析日期时间: {date_str}")
                return None
                
        except Exception as e:
            logger.error(f"解析日期时间时发生错误: {date_str}, {e}")
            return None