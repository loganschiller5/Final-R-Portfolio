# ============================================================
# STOCK ANALYTICS & PORTFOLIO DASHBOARD
# FIN 330 Final Project — Professional Grade Fintech App
# ============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EquityLens — Stock Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — DARK FINTECH THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base & Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 100%; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p {
    color: #8b949e !important;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f0f6fc !important;
}

/* ── Metric Cards ── */
[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    transition: border-color 0.2s;
}
[data-testid="metric-container"]:hover {
    border-color: #388bfd;
}
[data-testid="metric-container"] label {
    color: #8b949e !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #f0f6fc !important;
    font-size: 1.5rem !important;
    font-weight: 600;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #21262d;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8b949e;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 500;
    font-size: 0.875rem;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: #21262d !important;
    color: #f0f6fc !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #238636, #2ea043);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    font-size: 0.875rem;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2ea043, #3fb950);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(46,160,67,0.4);
}

/* ── Inputs ── */
.stTextInput input, .stSelectbox select, .stMultiSelect > div {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #f0f6fc !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* ── Dividers ── */
hr { border-color: #21262d; }

/* ── Custom card containers ── */
.card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.card-title {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8b949e;
    margin-bottom: 0.4rem;
    font-weight: 600;
}
.card-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f0f6fc;
}
.card-sub {
    font-size: 0.78rem;
    color: #8b949e;
    margin-top: 0.2rem;
}

/* ── Signal badges ── */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-buy   { background: #0d4429; color: #3fb950; border: 1px solid #238636; }
.badge-sell  { background: #4a1010; color: #f85149; border: 1px solid #da3633; }
.badge-hold  { background: #2a2009; color: #e3b341; border: 1px solid #9e6a03; }
.badge-up    { color: #3fb950; }
.badge-down  { color: #f85149; }

/* ── Section header ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f0f6fc;
    border-bottom: 1px solid #21262d;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

/* ── Sidebar logo area ── */
.sidebar-logo {
    font-size: 1.4rem;
    font-weight: 700;
    color: #f0f6fc;
    letter-spacing: -0.03em;
}
.sidebar-logo span { color: #388bfd; }

/* ── Alert / callout ── */
.info-box {
    background: #0d2137;
    border: 1px solid #1f6feb;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    color: #79c0ff;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

@st.cache_data(ttl=300, show_spinner=False)
def fetch_stock_data(ticker: str, period: str = "6mo") -> pd.DataFrame:
    try:
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.index = pd.to_datetime(df.index)
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=300, show_spinner=False)
def fetch_info(ticker: str) -> dict:
    try:
        return yf.Ticker(ticker).info
    except Exception:
        return {}

def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - 100 / (1 + rs)

def compute_macd(series: pd.Series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def compute_bollinger(series: pd.Series, window: int = 20):
    mid = series.rolling(window).mean()
    std = series.rolling(window).std()
    return mid + 2 * std, mid, mid - 2 * std

def trend_analysis(df: pd.DataFrame) -> dict:
    close = df["Close"].squeeze()
    price = float(close.iloc[-1])
    ma20  = float(close.rolling(20).mean().iloc[-1])
    ma50  = float(close.rolling(50).mean().iloc[-1])

    if price > ma20 > ma50:
        trend = "Strong Uptrend"
        trend_color = "#3fb950"
    elif price < ma20 < ma50:
        trend = "Strong Downtrend"
        trend_color = "#f85149"
    else:
        trend = "Mixed / Sideways"
        trend_color = "#e3b341"

    return {"price": price, "ma20": ma20, "ma50": ma50,
            "trend": trend, "trend_color": trend_color}

def momentum_analysis(df: pd.DataFrame) -> dict:
    close = df["Close"].squeeze()
    rsi_series = compute_rsi(close)
    rsi = float(rsi_series.iloc[-1])

    if rsi > 70:
        signal = "Overbought"; sig_color = "#f85149"
    elif rsi < 30:
        signal = "Oversold";   sig_color = "#3fb950"
    else:
        signal = "Neutral";    sig_color = "#8b949e"

    return {"rsi": rsi, "signal": signal, "sig_color": sig_color, "rsi_series": rsi_series}

def volatility_analysis(df: pd.DataFrame) -> dict:
    close = df["Close"].squeeze()
    daily_ret = close.pct_change().dropna()
    vol = float(daily_ret.rolling(20).std().iloc[-1] * np.sqrt(252) * 100)

    if vol > 40:
        label = "High"; vol_color = "#f85149"
    elif vol > 25:
        label = "Medium"; vol_color = "#e3b341"
    else:
        label = "Low"; vol_color = "#3fb950"

    return {"vol": vol, "label": label, "vol_color": vol_color}

def recommendation(trend: dict, momentum: dict, volatility: dict) -> tuple[str, str, str]:
    t = trend["trend"]
    r = momentum["rsi"]
    v = volatility["vol"]

    if "Uptrend" in t and r < 70 and v < 50:
        rec = "BUY"
        color = "#3fb950"
        reason = f"Price above both MAs, RSI neutral at {r:.1f}, manageable volatility {v:.1f}%."
    elif "Downtrend" in t or r > 75:
        rec = "SELL"
        color = "#f85149"
        reason = f"Bearish trend structure or overbought RSI {r:.1f}. Consider reducing exposure."
    else:
        rec = "HOLD"
        color = "#e3b341"
        reason = f"Mixed signals. RSI at {r:.1f}, trend unclear. Monitor for confirmation."

    return rec, color, reason

def portfolio_metrics(weights: dict, tickers: list, period: str = "1y") -> dict:
    raw = {}
    for t in tickers:
        df = fetch_stock_data(t, period)
        if df.empty:
            continue
        raw[t] = df["Close"].squeeze()

    if not raw:
        return {}

    prices = pd.DataFrame(raw).dropna()
    returns = prices.pct_change().dropna()

    w = np.array([weights[t] for t in prices.columns])
    port_ret = returns.dot(w)

    bench = fetch_stock_data("SPY", period)
    bench_ret = bench["Close"].squeeze().pct_change().dropna() if not bench.empty else None

    total_ret     = float((1 + port_ret).prod() - 1)
    ann_vol       = float(port_ret.std() * np.sqrt(252))
    sharpe        = float((port_ret.mean() * 252) / ann_vol) if ann_vol > 0 else 0
    bench_total   = float((1 + bench_ret).prod() - 1) if bench_ret is not None else 0
    outperf       = total_ret - bench_total
    cumulative    = (1 + port_ret).cumprod()
    bench_cum     = (1 + bench_ret).cumprod() if bench_ret is not None else None

    return {
        "total_ret": total_ret,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
        "bench_total": bench_total,
        "outperf": outperf,
        "cumulative": cumulative,
        "bench_cum": bench_cum,
        "returns": returns,
        "port_ret": port_ret,
        "prices": prices,
    }

def fmt_pct(v: float, signed: bool = True) -> str:
    sign = "+" if signed and v >= 0 else ""
    return f"{sign}{v*100:.2f}%"

def fmt_num(v: float, prefix: str = "") -> str:
    if v >= 1e12: return f"{prefix}{v/1e12:.2f}T"
    if v >= 1e9:  return f"{prefix}{v/1e9:.2f}B"
    if v >= 1e6:  return f"{prefix}{v/1e6:.2f}M"
    return f"{prefix}{v:,.0f}"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#8b949e", size=12),
    xaxis=dict(gridcolor="#21262d", zeroline=False, showline=False),
    yaxis=dict(gridcolor="#21262d", zeroline=False, showline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#21262d", borderwidth=1),
    margin=dict(l=10, r=10, t=30, b=10),
    hovermode="x unified",
)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">Equity<span>Lens</span> 📈</div>', unsafe_allow_html=True)
    st.caption("Professional Stock & Portfolio Analytics")
    st.divider()

    page = st.radio(
        "Navigation",
        ["📊 Stock Analysis", "💼 Portfolio Dashboard", "🔍 Stock Screener"],
        label_visibility="collapsed",
    )

    st.divider()

    if page == "📊 Stock Analysis":
        st.markdown("**STOCK ANALYSIS**")
        ticker_input = st.text_input("Ticker Symbol", value="AAPL", placeholder="e.g. AAPL").upper().strip()
        period_map   = {"1 Month": "1mo", "3 Months": "3mo", "6 Months": "6mo", "1 Year": "1y", "2 Years": "2y"}
        period_label = st.selectbox("Time Period", list(period_map.keys()), index=2)
        period_code  = period_map[period_label]
        run_analysis = st.button("🔍  Analyze Stock")

    elif page == "💼 Portfolio Dashboard":
        st.markdown("**PORTFOLIO SETUP**")
        default_stocks  = "AAPL, MSFT, GOOGL, NVDA, JPM"
        portfolio_input = st.text_area("Tickers (comma-separated)", value=default_stocks, height=80)
        portfolio_tickers = [t.strip().upper() for t in portfolio_input.split(",") if t.strip()]

        st.markdown("**WEIGHTS**")
        weights = {}
        n = len(portfolio_tickers)
        remaining = 1.0
        for i, t in enumerate(portfolio_tickers):
            if i < n - 1:
                default_w = round(1 / n, 2)
                w = st.slider(t, 0.0, 1.0, default_w, 0.01, key=f"w_{t}")
                weights[t] = w
                remaining -= w
            else:
                weights[t] = max(round(remaining, 2), 0.0)
                st.metric(t, f"{weights[t]*100:.0f}%", "remainder")

        total_w = sum(weights.values())
        if abs(total_w - 1.0) > 0.01:
            st.warning(f"Weights sum to {total_w:.2f}. Should be 1.00.")

        port_period_map   = {"6 Months": "6mo", "1 Year": "1y", "2 Years": "2y"}
        port_period_label = st.selectbox("Analysis Period", list(port_period_map.keys()), index=1)
        port_period_code  = port_period_map[port_period_label]
        run_portfolio     = st.button("📊  Run Portfolio Analysis")

    elif page == "🔍 Stock Screener":
        st.markdown("**SCREENER**")
        screener_tickers_str = st.text_area(
            "Compare Tickers",
            value="AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META, JPM, V, JNJ",
            height=120
        )
        screener_tickers = [t.strip().upper() for t in screener_tickers_str.split(",") if t.strip()]
        run_screener = st.button("🔍  Screen Stocks")

    st.divider()
    st.caption("Data via Yahoo Finance · Refreshes every 5 min")


# ─────────────────────────────────────────────
# PAGE 1 — STOCK ANALYSIS
# ─────────────────────────────────────────────
if page == "📊 Stock Analysis":

    if not run_analysis:
        # Hero / landing state
        st.markdown("""
        <div style='text-align:center; padding: 4rem 0 2rem 0;'>
            <div style='font-size:3rem;'>📈</div>
            <h1 style='color:#f0f6fc; font-weight:700; font-size:2.2rem; margin:0.5rem 0;'>
                EquityLens Stock Analytics
            </h1>
            <p style='color:#8b949e; font-size:1.05rem; max-width:520px; margin:auto;'>
                Enter a ticker in the sidebar and click <strong style='color:#3fb950'>Analyze Stock</strong>
                to get a full technical analysis, signals, and trading recommendation.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Quick-access popular tickers
        st.markdown("---")
        st.markdown('<p style="text-align:center;color:#8b949e;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;">Popular Tickers</p>', unsafe_allow_html=True)
        cols = st.columns(8)
        for c, t in zip(cols, ["AAPL","MSFT","GOOGL","NVDA","TSLA","AMZN","META","JPM"]):
            c.markdown(f"""
            <div style='background:#161b22;border:1px solid #21262d;border-radius:8px;
                        padding:8px;text-align:center;cursor:pointer;font-weight:600;color:#79c0ff;'>
                {t}
            </div>""", unsafe_allow_html=True)
        st.stop()

    # ── Fetch data ──
    with st.spinner(f"Fetching data for {ticker_input}…"):
        df   = fetch_stock_data(ticker_input, period_code)
        info = fetch_info(ticker_input)

    if df.empty:
        st.error(f"❌ No data found for **{ticker_input}**. Check the ticker and try again.")
        st.stop()

    close = df["Close"].squeeze()

    # ── Compute indicators ──
    trend    = trend_analysis(df)
    momentum = momentum_analysis(df)
    vol      = volatility_analysis(df)
    rec, rec_color, rec_reason = recommendation(trend, momentum, vol)
    macd, macd_sig, macd_hist  = compute_macd(close)
    bb_upper, bb_mid, bb_lower = compute_bollinger(close)

    price_now = trend["price"]
    price_ago = float(close.iloc[0])
    pct_change = (price_now - price_ago) / price_ago

    # ── Header ──
    company = info.get("longName", ticker_input)
    sector  = info.get("sector", "—")
    industry= info.get("industry", "—")
    mktcap  = info.get("marketCap", 0)

    col_title, col_badge = st.columns([3, 1])
    with col_title:
        st.markdown(f"""
        <h1 style='color:#f0f6fc;font-weight:700;font-size:1.8rem;margin:0;'>{company}</h1>
        <p style='color:#8b949e;font-size:0.85rem;margin:2px 0 0 2px;'>
            <strong style='color:#388bfd;'>{ticker_input}</strong> &nbsp;·&nbsp;
            {sector} &nbsp;·&nbsp; {industry}
        </p>
        """, unsafe_allow_html=True)
    with col_badge:
        badge_cls = {"BUY":"badge-buy","SELL":"badge-sell","HOLD":"badge-hold"}[rec]
        st.markdown(f"""
        <div style='text-align:right;padding-top:0.5rem;'>
            <span class='badge {badge_cls}' style='font-size:1rem;padding:6px 24px;'>
                ⬟ {rec}
            </span>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── KPI Row ──
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    arrow = "▲" if pct_change >= 0 else "▼"
    chg_color = "#3fb950" if pct_change >= 0 else "#f85149"

    kpi1.metric("Current Price",   f"${price_now:,.2f}", fmt_pct(pct_change))
    kpi2.metric("Market Cap",       fmt_num(mktcap, "$") if mktcap else "—")
    kpi3.metric("20-Day MA",        f"${trend['ma20']:,.2f}")
    kpi4.metric("50-Day MA",        f"${trend['ma50']:,.2f}")
    kpi5.metric("RSI (14)",         f"{momentum['rsi']:.1f}", momentum["signal"])

    st.markdown("")

    # ── TABS ──
    tab_chart, tab_technical, tab_summary = st.tabs(
        ["📈  Price Chart", "🔬  Technical Indicators", "📋  Analysis Summary"]
    )

    # ── TAB 1: Price Chart ──
    with tab_chart:
        chart_type = st.radio("Chart Type", ["Candlestick", "Line", "Area"], horizontal=True)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.72, 0.28], vertical_spacing=0.03)

        if chart_type == "Candlestick":
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"].squeeze(), high=df["High"].squeeze(),
                low=df["Low"].squeeze(),   close=close,
                increasing_line_color="#3fb950", decreasing_line_color="#f85149",
                name="Price", showlegend=False,
            ), row=1, col=1)
        elif chart_type == "Line":
            fig.add_trace(go.Scatter(
                x=df.index, y=close, name="Price",
                line=dict(color="#388bfd", width=2), showlegend=False,
            ), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(
                x=df.index, y=close, name="Price",
                fill="tozeroy",
                fillcolor="rgba(56,139,253,0.10)",
                line=dict(color="#388bfd", width=2), showlegend=False,
            ), row=1, col=1)

        # MAs
        ma20_s = close.rolling(20).mean()
        ma50_s = close.rolling(50).mean()
        fig.add_trace(go.Scatter(x=df.index, y=ma20_s, name="MA 20",
                                 line=dict(color="#e3b341", width=1.5, dash="dot")), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=ma50_s, name="MA 50",
                                 line=dict(color="#da3633", width=1.5, dash="dot")), row=1, col=1)

        # Bollinger Bands
        fig.add_trace(go.Scatter(x=df.index, y=bb_upper, name="BB Upper",
                                 line=dict(color="#6e40c9", width=1, dash="dash")), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=bb_lower, name="BB Lower",
                                 line=dict(color="#6e40c9", width=1, dash="dash"),
                                 fill="tonexty", fillcolor="rgba(110,64,201,0.05)"), row=1, col=1)

        # Volume
        vol_colors = ["#3fb950" if c >= o else "#f85149"
                      for c, o in zip(df["Close"].squeeze(), df["Open"].squeeze())]
        fig.add_trace(go.Bar(x=df.index, y=df["Volume"].squeeze(),
                             marker_color=vol_colors, name="Volume",
                             opacity=0.6, showlegend=False), row=2, col=1)

        fig.update_layout(**PLOTLY_LAYOUT, height=520,
                          yaxis2=dict(gridcolor="#21262d", title="Volume",
                                      title_font=dict(size=10), zeroline=False))
        fig.update_xaxes(rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── TAB 2: Technical Indicators ──
    with tab_technical:
        col_rsi, col_macd = st.columns(2)

        with col_rsi:
            st.markdown('<p class="section-header">RSI (14)</p>', unsafe_allow_html=True)
            rsi_s = momentum["rsi_series"]
            fig_rsi = go.Figure()
            fig_rsi.add_hrect(y0=70, y1=100, fillcolor="rgba(248,81,73,0.08)", line_width=0)
            fig_rsi.add_hrect(y0=0,  y1=30,  fillcolor="rgba(63,185,80,0.08)", line_width=0)
            fig_rsi.add_hline(y=70, line_dash="dot", line_color="#f85149", line_width=1)
            fig_rsi.add_hline(y=30, line_dash="dot", line_color="#3fb950", line_width=1)
            fig_rsi.add_trace(go.Scatter(
                x=rsi_s.index, y=rsi_s, name="RSI",
                line=dict(color="#79c0ff", width=2),
            ))
            fig_rsi.update_layout(**PLOTLY_LAYOUT, height=280,
                                  yaxis=dict(range=[0,100], gridcolor="#21262d", zeroline=False))
            st.plotly_chart(fig_rsi, use_container_width=True)

        with col_macd:
            st.markdown('<p class="section-header">MACD (12/26/9)</p>', unsafe_allow_html=True)
            hist_colors = ["#3fb950" if v >= 0 else "#f85149" for v in macd_hist.fillna(0)]
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Bar(x=df.index, y=macd_hist, name="Histogram",
                                      marker_color=hist_colors, opacity=0.7))
            fig_macd.add_trace(go.Scatter(x=df.index, y=macd, name="MACD",
                                          line=dict(color="#388bfd", width=2)))
            fig_macd.add_trace(go.Scatter(x=df.index, y=macd_sig, name="Signal",
                                          line=dict(color="#f85149", width=1.5, dash="dot")))
            fig_macd.update_layout(**PLOTLY_LAYOUT, height=280)
            st.plotly_chart(fig_macd, use_container_width=True)

        # Volatility gauge
        st.markdown('<p class="section-header">20-Day Annualized Volatility</p>', unsafe_allow_html=True)
        fig_vol = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=vol["vol"],
            number={"suffix": "%", "font": {"color": "#f0f6fc", "size": 40}},
            gauge={
                "axis": {"range": [0, 80], "tickcolor": "#8b949e"},
                "bar": {"color": vol["vol_color"], "thickness": 0.3},
                "bgcolor": "#161b22",
                "steps": [
                    {"range": [0, 25],  "color": "#0d2a1a"},
                    {"range": [25, 40], "color": "#2a2009"},
                    {"range": [40, 80], "color": "#4a1010"},
                ],
                "threshold": {"line": {"color": "#f0f6fc", "width": 2},
                              "thickness": 0.8, "value": vol["vol"]},
            },
            title={"text": f"Volatility Level: <b>{vol['label']}</b>",
                   "font": {"color": "#8b949e", "size": 14}},
        ))
        fig_vol.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=260,
                              font=dict(color="#8b949e", family="Inter"),
                              margin=dict(l=20, r=20, t=20, b=10))
        st.plotly_chart(fig_vol, use_container_width=True)

    # ── TAB 3: Analysis Summary ──
    with tab_summary:
        c1, c2, c3 = st.columns(3)

        with c1:
            color = trend["trend_color"]
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>📊 Trend Analysis</div>
                <div class='card-value' style='color:{color};font-size:1.1rem;'>{trend['trend']}</div>
                <div class='card-sub' style='margin-top:0.8rem;'>
                    <span style='color:#8b949e;'>Price:</span>
                    <strong style='color:#f0f6fc;'> ${price_now:,.2f}</strong><br>
                    <span style='color:#8b949e;'>20-Day MA:</span>
                    <strong style='color:#e3b341;'> ${trend['ma20']:,.2f}</strong><br>
                    <span style='color:#8b949e;'>50-Day MA:</span>
                    <strong style='color:#da3633;'> ${trend['ma50']:,.2f}</strong>
                </div>
            </div>""", unsafe_allow_html=True)

        with c2:
            mc = momentum["sig_color"]
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>⚡ Momentum (RSI)</div>
                <div class='card-value' style='color:{mc};font-size:1.1rem;'>{momentum['signal']}</div>
                <div class='card-sub' style='margin-top:0.8rem;'>
                    <span style='color:#8b949e;'>RSI Value:</span>
                    <strong style='color:#f0f6fc;'> {momentum['rsi']:.2f}</strong><br>
                    <span style='color:#3fb950;'>＜30 = Oversold</span><br>
                    <span style='color:#f85149;'>＞70 = Overbought</span>
                </div>
            </div>""", unsafe_allow_html=True)

        with c3:
            vc = vol["vol_color"]
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>🌊 Volatility</div>
                <div class='card-value' style='color:{vc};font-size:1.1rem;'>{vol['label']}</div>
                <div class='card-sub' style='margin-top:0.8rem;'>
                    <span style='color:#8b949e;'>Ann. Volatility:</span>
                    <strong style='color:#f0f6fc;'> {vol['vol']:.1f}%</strong><br>
                    <span style='color:#3fb950;'>＜25% = Low</span><br>
                    <span style='color:#e3b341;'>25–40% = Medium</span><br>
                    <span style='color:#f85149;'>＞40% = High</span>
                </div>
            </div>""", unsafe_allow_html=True)

        # Final recommendation box
        badge_cls = {"BUY":"badge-buy","SELL":"badge-sell","HOLD":"badge-hold"}[rec]
        st.markdown(f"""
        <div style='background:linear-gradient(135deg, #161b22, #0d1117);
                    border:1px solid {rec_color}33;border-radius:12px;
                    padding:1.5rem 2rem;margin-top:1rem;'>
            <div style='display:flex;align-items:center;gap:1rem;'>
                <span class='badge {badge_cls}' style='font-size:1.2rem;padding:8px 28px;'>
                    {rec}
                </span>
                <div>
                    <div style='color:#f0f6fc;font-weight:600;font-size:1rem;margin-bottom:0.25rem;'>
                        Trading Recommendation
                    </div>
                    <div style='color:#8b949e;font-size:0.875rem;'>{rec_reason}</div>
                </div>
            </div>
            <p style='color:#8b949e;font-size:0.72rem;margin:1rem 0 0 0;border-top:1px solid #21262d;padding-top:0.75rem;'>
                ⚠ This recommendation is generated from technical indicators only and does not
                constitute financial advice. Always conduct your own due diligence.
            </p>
        </div>""", unsafe_allow_html=True)

        # Company fundamentals
        if info:
            st.markdown("---")
            st.markdown('<p class="section-header">Company Fundamentals</p>', unsafe_allow_html=True)
            f1, f2, f3, f4 = st.columns(4)
            f1.metric("P/E Ratio",       f"{info.get('trailingPE', 0):.1f}x"  if info.get('trailingPE') else "—")
            f2.metric("EPS (TTM)",        f"${info.get('trailingEps', 0):.2f}" if info.get('trailingEps') else "—")
            f3.metric("52W High",         f"${info.get('fiftyTwoWeekHigh', 0):,.2f}" if info.get('fiftyTwoWeekHigh') else "—")
            f4.metric("52W Low",          f"${info.get('fiftyTwoWeekLow', 0):,.2f}"  if info.get('fiftyTwoWeekLow')  else "—")


# ─────────────────────────────────────────────
# PAGE 2 — PORTFOLIO DASHBOARD
# ─────────────────────────────────────────────
elif page == "💼 Portfolio Dashboard":

    if not run_portfolio:
        st.markdown("""
        <div style='text-align:center;padding:3rem 0 2rem 0;'>
            <div style='font-size:3rem;'>💼</div>
            <h1 style='color:#f0f6fc;font-weight:700;font-size:2rem;margin:0.5rem 0;'>
                Portfolio Dashboard
            </h1>
            <p style='color:#8b949e;font-size:1rem;max-width:500px;margin:auto;'>
                Configure your portfolio in the sidebar — add tickers, set weights, choose a period,
                then click <strong style='color:#3fb950'>Run Portfolio Analysis</strong>.
            </p>
        </div>""", unsafe_allow_html=True)
        st.stop()

    with st.spinner("Running portfolio analysis…"):
        metrics = portfolio_metrics(weights, portfolio_tickers, port_period_code)

    if not metrics:
        st.error("Could not fetch data for the selected tickers. Please verify them.")
        st.stop()

    # ── Header ──
    st.markdown(f"""
    <h1 style='color:#f0f6fc;font-weight:700;font-size:1.8rem;margin:0 0 0.25rem 0;'>
        Portfolio Overview
    </h1>
    <p style='color:#8b949e;font-size:0.85rem;'>
        {" · ".join(portfolio_tickers)} &nbsp;|&nbsp; Period: {port_period_label} &nbsp;|&nbsp;
        Benchmark: SPY
    </p>""", unsafe_allow_html=True)
    st.markdown("---")

    # ── KPI Row ──
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Return",       fmt_pct(metrics["total_ret"]),
              f"vs SPY {fmt_pct(metrics['bench_total'])}")
    k2.metric("Benchmark (SPY)",    fmt_pct(metrics["bench_total"]))
    k3.metric("Outperformance",     fmt_pct(metrics["outperf"]),
              "Alpha vs SPY")
    k4.metric("Ann. Volatility",    f"{metrics['ann_vol']*100:.1f}%")
    k5.metric("Sharpe Ratio",       f"{metrics['sharpe']:.2f}",
              "≥1 = Good · ≥2 = Excellent")

    st.markdown("")

    tab_perf, tab_alloc, tab_risk, tab_stocks = st.tabs(
        ["📈  Performance", "🥧  Allocation", "⚡  Risk Analysis", "🔬  Stock Breakdown"]
    )

    # ── TAB: Performance ──
    with tab_perf:
        cum   = metrics["cumulative"]
        bench = metrics["bench_cum"]

        fig_perf = go.Figure()
        fig_perf.add_trace(go.Scatter(
            x=cum.index, y=(cum - 1) * 100,
            name="My Portfolio", fill="tozeroy",
            fillcolor="rgba(56,139,253,0.08)",
            line=dict(color="#388bfd", width=2.5),
        ))
        if bench is not None:
            fig_perf.add_trace(go.Scatter(
                x=bench.index, y=(bench - 1) * 100,
                name="SPY (Benchmark)",
                line=dict(color="#8b949e", width=1.5, dash="dot"),
            ))
        fig_perf.add_hline(y=0, line_color="#21262d", line_width=1)
        fig_perf.update_layout(**PLOTLY_LAYOUT, height=380,
                               yaxis=dict(ticksuffix="%", gridcolor="#21262d", zeroline=False),
                               title=dict(text="Cumulative Return vs Benchmark",
                                          font=dict(color="#f0f6fc", size=14)))
        st.plotly_chart(fig_perf, use_container_width=True)

        # Rolling Sharpe
        port_ret = metrics["port_ret"]
        rolling_sharpe = (port_ret.rolling(21).mean() / port_ret.rolling(21).std()) * np.sqrt(252)
        fig_rs = go.Figure()
        fig_rs.add_trace(go.Scatter(x=rolling_sharpe.index, y=rolling_sharpe,
                                    name="Rolling Sharpe (21d)",
                                    line=dict(color="#6e40c9", width=2)))
        fig_rs.add_hline(y=1, line_dash="dot", line_color="#3fb950", line_width=1)
        fig_rs.add_hline(y=0, line_color="#21262d", line_width=1)
        fig_rs.update_layout(**PLOTLY_LAYOUT, height=220,
                             title=dict(text="Rolling 21-Day Sharpe Ratio",
                                        font=dict(color="#f0f6fc", size=14)))
        st.plotly_chart(fig_rs, use_container_width=True)

    # ── TAB: Allocation ──
    with tab_alloc:
        col_pie, col_bar = st.columns(2)

        with col_pie:
            labels = list(weights.keys())
            vals   = [weights[t] * 100 for t in labels]
            colors = ["#388bfd","#3fb950","#e3b341","#f85149","#6e40c9",
                      "#da3633","#79c0ff","#7ee787","#d2a679"][:len(labels)]

            fig_pie = go.Figure(go.Pie(
                labels=labels, values=vals,
                hole=0.55,
                marker=dict(colors=colors, line=dict(color="#0d1117", width=2)),
                textinfo="label+percent",
                textfont=dict(color="#f0f6fc", size=12),
            ))
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False, height=320,
                margin=dict(l=10, r=10, t=30, b=10),
                title=dict(text="Portfolio Allocation", font=dict(color="#f0f6fc", size=14)),
                annotations=[dict(text="Weights", x=0.5, y=0.5,
                                  font=dict(size=13, color="#8b949e"), showarrow=False)],
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_bar:
            returns_by_stock = {}
            for t in portfolio_tickers:
                df_t = fetch_stock_data(t, port_period_code)
                if not df_t.empty:
                    c = df_t["Close"].squeeze()
                    returns_by_stock[t] = float((c.iloc[-1] / c.iloc[0]) - 1) * 100

            sorted_ret = dict(sorted(returns_by_stock.items(), key=lambda x: x[1], reverse=True))
            bar_colors = ["#3fb950" if v >= 0 else "#f85149" for v in sorted_ret.values()]

            fig_bar = go.Figure(go.Bar(
                x=list(sorted_ret.keys()), y=list(sorted_ret.values()),
                marker_color=bar_colors,
                text=[f"{v:.1f}%" for v in sorted_ret.values()],
                textposition="outside", textfont=dict(color="#f0f6fc"),
            ))
            fig_bar.update_layout(**PLOTLY_LAYOUT, height=320,
                                  yaxis=dict(ticksuffix="%", gridcolor="#21262d", zeroline=False),
                                  title=dict(text="Individual Stock Returns",
                                             font=dict(color="#f0f6fc", size=14)))
            st.plotly_chart(fig_bar, use_container_width=True)

        # Weight table
        weight_df = pd.DataFrame({
            "Ticker": list(weights.keys()),
            "Weight": [f"{v*100:.1f}%" for v in weights.values()],
            "Return": [f"{returns_by_stock.get(t, 0):.2f}%" for t in weights.keys()],
        })
        st.dataframe(weight_df, use_container_width=True, hide_index=True)

    # ── TAB: Risk ──
    with tab_risk:
        returns = metrics["returns"]

        c_left, c_right = st.columns(2)

        with c_left:
            # Daily return distribution
            port_ret = metrics["port_ret"]
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=port_ret * 100, nbinsx=40,
                name="Daily Returns",
                marker_color="#388bfd", opacity=0.75,
            ))
            fig_hist.add_vline(x=float(port_ret.mean()*100), line_dash="dot",
                               line_color="#3fb950", line_width=1.5,
                               annotation_text="Mean", annotation_font_color="#3fb950")
            fig_hist.update_layout(**PLOTLY_LAYOUT, height=300,
                                   xaxis=dict(ticksuffix="%", gridcolor="#21262d"),
                                   title=dict(text="Portfolio Daily Return Distribution",
                                              font=dict(color="#f0f6fc", size=14)))
            st.plotly_chart(fig_hist, use_container_width=True)

        with c_right:
            # Correlation heatmap
            if returns.shape[1] > 1:
                corr = returns.corr()
                fig_heat = go.Figure(go.Heatmap(
                    z=corr.values, x=corr.columns, y=corr.index,
                    colorscale=[[0,"#f85149"],[0.5,"#161b22"],[1,"#388bfd"]],
                    zmin=-1, zmax=1,
                    text=[[f"{v:.2f}" for v in row] for row in corr.values],
                    texttemplate="%{text}",
                    textfont=dict(size=11, color="#f0f6fc"),
                ))
                fig_heat.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    height=300, margin=dict(l=10, r=10, t=30, b=10),
                    font=dict(family="Inter", color="#8b949e"),
                    title=dict(text="Return Correlation Matrix",
                               font=dict(color="#f0f6fc", size=14)),
                )
                st.plotly_chart(fig_heat, use_container_width=True)

        # Drawdown
        cum_port   = metrics["cumulative"]
        roll_max   = cum_port.cummax()
        drawdown   = (cum_port - roll_max) / roll_max * 100

        fig_dd = go.Figure()
        fig_dd.add_trace(go.Scatter(
            x=drawdown.index, y=drawdown,
            fill="tozeroy", fillcolor="rgba(248,81,73,0.15)",
            line=dict(color="#f85149", width=1.5),
            name="Drawdown",
        ))
        fig_dd.update_layout(**PLOTLY_LAYOUT, height=220,
                             yaxis=dict(ticksuffix="%", gridcolor="#21262d", zeroline=False),
                             title=dict(text=f"Portfolio Drawdown  (Max: {drawdown.min():.1f}%)",
                                        font=dict(color="#f0f6fc", size=14)))
        st.plotly_chart(fig_dd, use_container_width=True)

    # ── TAB: Stock Breakdown ──
    with tab_stocks:
        for t in portfolio_tickers:
            df_t = fetch_stock_data(t, port_period_code)
            if df_t.empty:
                continue
            tr   = trend_analysis(df_t)
            mom  = momentum_analysis(df_t)
            vl   = volatility_analysis(df_t)
            r, rc, _ = recommendation(tr, mom, vl)
            badge_cls = {"BUY":"badge-buy","SELL":"badge-sell","HOLD":"badge-hold"}[r]
            ret_val = (df_t["Close"].squeeze().iloc[-1] / df_t["Close"].squeeze().iloc[0] - 1) * 100
            ret_color = "#3fb950" if ret_val >= 0 else "#f85149"
            st.markdown(f"""
            <div class='card' style='display:flex;align-items:center;justify-content:space-between;'>
                <div>
                    <strong style='color:#f0f6fc;font-size:1.05rem;'>{t}</strong>
                    <span style='color:#8b949e;font-size:0.8rem;margin-left:0.5rem;'>
                        {tr['trend']} &nbsp;·&nbsp; RSI {mom['rsi']:.0f} &nbsp;·&nbsp;
                        Vol {vl['vol']:.1f}%
                    </span>
                </div>
                <div style='display:flex;align-items:center;gap:1rem;'>
                    <span style='color:{ret_color};font-weight:600;'>
                        {'+' if ret_val>=0 else ''}{ret_val:.2f}%
                    </span>
                    <span class='badge {badge_cls}'>{r}</span>
                </div>
            </div>""", unsafe_allow_html=True)

        # Interpretation
        st.markdown("---")
        outperf  = metrics["outperf"]
        sharpe   = metrics["sharpe"]
        ann_vol  = metrics["ann_vol"]
        bench_v  = metrics["bench_total"]
        port_v   = metrics["total_ret"]

        perf_icon = "✅" if outperf > 0 else "❌"
        risk_icon = "✅" if ann_vol < 0.2 else "⚠️"
        sr_icon   = "✅" if sharpe >= 1 else ("⚠️" if sharpe >= 0.5 else "❌")

        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>📋 Portfolio Interpretation</div>
            <ul style='color:#c9d1d9;line-height:2;margin:0.5rem 0;'>
                <li>{perf_icon} Portfolio returned <strong style='color:#f0f6fc;'>{fmt_pct(port_v)}</strong>
                    vs SPY <strong style='color:#8b949e;'>{fmt_pct(bench_v)}</strong>
                    → <strong style='color:{"#3fb950" if outperf>0 else "#f85149"};'>
                    {"Outperformed" if outperf>0 else "Underperformed"} by {fmt_pct(abs(outperf))}
                    </strong></li>
                <li>{risk_icon} Annualized volatility of <strong style='color:#f0f6fc;'>{ann_vol*100:.1f}%</strong>
                    — {"lower" if ann_vol < 0.20 else "higher"} risk relative to typical equity portfolios</li>
                <li>{sr_icon} Sharpe ratio of <strong style='color:#f0f6fc;'>{sharpe:.2f}</strong>
                    — {"excellent risk-adjusted returns" if sharpe>=2 else
                       "good risk-adjusted returns" if sharpe>=1 else
                       "fair risk-adjusted returns" if sharpe>=0.5 else
                       "poor risk-adjusted returns — consider rebalancing"}</li>
            </ul>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE 3 — STOCK SCREENER
# ─────────────────────────────────────────────
elif page == "🔍 Stock Screener":

    if not run_screener:
        st.markdown("""
        <div style='text-align:center;padding:3rem 0 2rem 0;'>
            <div style='font-size:3rem;'>🔍</div>
            <h1 style='color:#f0f6fc;font-weight:700;font-size:2rem;'>Stock Screener</h1>
            <p style='color:#8b949e;font-size:1rem;max-width:480px;margin:auto;'>
                Compare multiple stocks side-by-side. Add tickers in the sidebar and click
                <strong style='color:#3fb950'>Screen Stocks</strong>.
            </p>
        </div>""", unsafe_allow_html=True)
        st.stop()

    st.markdown(f"""
    <h1 style='color:#f0f6fc;font-weight:700;font-size:1.8rem;margin:0 0 0.25rem 0;'>
        Stock Screener
    </h1>
    <p style='color:#8b949e;font-size:0.85rem;'>Screening {len(screener_tickers)} stocks · 6-month window</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    rows = []
    prog = st.progress(0, text="Fetching data…")
    for i, t in enumerate(screener_tickers):
        df_t = fetch_stock_data(t, "6mo")
        info_t = fetch_info(t)
        if df_t.empty:
            prog.progress((i+1)/len(screener_tickers))
            continue
        tr   = trend_analysis(df_t)
        mom  = momentum_analysis(df_t)
        vl   = volatility_analysis(df_t)
        rec_t, _, _ = recommendation(tr, mom, vl)
        close_t = df_t["Close"].squeeze()
        ret_1m = float((close_t.iloc[-1]/close_t.iloc[-21] - 1)*100) if len(close_t) >= 21 else None
        ret_6m = float((close_t.iloc[-1]/close_t.iloc[0]   - 1)*100)
        rows.append({
            "Ticker":       t,
            "Company":      info_t.get("shortName", t),
            "Price":        f"${tr['price']:,.2f}",
            "6M Return":    f"{ret_6m:+.1f}%",
            "1M Return":    f"{ret_1m:+.1f}%" if ret_1m else "—",
            "RSI":          f"{mom['rsi']:.1f}",
            "Volatility":   f"{vl['vol']:.1f}%",
            "Vol Level":    vl["label"],
            "Trend":        tr["trend"],
            "Signal":       mom["signal"],
            "Rec":          rec_t,
            "_ret6":        ret_6m,
        })
        prog.progress((i+1)/len(screener_tickers))

    prog.empty()

    if not rows:
        st.error("No data returned. Check your tickers.")
        st.stop()

    screen_df = pd.DataFrame(rows)

    # Performance comparison chart
    fig_screen = go.Figure()
    colors = ["#388bfd","#3fb950","#e3b341","#f85149","#6e40c9",
              "#da3633","#79c0ff","#7ee787","#d2a679","#ff7b72"]
    for idx, t in enumerate(screener_tickers):
        df_t = fetch_stock_data(t, "6mo")
        if df_t.empty:
            continue
        c = df_t["Close"].squeeze()
        normalized = (c / c.iloc[0] - 1) * 100
        fig_screen.add_trace(go.Scatter(
            x=normalized.index, y=normalized,
            name=t, line=dict(color=colors[idx % len(colors)], width=2),
        ))
    fig_screen.add_hline(y=0, line_color="#21262d", line_width=1)
    fig_screen.update_layout(**PLOTLY_LAYOUT, height=380,
                             yaxis=dict(ticksuffix="%", gridcolor="#21262d", zeroline=False),
                             title=dict(text="6-Month Normalized Performance Comparison",
                                        font=dict(color="#f0f6fc", size=14)))
    st.plotly_chart(fig_screen, use_container_width=True)

    # Summary table
    st.markdown('<p class="section-header">Screener Results</p>', unsafe_allow_html=True)

    display_df = screen_df.drop(columns=["_ret6"]).set_index("Ticker")
    st.dataframe(
        display_df,
        use_container_width=True,
        height=min(40 * len(display_df) + 50, 500),
    )

    # Signal breakdown
    st.markdown("---")
    col_b, col_s, col_h = st.columns(3)
    buys  = [r["Ticker"] for r in rows if r["Rec"] == "BUY"]
    sells = [r["Ticker"] for r in rows if r["Rec"] == "SELL"]
    holds = [r["Ticker"] for r in rows if r["Rec"] == "HOLD"]

    for col, label, badge, tickers in [
        (col_b, "BUY Signals",  "badge-buy",  buys),
        (col_h, "HOLD Signals", "badge-hold", holds),
        (col_s, "SELL Signals", "badge-sell", sells),
    ]:
        with col:
            items = " ".join(f"<span class='badge {badge}'>{t}</span>" for t in tickers) or "—"
            st.markdown(f"""
            <div class='card' style='text-align:center;'>
                <div class='card-title'>{label}</div>
                <div style='font-size:1.5rem;font-weight:700;color:#f0f6fc;margin:0.4rem 0;'>
                    {len(tickers)}
                </div>
                <div style='display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:0.5rem;'>
                    {items}
                </div>
            </div>""", unsafe_allow_html=True)
