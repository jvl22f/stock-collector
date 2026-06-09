# stock-collector

毎日自動実行する株式情報収集・AI分析ツール。

## 概要

- **目的**: 指定銘柄の株価・ニュース・決算情報を自動収集し、Claude API で日本語サマリーを生成する
- **実行方法**: Mac の cron で毎朝8時に自動実行（平日）
- **バージョン管理**: GitHub private リポジトリ

## 実行方法

```bash
# 仮想環境を使って実行
venv/bin/python main.py
```

## 環境設定

`.env` ファイルを作成して API キーを設定（`.env.example` を参照）:

```
ANTHROPIC_API_KEY=sk-ant-...
```

`.env` は `.gitignore` 対象なので git には含まれない。

## プロジェクト構成

```
stock-collector/
├── main.py                   # エントリーポイント
├── config.py                 # 監視銘柄・設定（ここを編集して銘柄追加）
├── requirements.txt
├── .env                      # APIキー（要作成・gitignore対象）
├── .env.example
│
├── collectors/               # データ収集
│   ├── base.py               # StockData dataclass・BaseCollector ABC
│   ├── yahoo_finance.py      # 株価・出来高（yfinance）
│   ├── kabutan.py            # 株探スクレイピング（ニュース）
│   └── google_news.py        # Google News RSS
│
├── analyzers/
│   └── claude_analyzer.py    # Claude API（claude-opus-4-8）で要約生成
│
├── exporters/
│   ├── text_exporter.py      # output/report_YYYYMMDD.txt
│   └── csv_exporter.py       # output/stocks_YYYYMMDD.csv（Excel対応 utf-8-sig）
│
├── notifiers/
│   └── base.py               # 将来のメール・LINE通知用の基底クラス
│
├── output/                   # 生成レポート（gitignore対象）
└── logs/                     # ログファイル（gitignore対象）
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

## Claude API 設定

- モデル: `claude-opus-4-8`（`config.py` の `CLAUDE_MODEL` で変更可）
- thinking: `adaptive` を使用
- `analyzers/claude_analyzer.py` でプロンプトを管理

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
| `anthropic` | Claude API |
| `yfinance` | 株価データ取得 |
| `feedparser` | Google News RSS |
| `requests` + `beautifulsoup4` + `lxml` | 株探スクレイピング |
| `python-dotenv` | .env 読み込み |

## 動作確認済み

- Yahoo Finance: トヨタ株価 2830円など正常取得
- Google News RSS: 銘柄名で日本語ニュース5件取得
- 株探: ニュース一覧スクレイピング
- Claude API: claude-opus-4-8 + adaptive thinking で日本語サマリー生成
