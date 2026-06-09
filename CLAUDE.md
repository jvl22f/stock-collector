# stock-collector

毎日自動実行する株式情報収集・AI分析ツール。

## 重要ルール

- **GitHub へのコミット・プッシュは必ずユーザーに確認してから実行する**

## 概要

- **目的**: 指定銘柄またはランキング上位銘柄の株価・ニュースを自動収集し、Google Gemini API で日本語サマリーを生成する
- **実行方法**: Mac の cron で毎朝8時に自動実行（平日）、または手動実行
- **バージョン管理**: GitHub private リポジトリ（https://github.com/jvl22f/stock-collector）

## 実行方法

```bash
# 手動実行
venv/bin/python main.py
```

## 環境設定

`.env` ファイルを作成して API キーを設定:

```
GEMINI_API_KEY=AIzaSy...
```

`.env` は `.gitignore` 対象なので git には含まれない。

## プロジェクト構成

```
stock-collector/
├── main.py                       # エントリーポイント
├── config.py                     # 監視銘柄・設定（ここを編集して銘柄追加）
├── requirements.txt
├── .env                          # APIキー（要作成・gitignore対象）
├── .env.example
│
├── collectors/                   # データ収集
│   ├── base.py                   # StockData dataclass・BaseCollector ABC
│   ├── yahoo_finance.py          # 株価・出来高（yfinance）
│   ├── kabutan.py                # 株探スクレイピング（ニュース）
│   ├── kabutan_ranking.py        # 株探ランキングから銘柄自動取得
│   └── google_news.py            # Google News RSS
│
├── analyzers/
│   └── gemini_analyzer.py        # Google Gemini API で日本語サマリー生成
│
├── exporters/
│   ├── text_exporter.py          # output/report_YYYYMMDD.txt
│   └── csv_exporter.py           # output/stocks_YYYYMMDD.csv（Excel対応 utf-8-sig）
│
├── notifiers/
│   └── base.py                   # 将来のメール・LINE通知用の基底クラス
│
├── docs/
│   └── architecture.md           # アーキテクチャ図（Mermaid）
│
├── output/                       # 生成レポート（gitignore対象）
└── logs/                         # ログファイル（gitignore対象）
```

## 銘柄の追加・変更

`config.py` の `STOCKS` リストを編集する:

```python
STOCKS = [
    {"code": "7203.T", "name": "トヨタ自動車"},
    {"code": "9984.T", "name": "ソフトバンクグループ"},
    # ここに追加（Yahoo Finance形式: 日本株は末尾 .T）
]
```

## ランキング収集モード

`config.py` で設定:

```python
USE_RANKING = True        # True: ランキングから自動取得 / False: STOCKS リストを使用
RANKING_TYPE = "値上がり率"  # "値上がり率" or "出来高急増"
RANKING_COUNT = 5         # 取得する銘柄数
```

## Gemini API 設定

- モデル: `gemini-2.5-flash-lite`（無料枠で動作確認済み）
- `config.py` の `GEMINI_MODEL` で変更可
- `analyzers/gemini_analyzer.py` でプロンプトを管理

## cron 設定（毎朝8時・平日のみ）

```bash
crontab -e
# 以下を追加：
0 8 * * 1-5 cd /Users/jin/stock-collector && venv/bin/python main.py
```

## 将来の拡張予定

- `notifiers/base.py` を継承してメール・LINE通知を実装
- `collectors/` に新しいデータソースを追加（掲示板・SNS等）

## 依存パッケージ

| パッケージ | 用途 |
|---|---|
| `google-genai` | Gemini API |
| `yfinance` | 株価データ取得 |
| `feedparser` | Google News RSS |
| `requests` + `beautifulsoup4` + `lxml` | 株探スクレイピング |
| `python-dotenv` | .env 読み込み |

## 動作確認済み

- Yahoo Finance: 株価・出来高・前日比 正常取得
- Google News RSS: 銘柄名で日本語ニュース取得
- 株探: ニュース一覧スクレイピング・ランキングスクレイピング
- Gemini API: gemini-2.5-flash-lite で日本語サマリー生成（無料枠）
- ランキングモード: 株探 値上がり率 Top5 を自動取得してAI分析
