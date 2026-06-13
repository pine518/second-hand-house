import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.config import settings
from app.core.database import SessionLocal, init_db
from app.core.logger import configure_logging, get_logger
from app.crawlers.base_crawler import CrawlerConfig
from app.crawlers.requests_crawler import RequestsHouseCrawler
from app.crawlers.sample_data import sample_houses
from app.crud.house_crud import bulk_upsert_houses
from app.models.crawl_log import CrawlLog
from app.services.clean_service import clean_houses

logger = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse crawler CLI arguments."""
    parser = argparse.ArgumentParser(description="运行二手房基础爬虫")
    parser.add_argument("--sample", action="store_true", help="写入本地样例数据")
    parser.add_argument("--pages", type=int, default=settings.crawler_max_pages)
    parser.add_argument("--city", default=settings.crawler_city)
    return parser.parse_args()


def main() -> None:
    """Run crawler, clean rows, and persist them to MySQL."""
    configure_logging()
    args = parse_args()
    init_db()
    db = SessionLocal()
    now = datetime.now(UTC).replace(tzinfo=None)
    log = CrawlLog(task_name="requests_house_crawler", start_time=now)
    db.add(log)
    db.commit()
    try:
        if args.sample:
            raw_rows = sample_houses(city=args.city)
        else:
            config = CrawlerConfig(
                base_url=settings.crawler_base_url,
                city=args.city,
                max_pages=args.pages,
                request_interval=settings.crawler_request_interval,
                timeout=settings.crawler_timeout,
                retry_times=settings.crawler_retry_times,
                user_agent=settings.crawler_user_agent,
            )
            raw_rows = RequestsHouseCrawler(config).crawl()
        cleaned_rows = clean_houses(raw_rows, default_city=args.city)
        success_count = bulk_upsert_houses(db, cleaned_rows)
        log.success_count = success_count
        log.fail_count = max(len(raw_rows) - success_count, 0)
        log.status = "success"
        logger.info("爬虫完成: 原始=%s 入库=%s", len(raw_rows), success_count)
    except Exception as exc:
        db.rollback()
        log.status = "failed"
        log.error_message = str(exc)
        logger.exception("爬虫执行失败: %s", exc)
        raise
    finally:
        log.end_time = datetime.now(UTC).replace(tzinfo=None)
        db.add(log)
        db.commit()
        db.close()


if __name__ == "__main__":
    main()
