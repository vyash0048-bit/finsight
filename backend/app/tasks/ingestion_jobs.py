import asyncio
import logging
import os
import sys

# Ensure the backend directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.api.deps import SessionLocal
from app.models.price_bar import PriceBar
from app.services.market_data_service import get_price_history
from app.services.news_service import get_recent_news
from app.services.rag_service import chunk_and_store_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_ingestion_for_ticker(ticker: str):
    logger.info(f"========== Starting ingestion for {ticker} ==========")
    
    # 1. Ingest Prices into Postgres
    logger.info(f"[{ticker}] Ingesting prices...")
    db = SessionLocal()
    try:
        history = get_price_history(ticker, period="1mo", use_cache=False)
        bars_added = 0
        for bar in history.bars:
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
                bars_added += 1
        db.commit()
        logger.info(f"[{ticker}] Added {bars_added} new price bars to Postgres.")
    except Exception as e:
        logger.error(f"[{ticker}] Failed to ingest prices: {e}")
    finally:
        db.close()
        
    # 2. Ingest News into Mongo and ChromaDB
    logger.info(f"[{ticker}] Ingesting news into Mongo and ChromaDB...")
    try:
        # get_recent_news automatically deduplicates and stores raw articles into Mongo
        articles = await get_recent_news(ticker, days=7)
        logger.info(f"[{ticker}] Fetched and saved {len(articles)} new unique articles to Mongo.")
        
        chunks_added = 0
        for article in articles:
            # Prepare text for embedding
            text_to_embed = f"Title: {article.title}\nSource: {article.source}\nSummary: {article.summary}"
            metadata = {
                "ticker": article.ticker,
                "url": article.url,
                "source": article.source
            }
            # Create a deterministic ID
            doc_id = f"{article.ticker}_{hash(article.url)}"
            
            n = chunk_and_store_text(doc_id, text_to_embed, metadata)
            chunks_added += n
            
        logger.info(f"[{ticker}] Embedded {chunks_added} chunks into ChromaDB.")
    except Exception as e:
        logger.error(f"[{ticker}] Failed to ingest news: {e}")
        
async def main():
    tickers = ["AAPL", "MSFT", "NVDA"]
    logger.info("Starting Full Ingestion Job...")
    for ticker in tickers:
        await run_ingestion_for_ticker(ticker)
    logger.info("Full Ingestion Job Complete!")
        
if __name__ == "__main__":
    asyncio.run(main())
