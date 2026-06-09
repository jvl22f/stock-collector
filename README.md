# stock-collector

毎日自動実行する株式情報収集・AI分析ツール。指定した銘柄の株価・ニュースを自動収集し、Google Gemini API で日本語サマリーを生成します。

## 機能

- **株価取得**: Yahoo Finance から株価・出来高・前日比を取得
- **ニュース収集**: Google News RSS と株探のスクレイピングで関連ニュースを収集
- **AI分析**: Google Gemini API（gemini-2.5-flash-lite）で投資家向け日本語サマリーを自動生成
- **レポート出力**: テキストレポート（`.txt`）と CSV ファイル（`.csv`）を `output/` に保存
- **自動実行**: Mac の cron で毎朝8時（平日）に自動実行

## セットアップ

### 1. 依存パッケージのインストール

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

### 2. APIキーの設定

Google AI Studio（[aistudio.google.com](https://aistudio.google.com)）で Gemini API キーを取得し、`.env` ファイルに設定します：

```bash
echo 'GEMINI_API_KEY=AIzaSy...' > .env
```

### 3. 動作確認

```bash
venv/bin/python main.py
```

`output/` フォルダにレポートが生成されれば成功です。

## 銘柄の追加・変更

`config.py` の `STOCKS` リストを編集します：

```python
STOCKS = [
    {"code": "7203.T", "name": "トヨタ自動車"},
    {"code": "9984.T", "name": "ソフトバンクグループ"},
    # ここに追加（Yahoo Finance 形式: 日本株は末尾 .T）
]
```

## 自動実行の設定（cron）

ターミナルで `crontab -e` を開き、以下を追加します：

```
0 8 * * 1-5 cd /Users/jin/stock-collector && venv/bin/python main.py
```

## プロジェクト構成

```
stock-collector/
├── main.py                   # エントリーポイント
├── config.py                 # 監視銘柄・設定
├── requirements.txt
├── .env                      # APIキー（要作成・gitignore対象）
├── .env.example
│
├── collectors/               # データ収集
│   ├── yahoo_finance.py      # 株価・出来高（yfinance）
│   ├── kabutan.py            # 株探スクレイピング
│   └── google_news.py        # Google News RSS
│
├── analyzers/
│   └── gemini_analyzer.py    # Gemini API で日本語サマリー生成
│
├── exporters/
│   ├── text_exporter.py      # output/report_YYYYMMDD.txt
│   └── csv_exporter.py       # output/stocks_YYYYMMDD.csv
│
├── docs/
│   └── architecture.md       # アーキテクチャ図
│
├── output/                   # 生成レポート（gitignore対象）
└── logs/                     # ログファイル（gitignore対象）
```

## 出力サンプル

```
株式情報レポート　2026/06/09
============================================================

■ トヨタ自動車（7203.T）
  株価: 2830円  +0.27%
  ニュース: 5件

【AI分析】
1. 本日の株価動向
   前日比+0.27%の2830円で取引終了。出来高は22,825,800株。

2. 注目ニュース
   - AIによる株価分析記事が報じられました。
   - 米利上げ観測を背景に年初来安値更新との報道。
   - 自動車株への影響とV字回復株分析が掲載。

3. 総合所見
   地政学リスクを背景に下落局面が見られるものの本日は小幅上昇。
   今後の企業戦略と業績回復が株価の鍵となる。
```

## 依存パッケージ

| パッケージ | 用途 |
|---|---|
| `google-genai` | Gemini API |
| `yfinance` | 株価データ取得 |
| `feedparser` | Google News RSS |
| `requests` + `beautifulsoup4` + `lxml` | 株探スクレイピング |
| `python-dotenv` | .env 読み込み |
