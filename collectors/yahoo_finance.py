import yfinance as yf
from .base import BaseCollector, StockData


class YahooFinanceCollector(BaseCollector):
    def collect(self, stock: dict) -> StockData:
        data = StockData(code=stock["code"], name=stock["name"])

        try:
            ticker = yf.Ticker(stock["code"])
            hist = ticker.history(period="2d")

            if not hist.empty and len(hist) >= 1:
                latest = hist.iloc[-1]
                data.price = float(latest["Close"])
                data.volume = int(latest["Volume"])

                if len(hist) >= 2:
                    prev_close = float(hist.iloc[-2]["Close"])
                    data.change_pct = (data.price - prev_close) / prev_close * 100
                else:
                    open_price = float(latest["Open"])
                    if open_price:
                        data.change_pct = (data.price - open_price) / open_price * 100
        except Exception as e:
            print(f"[YahooFinance] Error for {stock['code']}: {e}")

        return data
