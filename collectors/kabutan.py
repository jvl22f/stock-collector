import time
import requests
from bs4 import BeautifulSoup
import config
from .base import BaseCollector, StockData


class KabutanCollector(BaseCollector):
    BASE_URL = "https://kabutan.jp/stock/news?code={code}"
    HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

    def collect(self, stock: dict) -> StockData:
        code = stock["code"].replace(".T", "")
        data = StockData(code=stock["code"], name=stock["name"])

        try:
            url = self.BASE_URL.format(code=code)
            resp = requests.get(url, headers=self.HEADERS, timeout=config.REQUEST_TIMEOUT)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")

            for row in soup.select("table.news_list tbody tr")[:5]:
                a_tag = row.find("a")
                date_td = row.find("td", class_="date")
                if a_tag:
                    href = a_tag.get("href", "")
                    data.news.append({
                        "source": "株探",
                        "title": a_tag.text.strip(),
                        "link": f"https://kabutan.jp{href}" if href.startswith("/") else href,
                        "published": date_td.text.strip() if date_td else "",
                    })

            time.sleep(config.REQUEST_DELAY)
        except Exception as e:
            print(f"[Kabutan] Error for {stock['code']}: {e}")

        return data
