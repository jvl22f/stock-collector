# stock-collector アーキテクチャ図

## 全体の処理フロー

```mermaid
flowchart TD
    CRON["🕗 cron\n毎朝8時（平日）"]
    MAIN["main.py\n司令塔"]
    CONFIG["config.py\n設定\n・監視銘柄リスト\n・APIキー\n・出力先"]

    subgraph COLLECTORS["collectors/　データ収集"]
        YAHOO["yahoo_finance.py\n株価・出来高・前日比\n（yfinance）"]
        GNEWS["google_news.py\nニュース5件\n（Google News RSS）"]
        KABUTAN["kabutan.py\nニュース\n（株探スクレイピング）"]
        BASE["base.py\nStockData\n共通データ入れ物"]
    end

    subgraph ANALYZERS["analyzers/　AI分析"]
        CLAUDE["claude_analyzer.py\nClaude API\nclaudeの各モデルを利用\n日本語サマリー生成"]
    end

    subgraph EXPORTERS["exporters/　出力"]
        TEXT["text_exporter.py\nreport_YYYYMMDD.txt\n人間向けレポート"]
        CSV["csv_exporter.py\nstocks_YYYYMMDD.csv\nExcel対応"]
    end

    subgraph OUTPUT["output/　生成ファイル（gitignore）"]
        RFILE["report_20260609.txt"]
        CFILE["stocks_20260609.csv"]
    end

    ENV[".env\nANTHROPIC_API_KEY"]

    CRON -->|"venv/bin/python main.py"| MAIN
    CONFIG -->|"銘柄リスト読み込み"| MAIN
    ENV -->|"APIキー読み込み"| CONFIG

    MAIN -->|"銘柄ごとにループ"| YAHOO
    MAIN --> GNEWS
    MAIN --> KABUTAN

    YAHOO -->|"StockData"| BASE
    GNEWS -->|"ニュースリスト"| BASE
    KABUTAN -->|"ニュースリスト"| BASE

    BASE -->|"合体したデータ"| CLAUDE
    CLAUDE -->|"日本語サマリー"| MAIN

    MAIN --> TEXT
    MAIN --> CSV
    TEXT --> RFILE
    CSV --> CFILE
```

## フォルダ構成と役割

| パス | 役割 |
|---|---|
| `main.py` | エントリーポイント。全体の処理を順番に呼び出す司令塔 |
| `config.py` | 監視銘柄・モデル名・出力先などの設定。銘柄追加はここだけ触る |
| `collectors/base.py` | `StockData` データクラスと `BaseCollector` 抽象クラスの定義 |
| `collectors/yahoo_finance.py` | yfinance で株価・出来高・前日比を取得 |
| `collectors/google_news.py` | Google News RSS から銘柄名で日本語ニュースを取得 |
| `collectors/kabutan.py` | 株探サイトをスクレイピングしてニュースを取得 |
| `analyzers/claude_analyzer.py` | Claude API に株価＋ニュースを投げて日本語サマリーを生成 |
| `exporters/text_exporter.py` | 人間向けテキストレポートを `output/` に保存 |
| `exporters/csv_exporter.py` | Excel 対応 CSV を `output/` に保存 |
| `notifiers/` | 将来のメール・LINE通知用（現在は未実装） |
| `output/` | 生成レポート置き場（gitignore対象） |
| `logs/` | 実行ログ置き場（gitignore対象） |

## 1回の実行で起きること

```
銘柄ごとに繰り返し（現在3社）
  1. Yahoo Finance → 株価・出来高・前日比 取得
  2. Google News + 株探 → ニュース取得・合体
  3. Claude API → 日本語サマリー生成

全銘柄完了後
  → output/report_YYYYMMDD.txt 保存
  → output/stocks_YYYYMMDD.csv 保存
```
