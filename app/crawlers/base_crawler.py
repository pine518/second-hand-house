from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class CrawlerConfig:
    """Runtime configuration for crawler tasks."""

    base_url: str
    city: str
    max_pages: int = 5
    request_interval: float = 1.5
    timeout: int = 10
    retry_times: int = 3
    user_agent: str = ""


class BaseCrawler(ABC):
    """Abstract crawler contract shared by all crawler implementations."""

    def __init__(self, config: CrawlerConfig) -> None:
        """Store crawler configuration."""
        self.config = config

    @abstractmethod
    def crawl(self) -> list[dict[str, Any]]:
        """Crawl house listing rows from the configured source."""
