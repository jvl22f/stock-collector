import logging
import sys
from datetime import datetime
from pathlib import Path

import config
from collectors.yahoo_finance import YahooFinanceCollector
from collectors.google_news import GoogleNewsCollector
from collectors.kabutan import KabutanCollector
from analyzers.gemini_analyzer import analyze_stock
from exporters.text_exporter import TextExporter
from exporters.csv_exporter import CsvExporter

Path(config.LOG_DIR).mkdir(exist_ok=True)
Path(config.OUTPUT_DIR).mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{config.LOG_DIR}/stock_collector.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


def run():
    today = datetime.now().strftime("%Y%m%d")
    log.info(f"===== 株式情報収集開始: {today} =====")

    yahoo = YahooFinanceCollector()
    gnews = GoogleNewsCollector()
    kabutan = KabutanCollector()
    text_exp = TextExporter()
    csv_exp = CsvExporter()

    results = []

    for stock in config.STOCKS:
        log.info(f"収集中: {stock['name']} ({stock['code']})")

        stock_data = yahoo.collect(stock)

        news_data = gnews.collect(stock)
        kabutan_data = kabutan.collect(stock)
        stock_data.news = news_data.news + kabutan_data.news

        log.info(f"Claude分析中: {stock['name']} (ニュース {len(stock_data.news)}件)")
        summary = analyze_stock(stock_data)

        results.append({"stock_data": stock_data, "summary": summary})
        log.info(f"完了: {stock['name']}")

    text_exp.export(results, today)
    csv_exp.export(results, today)

    log.info("===== 収集完了 =====")


if __name__ == "__main__":
    run()
