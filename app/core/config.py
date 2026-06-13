import os
from dataclasses import dataclass
from urllib.parse import quote_plus

from dotenv import load_dotenv


load_dotenv()


def _as_bool(value: str | None, default: bool = False) -> bool:
    """Convert common environment string values to bool."""
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Central application settings loaded from environment variables."""

    app_name: str = os.getenv("APP_NAME", "二手房数据爬取及可视化分析系统")
    app_env: str = os.getenv("APP_ENV", "development")
    app_debug: bool = _as_bool(os.getenv("APP_DEBUG"), True)
    auto_create_tables: bool = _as_bool(os.getenv("AUTO_CREATE_TABLES"), True)

    db_host: str = os.getenv("DB_HOST", "127.0.0.1")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "second_hand_house")
    db_charset: str = os.getenv("DB_CHARSET", "utf8mb4")

    crawler_base_url: str = os.getenv("CRAWLER_BASE_URL", "")
    crawler_city: str = os.getenv("CRAWLER_CITY", "上海")
    crawler_max_pages: int = int(os.getenv("CRAWLER_MAX_PAGES", "5"))
    crawler_request_interval: float = float(os.getenv("CRAWLER_REQUEST_INTERVAL", "1.5"))
    crawler_timeout: int = int(os.getenv("CRAWLER_TIMEOUT", "10"))
    crawler_retry_times: int = int(os.getenv("CRAWLER_RETRY_TIMES", "3"))
    crawler_user_agent: str = os.getenv(
        "CRAWLER_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    )

    @property
    def database_url(self) -> str:
        """Build SQLAlchemy database URL from safe environment settings."""
        password = quote_plus(self.db_password)
        return (
            f"mysql+pymysql://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?charset={self.db_charset}"
        )


settings = Settings()
