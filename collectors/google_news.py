import feedparser
from .base import BaseCollector, StockData


class GoogleNewsCollector(BaseCollector):
    BASE_URL = "https://news.google.com/rss/search?q={query}&hl=ja&gl=JP&ceid=JP:ja"

    def collect(self, stock: dict) -> StockData:
        data = StockData(code=stock["code"], name=stock["name"])

        try:
            query = stock["name"].replace(" ", "+") + "+株"
            url = self.BASE_URL.format(query=query)
            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:
                data.news.append({
                    "source": "Google News",
                    "title": entry.get("title", "").strip(),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                })
        except Exception as e:
            print(f"[GoogleNews] Error for {stock['name']}: {e}")

        return data
