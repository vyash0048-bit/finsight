import sys
import os
from pathlib import Path

# Add backend directory to path so we can import app modules
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.append(str(backend_dir))

from app.api.deps import SessionLocal
from app.services.market_data_service import get_price_history
from app.models.price_bar import PriceBar

def seed():
    db = SessionLocal()
    tickers = ["AAPL", "MSFT", "NVDA"]
    
    print("Seeding database with historical price data...")
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        try:
            history = get_price_history(ticker, period="1mo", use_cache=False)
            
            for bar in history.bars:
                # Basic check to prevent duplicates
                existing = db.query(PriceBar).filter_by(ticker=bar.ticker, timestamp=bar.timestamp).first()
                if not existing:
                    db_bar = PriceBar(
                        ticker=bar.ticker,
                        timestamp=bar.timestamp,
                        open_price=bar.open,
                        high_price=bar.high,
                        low_price=bar.low,
                        close_price=bar.close,
                        volume=bar.volume
                    )
                    db.add(db_bar)
            print(f"Successfully loaded {len(history.bars)} bars for {ticker}.")
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            
    db.commit()
    print("Database seeding complete!")

if __name__ == "__main__":
    seed()
