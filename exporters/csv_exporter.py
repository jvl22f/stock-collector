import csv
from pathlib import Path
import config


class CsvExporter:
    def export(self, results: list, date: str) -> Path:
        path = Path(config.OUTPUT_DIR) / f"stocks_{date}.csv"

        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "日付", "銘柄コード", "銘柄名",
                "株価(円)", "前日比(%)", "出来高", "ニュース数", "AI分析",
            ])

            for r in results:
                s = r["stock_data"]
                writer.writerow([
                    f"{date[:4]}/{date[4:6]}/{date[6:]}",
                    s.code,
                    s.name,
                    f"{s.price:.0f}" if s.price else "",
                    f"{s.change_pct:+.2f}" if s.change_pct is not None else "",
                    s.volume or "",
                    len(s.news),
                    r["summary"].replace("\n", " ").strip(),
                ])

        print(f"CSVレポート保存: {path}")
        return path
