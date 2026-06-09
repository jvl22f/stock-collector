from pathlib import Path
import config


class TextExporter:
    def export(self, results: list, date: str, mode: str = "stocks") -> Path:
        path = Path(config.OUTPUT_DIR) / f"report_{mode}_{date}.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"株式情報レポート　{date[:4]}/{date[4:6]}/{date[6:]}\n")
            f.write("=" * 60 + "\n\n")

            for r in results:
                s = r["stock_data"]
                f.write(f"■ {s.name}（{s.code}）\n")

                if s.price:
                    sign = "+" if s.change_pct and s.change_pct >= 0 else ""
                    change = f"{sign}{s.change_pct:.2f}%" if s.change_pct is not None else ""
                    f.write(f"  株価: {s.price:.0f}円  {change}\n")

                if s.news:
                    f.write(f"  ニュース: {len(s.news)}件\n")

                f.write("\n【AI分析】\n")
                f.write(r["summary"].strip() + "\n")
                f.write("\n" + "-" * 60 + "\n\n")

        print(f"テキストレポート保存: {path}")
        return path
