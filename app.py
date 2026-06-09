import streamlit as st
import config
from collectors.yahoo_finance import YahooFinanceCollector
from collectors.google_news import GoogleNewsCollector
from collectors.kabutan import KabutanCollector
from collectors.kabutan_ranking import fetch_ranking
from analyzers.gemini_analyzer import analyze_stock

st.set_page_config(page_title="株式情報収集ツール", page_icon="📈", layout="wide")
st.title("📈 株式情報収集ツール")

# ---- サイドバー: モード選択 ----
with st.sidebar:
    st.header("⚙️ 設定")

    mode = st.radio(
        "収集モード",
        ["登録銘柄を分析", "ランキングから収集"],
        index=0,
    )

    if mode == "登録銘柄を分析":
        stock_options = {f"{s['name']} ({s['code']})": s for s in config.STOCKS}
        selected = st.multiselect(
            "分析する銘柄",
            options=list(stock_options.keys()),
            default=list(stock_options.keys()),
        )
        stocks_to_run = [stock_options[k] for k in selected]
    else:
        ranking_type = st.selectbox("ランキング種別", ["値上がり率", "出来高急増"])
        ranking_count = st.slider("取得件数", min_value=3, max_value=20, value=5)
        stocks_to_run = None  # 実行時に取得

    run_btn = st.button("▶ 実行", type="primary", use_container_width=True)

# ---- メイン: 結果表示 ----
if run_btn:
    yahoo = YahooFinanceCollector()
    gnews = GoogleNewsCollector()
    kabutan = KabutanCollector()

    if mode == "ランキングから収集":
        with st.spinner(f"株探から{ranking_type}ランキングを取得中..."):
            stocks_to_run = fetch_ranking(ranking_type, ranking_count)
        st.info(f"**{ranking_type} Top{ranking_count}**: " + "、".join(s["name"] for s in stocks_to_run))

    if not stocks_to_run:
        st.warning("銘柄が選択されていません。")
        st.stop()

    progress = st.progress(0, text="収集開始...")
    total = len(stocks_to_run)

    for i, stock in enumerate(stocks_to_run):
        progress.progress((i) / total, text=f"収集中: {stock['name']} ({i+1}/{total})")

        with st.spinner(f"{stock['name']} のデータ収集・AI分析中..."):
            stock_data = yahoo.collect(stock)
            news_data = gnews.collect(stock)
            kabutan_data = kabutan.collect(stock)
            stock_data.news = news_data.news + kabutan_data.news
            summary = analyze_stock(stock_data)

        # 結果カード
        with st.expander(
            f"{'🟢' if stock_data.change_pct and stock_data.change_pct >= 0 else '🔴'} "
            f"**{stock['name']}** ({stock['code']})　"
            f"{f'{stock_data.price:.0f}円　{stock_data.change_pct:+.2f}%' if stock_data.price else '株価取得不可'}",
            expanded=True,
        ):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.metric("株価", f"{stock_data.price:.0f}円" if stock_data.price else "—",
                          f"{stock_data.change_pct:+.2f}%" if stock_data.change_pct is not None else None)
                st.metric("出来高", f"{stock_data.volume:,}株" if stock_data.volume else "—")
                st.metric("ニュース件数", f"{len(stock_data.news)}件")

                if stock_data.news:
                    st.markdown("**関連ニュース**")
                    for n in stock_data.news[:5]:
                        st.markdown(f"- [{n['title']}]({n['link']})")

            with col2:
                st.markdown("**AI分析（Gemini）**")
                st.markdown(summary)

        progress.progress((i + 1) / total, text=f"完了: {stock['name']} ({i+1}/{total})")

    progress.progress(1.0, text="✅ すべて完了")
    st.success(f"{total}銘柄の分析が完了しました。")
