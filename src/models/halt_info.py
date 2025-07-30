"""
停牌信息数据模型
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field

Base = declarative_base()


class HaltInfo(Base):
    """停牌信息数据库模型"""
    __tablename__ = 'halt_info'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    market = Column(String(10), nullable=False, index=True, comment='市场代码')
    symbol = Column(String(20), nullable=False, index=True, comment='股票代码')
    company_name = Column(String(200), comment='公司名称')
    halt_type = Column(String(50), comment='停牌类型')
    halt_reason = Column(Text, comment='停牌原因')
    halt_time = Column(DateTime, nullable=False, index=True, comment='停牌时间')
    resume_time = Column(DateTime, comment='恢复交易时间')
    price = Column(Float, comment='停牌前价格')
    volume = Column(Integer, comment='停牌前成交量')
    source = Column(String(100), comment='数据来源')
    url = Column(String(500), comment='原始链接')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    is_active = Column(Boolean, default=True, comment='是否有效')


class HaltInfoCreate(BaseModel):
    """创建停牌信息的请求模型"""
    market: str = Field(..., description='市场代码')
    symbol: str = Field(..., description='股票代码')
    company_name: Optional[str] = Field(None, description='公司名称')
    halt_type: Optional[str] = Field(None, description='停牌类型')
    halt_reason: Optional[str] = Field(None, description='停牌原因')
    halt_time: datetime = Field(..., description='停牌时间')
    resume_time: Optional[datetime] = Field(None, description='恢复交易时间')
    price: Optional[float] = Field(None, description='停牌前价格')
    volume: Optional[int] = Field(None, description='停牌前成交量')
    source: Optional[str] = Field(None, description='数据来源')
    url: Optional[str] = Field(None, description='原始链接')


class HaltInfoResponse(BaseModel):
    """停牌信息响应模型"""
    id: int
    market: str
    symbol: str
    company_name: Optional[str]
    halt_type: Optional[str]
    halt_reason: Optional[str]
    halt_time: datetime
    resume_time: Optional[datetime]
    price: Optional[float]
    volume: Optional[int]
    source: Optional[str]
    url: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class HaltInfoFilter(BaseModel):
    """停牌信息过滤模型"""
    market: Optional[str] = Field(None, description='市场代码')
    symbol: Optional[str] = Field(None, description='股票代码')
    halt_type: Optional[str] = Field(None, description='停牌类型')
    start_date: Optional[datetime] = Field(None, description='开始日期')
    end_date: Optional[datetime] = Field(None, description='结束日期')
    is_active: Optional[bool] = Field(None, description='是否有效')
    limit: int = Field(100, description='返回数量限制')
    offset: int = Field(0, description='偏移量')