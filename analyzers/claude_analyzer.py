import anthropic
import config
from collectors.base import StockData

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    return _client


def analyze_stock(data: StockData) -> str:
    prompt = _build_prompt(data)

    response = _get_client().messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=1024,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
    )

    # thinking ブロックをスキップしてテキストのみ返す
    for block in response.content:
        if block.type == "text":
            return block.text

    return ""


def _build_prompt(data: StockData) -> str:
    price_info = (
        f"{data.price:.0f}円（前日比 {data.change_pct:+.2f}%）"
        if data.price and data.change_pct is not None
        else "取得不可"
    )
    volume_info = f"{data.volume:,}株" if data.volume else "取得不可"

    news_lines = "\n".join(
        f"- [{n['source']}] {n['title']}" for n in data.news[:10]
    ) or "ニュースなし"

    return f"""以下の株式情報を分析して、投資家向けの日本語サマリーを作成してください。

【銘柄】{data.name}（{data.code}）
【株価】{price_info}
【出来高】{volume_info}
【関連ニュース】
{news_lines}

以下の形式でまとめてください：
1. 本日の株価動向（1〜2文）
2. 注目ニュース（最大3件、各1文で要約）
3. 総合所見（2〜3文）
"""
