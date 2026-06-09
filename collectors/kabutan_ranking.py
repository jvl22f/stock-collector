import time
import requests
from bs4 import BeautifulSoup
import config

RANKING_URLS = {
    "値上がり率": "https://kabutan.jp/warning/?mode=2_1",
    "出来高急増": "https://kabutan.jp/warning/?mode=2_3",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


def fetch_ranking(ranking_type: str = "値上がり率", count: int = 10) -> list[dict]:
    url = RANKING_URLS.get(ranking_type, RANKING_URLS["値上がり率"])
    stocks = []

    try:
        resp = requests.get(url, headers=HEADERS, timeout=config.REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        table = soup.find("table", class_="stock_table")
        if not table:
            return stocks

        for row in table.select("tbody tr"):
            code_tag = row.select_one("td.tac a")
            name_tag = row.select_one("th.tal")
            if not code_tag or not name_tag:
                continue

            code = code_tag.text.strip()
            name = name_tag.text.strip()
            if code.isdigit():
                stocks.append({"code": f"{code}.T", "name": name})

            if len(stocks) >= count:
                break

        time.sleep(config.REQUEST_DELAY)
    except Exception as e:
        print(f"[KabutanRanking] Error: {e}")

    return stocks
