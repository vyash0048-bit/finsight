from datetime import datetime
from sqlalchemy import String, DateTime, Float, BigInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class PriceBar(Base):
    __tablename__ = "price_bars"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    open_price: Mapped[float] = mapped_column(Float)
    high_price: Mapped[float] = mapped_column(Float)
    low_price: Mapped[float] = mapped_column(Float)
    close_price: Mapped[float] = mapped_column(Float)
    volume: Mapped[int] = mapped_column(BigInteger)
    
    __table_args__ = (
        UniqueConstraint('ticker', 'timestamp', name='uix_ticker_timestamp'),
    )
