import logging
import time
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.crawlers.base_crawler import BaseCrawler, CrawlerConfig

logger = logging.getLogger(__name__)


class RequestsHouseCrawler(BaseCrawler):
    """Basic static-page crawler based on requests and BeautifulSoup."""

    def __init__(self, config: CrawlerConfig) -> None:
        """Create a requests session with crawler headers."""
        super().__init__(config)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": config.user_agent,
                "Accept-Language": "zh-CN,zh;q=0.9",
            }
        )

    def crawl(self) -> list[dict[str, Any]]:
        """Crawl all configured pages and return raw house rows."""
        rows: list[dict[str, Any]] = []
        if not self.config.base_url:
            logger.warning("未配置 CRAWLER_BASE_URL，跳过在线采集")
            return rows

        for page in range(1, self.config.max_pages + 1):
            try:
                html = self.fetch_page(page)
                rows.extend(self.parse_list(html))
            except Exception as exc:
                logger.exception("采集第 %s 页失败: %s", page, exc)
            time.sleep(self.config.request_interval)
        return rows

    def fetch_page(self, page: int) -> str:
        """Fetch one page with retry handling."""
        url = self.build_page_url(page)
        last_error: Exception | None = None
        for attempt in range(1, self.config.retry_times + 1):
            try:
                response = self.session.get(url, timeout=self.config.timeout)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                return response.text
            except requests.RequestException as exc:
                last_error = exc
                logger.warning("请求失败 url=%s attempt=%s error=%s", url, attempt, exc)
                time.sleep(self.config.request_interval)
        raise RuntimeError(f"请求失败: {url}") from last_error

    def build_page_url(self, page: int) -> str:
        """Build page URL with a conservative page query fallback."""
        if "{page}" in self.config.base_url:
            return self.config.base_url.format(page=page)
        connector = "&" if "?" in self.config.base_url else "?"
        return f"{self.config.base_url}{connector}page={page}"

    def parse_list(self, html: str) -> list[dict[str, Any]]:
        """Parse common listing cards from a static HTML page."""
        soup = BeautifulSoup(html, "lxml")
        cards = soup.select(
            ".house-item, .list-item, .sellListContent li, li.clear, article, .card"
        )
        rows = []
        for card in cards:
            item = self.parse_card(card)
            if item:
                rows.append(item)
        return rows

    def parse_card(self, card: Any) -> dict[str, Any] | None:
        """Parse one house card using common Chinese listing conventions."""
        link = card.select_one("a[href]")
        title_node = card.select_one(".title, h2, h3, a")
        source_url = urljoin(self.config.base_url, link.get("href")) if link else None
        title = title_node.get_text(" ", strip=True) if title_node else None
        if not title or not source_url:
            return None

        text = card.get_text(" ", strip=True)
        return {
            "title": title,
            "city": self.config.city,
            "district": self._text_of(card, ".district, .positionInfo a:first-child"),
            "community": self._text_of(card, ".community, .positionInfo a:last-child"),
            "total_price": self._text_of(card, ".totalPrice, .total-price")
            or self._match(text, r"(\d+(?:\.\d+)?)\s*万"),
            "unit_price": self._text_of(card, ".unitPrice, .unit-price")
            or self._match(text, r"(\d+(?:\.\d+)?)\s*元/平"),
            "area": self._text_of(card, ".area")
            or self._match(text, r"(\d+(?:\.\d+)?)\s*(?:平米|㎡|m²)"),
            "layout": self._match(text, r"(\d+\s*室\s*\d+\s*厅)"),
            "floor": self._match(text, r"([高中低]楼层[^ ]*)"),
            "orientation": self._match(text, r"(南北|朝南|朝北|朝东|朝西|东西)"),
            "decoration": self._match(text, r"(精装|简装|毛坯|中装)"),
            "build_year": self._match(text, r"((?:19|20)\d{2}\s*年)"),
            "source_url": source_url,
        }

    @staticmethod
    def _text_of(card: Any, selector: str) -> str | None:
        """Return normalized text for the first matching selector."""
        node = card.select_one(selector)
        return node.get_text(" ", strip=True) if node else None

    @staticmethod
    def _match(text: str, pattern: str) -> str | None:
        """Return the first regex group from text."""
        import re

        match = re.search(pattern, text)
        return match.group(1) if match else None
