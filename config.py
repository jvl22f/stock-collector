import os
from dotenv import load_dotenv

load_dotenv()

# 監視銘柄リスト（Yahoo Finance形式: 日本株は末尾に .T）
STOCKS = [
    {"code": "7203.T", "name": "トヨタ自動車"},
    {"code": "9984.T", "name": "ソフトバンクグループ"},
    {"code": "6758.T", "name": "ソニーグループ"},
]

# Claude API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-opus-4-8"

# 出力先
OUTPUT_DIR = "output"
LOG_DIR = "logs"

# スクレイピング設定
REQUEST_DELAY = 2    # リクエスト間隔（秒）
REQUEST_TIMEOUT = 10
