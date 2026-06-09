import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import config
from collectors.yahoo_finance import YahooFinanceCollector
from collectors.google_news import GoogleNewsCollector
from collectors.kabutan import KabutanCollector
from collectors.kabutan_ranking import fetch_ranking
from analyzers.gemini_analyzer import analyze_stock


def run_analysis(mode, output):
    yahoo = YahooFinanceCollector()
    gnews = GoogleNewsCollector()
    kabutan = KabutanCollector()

    if mode == "ranking":
        output.insert(tk.END, "株探からランキング取得中...\n")
        stocks = fetch_ranking("値上がり率", 5)
        output.insert(tk.END, f"取得銘柄: {', '.join(s['name'] for s in stocks)}\n\n")
    else:
        stocks = config.STOCKS

    for stock in stocks:
        output.insert(tk.END, f"■ {stock['name']} ({stock['code']}) 収集中...\n")
        output.see(tk.END)

        stock_data = yahoo.collect(stock)
        news_data = gnews.collect(stock)
        kabutan_data = kabutan.collect(stock)
        stock_data.news = news_data.news + kabutan_data.news
        summary = analyze_stock(stock_data)

        price_line = (
            f"株価: {stock_data.price:.0f}円  {stock_data.change_pct:+.2f}%"
            if stock_data.price else "株価: 取得不可"
        )
        output.insert(tk.END, f"{price_line}\n")
        output.insert(tk.END, f"{summary}\n")
        output.insert(tk.END, "-" * 60 + "\n")
        output.see(tk.END)

    output.insert(tk.END, "✅ 完了\n")
    output.see(tk.END)


def on_run(mode_var, output, run_btn):
    output.delete("1.0", tk.END)
    run_btn.config(state=tk.DISABLED, text="実行中...")

    def task():
        try:
            run_analysis(mode_var.get(), output)
        finally:
            run_btn.config(state=tk.NORMAL, text="▶ 実行")

    threading.Thread(target=task, daemon=True).start()


def main():
    root = tk.Tk()
    root.title("株式情報収集ツール")
    root.geometry("700x520")

    # モード選択
    mode_var = tk.StringVar(value="registered")
    frame_top = tk.Frame(root, padx=10, pady=8)
    frame_top.pack(fill=tk.X)
    tk.Label(frame_top, text="モード:").pack(side=tk.LEFT)
    tk.Radiobutton(frame_top, text="登録銘柄を分析", variable=mode_var, value="registered").pack(side=tk.LEFT, padx=8)
    tk.Radiobutton(frame_top, text="ランキングから収集", variable=mode_var, value="ranking").pack(side=tk.LEFT)

    # 実行ボタン
    run_btn = tk.Button(
        root, text="▶ 実行", width=12,
        command=lambda: on_run(mode_var, output, run_btn)
    )
    run_btn.pack(pady=4)

    # 出力エリア
    output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 11))
    output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    main()
