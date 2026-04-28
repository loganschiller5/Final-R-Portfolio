# ================================================================
# EQUITYLENS — Stock Analytics & Portfolio Dashboard
# FIN 330 Final Project
# ================================================================

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ────────────────────────────────────────────
st.set_page_config(
    page_title="EquityLens",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ────────────────────────────────────────────
# THEME / CSS
# ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0a0e1a !important;
    color: #e2e8f0 !important;
}
.main { background-color: #0a0e1a !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f1629 0%, #0a0e1a 100%) !important;
    border-right: 1px solid #1e2a45 !important;
}
section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] strong { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] label {
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
    font-weight: 600 !important;
    color: #64748b !important;
}

/* ── metric cards ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #111827 0%, #0f172a 100%) !important;
    border: 1px solid #1e2a45 !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.3rem !important;
    transition: all 0.25s ease !important;
}
[data-testid="metric-container"]:hover {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 20px rgba(59,130,246,0.12) !important;
    transform: translateY(-1px) !important;
}
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-weight: 700 !important; font-size: 1.45rem !important; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; font-weight: 600 !important; }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111827 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid #1e2a45 !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    border-radius: 9px !important;
    padding: 8px 22px !important;
    font-weight: 600 !important;
    font-size: 0.83rem !important;
    border: none !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: #fff !important;
    box-shadow: 0 2px 10px rgba(37,99,235,0.35) !important;
}

/* ── buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 0rem !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    width: 100% !important;
    letter-spacing: 0.03em !important;
    transition: all 0.22s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.4) !important;
}

/* ── inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background: #111827 !important;
    border: 1px solid #1e2a45 !important;
    border-radius: 9px !important;
    color: #f1f5f9 !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.18) !important;
}

/* ── slider ── */
.stSlider [data-testid="stThumb"] { background: #3b82f6 !important; }
.stSlider [data-baseweb="slider"] > div:first-child { background: #1e2a45 !important; }

/* ── radio ── */
.stRadio > div { gap: 0.5rem !important; }
.stRadio label {
    background: #111827 !important;
    border: 1px solid #1e2a45 !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    color: #94a3b8 !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
}
.stRadio label:has(input:checked) {
    background: #1e3a8a !important;
    border-color: #3b82f6 !important;
    color: #93c5fd !important;
}

/* ── dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #1e2a45 !important;
}

/* ── divider ── */
hr { border-color: #1e2a45 !important; margin: 1rem 0 !important; }

/* ── progress ── */
.stProgress > div > div > div { background: #3b82f6 !important; }

/* ── custom HTML elements ── */
.el-card {
    background: linear-gradient(135deg, #111827 0%, #0f172a 100%);
    border: 1px solid #1e2a45;
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 0.9rem;
    transition: border-color 0.2s;
}
.el-card:hover { border-color: #2563eb; }
.el-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #475569;
    font-weight: 700;
    margin-bottom: 0.35rem;
}
.el-value { font-size: 1.55rem; font-weight: 800; color: #f1f5f9; line-height: 1.1; }
.el-sub { font-size: 0.8rem; color: #64748b; margin-top: 0.4rem; line-height: 1.6; }

.badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 14px;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    gap: 5px;
}
.badge-buy  { background: rgba(16,185,129,0.12); color: #10b981; border: 1px solid rgba(16,185,129,0.35); }
.badge-sell { background: rgba(239,68,68,0.12);  color: #ef4444; border: 1px solid rgba(239,68,68,0.35); }
.badge-hold { background: rgba(245,158,11,0.12); color: #f59e0b; border: 1px solid rgba(245,158,11,0.35); }

.rec-panel {
    background: linear-gradient(135deg, #0f172a, #111827);
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-top: 1rem;
    position: relative;
    overflow: hidden;
}
.rec-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.rec-panel-buy::before   { background: linear-gradient(90deg, #10b981, #34d399); }
.rec-panel-sell::before  { background: linear-gradient(90deg, #ef4444, #f87171); }
.rec-panel-hold::before  { background: linear-gradient(90deg, #f59e0b, #fbbf24); }

.logo-text {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #f1f5f9;
}
.logo-text .accent { color: #3b82f6; }

.section-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2a45;
}

.hero-container {
    text-align: center;
    padding: 5rem 2rem 3rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #f1f5f9, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 1rem 0 0.5rem;
}
.hero-sub {
    color: #475569;
    font-size: 1.05rem;
    max-width: 480px;
    margin: 0 auto 2rem;
    line-height: 1.7;
}
.hero-icon { font-size: 3.5rem; line-height: 1; }

.ticker-chip {
    display: inline-block;
    background: #111827;
    border: 1px solid #1e2a45;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 0.85rem;
    font-weight: 700;
    color: #60a5fa;
    margin: 3px;
}

.interp-box {
    background: linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid #1e2a45;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
}
.interp-row {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #0f172a;
    font-size: 0.875rem;
    color: #94a3b8;
    line-height: 1.6;
}
.interp-row:last-child { border-bottom: none; }
.interp-icon { font-size: 1rem; flex-shrink: 0; margin-top: 1px; }
</style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────
# PLOTLY BASE LAYOUT  (no xaxis/yaxis keys)
# ────────────────────────────────────────────
BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#64748b", size=11),
    legend=dict(
        bgcolor="rgba(17,24,39,0.8)",
        bordercolor="#1e2a45",
        borderwidth=1,
        font=dict(size=11),
    ),
    margin=dict(l=8, r=8, t=36, b=8),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="#111827",
        bordercolor="#1e2a45",
        font=dict(family="Inter", size=11, color="#e2e8f0"),
    ),
)

GRID = dict(gridcolor="#1e2a45", zeroline=False, showline=False, tickfont=dict(size=10))


def apply_layout(fig, extra: dict = None):
    """Apply BASE_LAYOUT + any extra keys safely."""
    cfg = dict(**BASE_LAYOUT)
    if extra:
        cfg.update(extra)
    fig.update_layout(**cfg)
    return fig


# ────────────────────────────────────────────
# DATA HELPERS
# ────────────────────────────────────────────

@st.cache_data(ttl=300, show_spinner=False)
def load_prices(ticker: str, period: str) -> pd.DataFrame:
    try:
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]
        df.index = pd.to_datetime(df.index)
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=600, show_spinner=False)
def load_info(ticker: str) -> dict:
    try:
        return yf.Ticker(ticker).info or {}
    except Exception:
        return {}


# ────────────────────────────────────────────
# INDICATOR CALCULATIONS
# ────────────────────────────────────────────

def calc_rsi(s: pd.Series, n: int = 14) -> pd.Series:
    d = s.diff()
    up   = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    down = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs   = up / down.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).rename("RSI")


def calc_macd(s: pd.Series):
    ema12  = s.ewm(span=12, adjust=False).mean()
    ema26  = s.ewm(span=26, adjust=False).mean()
    macd   = (ema12 - ema26).rename("MACD")
    sig    = macd.ewm(span=9, adjust=False).mean().rename("Signal")
    hist   = (macd - sig).rename("Hist")
    return macd, sig, hist


def calc_bb(s: pd.Series, n: int = 20):
    mid   = s.rolling(n).mean()
    std   = s.rolling(n).std()
    return (mid + 2*std).rename("Upper"), mid.rename("Mid"), (mid - 2*std).rename("Lower")


def calc_vol(s: pd.Series, n: int = 20) -> float:
    return float(s.pct_change().dropna().rolling(n).std().iloc[-1] * np.sqrt(252) * 100)


# ────────────────────────────────────────────
# ANALYSIS LOGIC
# ────────────────────────────────────────────

def trend_signal(df: pd.DataFrame) -> dict:
    c     = df["Close"].squeeze()
    price = float(c.iloc[-1])
    ma20  = float(c.rolling(20).mean().iloc[-1])
    ma50  = float(c.rolling(50).mean().iloc[-1])
    if price > ma20 > ma50:
        label, color = "Strong Uptrend",   "#10b981"
    elif price < ma20 < ma50:
        label, color = "Strong Downtrend", "#ef4444"
    else:
        label, color = "Mixed / Sideways", "#f59e0b"
    return dict(price=price, ma20=ma20, ma50=ma50, label=label, color=color)


def momentum_signal(df: pd.DataFrame) -> dict:
    rsi_s = calc_rsi(df["Close"].squeeze())
    rsi   = float(rsi_s.iloc[-1])
    if rsi > 70:
        label, color = "Overbought", "#ef4444"
    elif rsi < 30:
        label, color = "Oversold",   "#10b981"
    else:
        label, color = "Neutral",    "#64748b"
    return dict(rsi=rsi, label=label, color=color, series=rsi_s)


def vol_signal(df: pd.DataFrame) -> dict:
    v = calc_vol(df["Close"].squeeze())
    if v > 40:
        label, color = "High",   "#ef4444"
    elif v > 25:
        label, color = "Medium", "#f59e0b"
    else:
        label, color = "Low",    "#10b981"
    return dict(vol=v, label=label, color=color)


def get_rec(t: dict, m: dict, v: dict):
    if "Uptrend" in t["label"] and m["rsi"] < 70 and v["vol"] < 55:
        return "BUY",  "#10b981", "badge-buy",  "rec-panel-buy",  \
               f"Price is above both moving averages with RSI at {m['rsi']:.1f} — momentum is intact and volatility ({v['vol']:.1f}%) is manageable."
    elif "Downtrend" in t["label"] or m["rsi"] > 75:
        return "SELL", "#ef4444", "badge-sell", "rec-panel-sell", \
               f"Bearish trend structure or elevated RSI ({m['rsi']:.1f}) suggests distribution. Consider trimming or exiting."
    else:
        return "HOLD", "#f59e0b", "badge-hold", "rec-panel-hold", \
               f"Signals are mixed. RSI at {m['rsi']:.1f} and trend is unclear. Wait for confirmation before acting."


def portfolio_calc(tickers, weights, period):
    frames = {}
    for t in tickers:
        df = load_prices(t, period)
        if not df.empty:
            frames[t] = df["Close"].squeeze()
    if not frames:
        return None
    prices   = pd.DataFrame(frames).dropna()
    rets     = prices.pct_change().dropna()
    w        = np.array([weights.get(t, 0) for t in prices.columns])
    w        = w / w.sum()   # normalise
    port_r   = rets.dot(w)
    bench_df = load_prices("SPY", period)
    bench_r  = bench_df["Close"].squeeze().pct_change().dropna() if not bench_df.empty else None
    total    = float((1 + port_r).prod() - 1)
    ann_vol  = float(port_r.std() * np.sqrt(252))
    sharpe   = float((port_r.mean() * 252) / ann_vol) if ann_vol > 0 else 0
    bench_t  = float((1 + bench_r).prod() - 1) if bench_r is not None else 0
    cum      = (1 + port_r).cumprod()
    bench_c  = (1 + bench_r).cumprod() if bench_r is not None else None
    dd       = (cum - cum.cummax()) / cum.cummax() * 100
    return dict(
        total=total, ann_vol=ann_vol, sharpe=sharpe,
        bench=bench_t, outperf=total - bench_t,
        cum=cum, bench_cum=bench_c,
        rets=rets, port_r=port_r, prices=prices, dd=dd,
    )


# ────────────────────────────────────────────
# FORMAT HELPERS
# ────────────────────────────────────────────

def pct(v, sign=True):
    s = "+" if sign and v >= 0 else ""
    return f"{s}{v*100:.2f}%"

def bignum(v, pre=""):
    if not v: return "—"
    if v >= 1e12: return f"{pre}{v/1e12:.2f}T"
    if v >= 1e9:  return f"{pre}{v/1e9:.2f}B"
    if v >= 1e6:  return f"{pre}{v/1e6:.2f}M"
    return f"{pre}{v:,.0f}"


COLORS = ["#3b82f6","#10b981","#f59e0b","#ef4444","#8b5cf6",
          "#06b6d4","#f97316","#84cc16","#ec4899","#14b8a6"]


# ────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        '<div class="logo-text">Equity<span class="accent">Lens</span> 📈</div>',
        unsafe_allow_html=True,
    )
    st.caption("Professional Stock & Portfolio Analytics")
    st.divider()

    page = st.radio(
        "nav",
        ["📊  Stock Analysis", "💼  Portfolio", "🔍  Screener"],
        label_visibility="collapsed",
    )
    st.divider()

    # ── per-page controls ──
    if page == "📊  Stock Analysis":
        st.markdown("**Stock Analysis**")
        ticker = st.text_input("Ticker", "AAPL", placeholder="AAPL, TSLA…").upper().strip()
        PERIODS = {"1 Month": "1mo", "3 Months": "3mo", "6 Months": "6mo",
                   "1 Year": "1y", "2 Years": "2y"}
        period_lbl = st.selectbox("Period", list(PERIODS.keys()), index=2)
        period     = PERIODS[period_lbl]
        go_btn     = st.button("🔍  Analyze")

    elif page == "💼  Portfolio":
        st.markdown("**Portfolio**")
        raw_tickers = st.text_area(
            "Tickers (comma-separated)",
            "AAPL, MSFT, GOOGL, NVDA, JPM",
            height=72,
        )
        ptickers = [t.strip().upper() for t in raw_tickers.split(",") if t.strip()]
        st.markdown("**Weights**")
        weights_raw = {}
        leftover    = 1.0
        for i, t in enumerate(ptickers):
            if i < len(ptickers) - 1:
                default = round(1 / len(ptickers), 2)
                w = st.slider(t, 0.0, 1.0, default, 0.01, key=f"pw_{t}")
                weights_raw[t] = w
                leftover -= w
            else:
                weights_raw[t] = max(round(leftover, 2), 0.0)
                st.metric(t, f"{weights_raw[t]*100:.0f}%", "auto")
        PPER = {"6 Months": "6mo", "1 Year": "1y", "2 Years": "2y"}
        pper_lbl = st.selectbox("Period", list(PPER.keys()), index=1)
        pper     = PPER[pper_lbl]
        go_port  = st.button("📊  Run Analysis")

    else:
        st.markdown("**Screener**")
        scr_raw  = st.text_area(
            "Tickers",
            "AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META, JPM, V, JNJ",
            height=110,
        )
        stickers = [t.strip().upper() for t in scr_raw.split(",") if t.strip()]
        go_scr   = st.button("🔍  Screen")

    st.divider()
    st.caption("Data: Yahoo Finance · cache 5 min")


# ════════════════════════════════════════════
# PAGE 1 — STOCK ANALYSIS
# ════════════════════════════════════════════
if page == "📊  Stock Analysis":

    if not go_btn:
        st.markdown("""
        <div class="hero-container">
            <div class="hero-icon">📈</div>
            <div class="hero-title">EquityLens</div>
            <p class="hero-sub">
                Enter any ticker in the sidebar and click <strong>Analyze</strong>
                for a full technical breakdown — trend, momentum, volatility, and a
                data-driven recommendation.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<p style='text-align:center;color:#334155;font-size:0.75rem;"
            "text-transform:uppercase;letter-spacing:.1em;'>Popular</p>",
            unsafe_allow_html=True,
        )
        chips = "".join(
            f"<span class='ticker-chip'>{t}</span>"
            for t in ["AAPL","MSFT","GOOGL","NVDA","TSLA","AMZN","META","JPM"]
        )
        st.markdown(f"<div style='text-align:center'>{chips}</div>", unsafe_allow_html=True)
        st.stop()

    # ── fetch ──
    with st.spinner(f"Loading {ticker}…"):
        df   = load_prices(ticker, period)
        info = load_info(ticker)

    if df.empty:
        st.error(f"No data found for **{ticker}**. Check the symbol and try again.")
        st.stop()

    close = df["Close"].squeeze()

    # ── compute ──
    tr   = trend_signal(df)
    mom  = momentum_signal(df)
    vlt  = vol_signal(df)
    rec, rec_col, rec_badge, rec_panel, rec_reason = get_rec(tr, mom, vlt)

    macd, macd_sig, macd_hist = calc_macd(close)
    bb_up, bb_mid, bb_lo      = calc_bb(close)

    price_now = tr["price"]
    price_beg = float(close.iloc[0])
    period_chg = (price_now - price_beg) / price_beg

    # ── header ──
    name     = info.get("longName", ticker)
    sector   = info.get("sector", "—")
    mktcap   = info.get("marketCap", 0)
    exchange = info.get("exchange", "")

    hcol1, hcol2 = st.columns([4, 1])
    with hcol1:
        st.markdown(
            f"<h1 style='color:#f1f5f9;font-weight:800;font-size:2rem;"
            f"letter-spacing:-0.03em;margin:0'>{name}</h1>"
            f"<p style='color:#475569;font-size:0.85rem;margin:3px 0 0'>"
            f"<span style='color:#60a5fa;font-weight:700'>{ticker}</span>"
            f" &nbsp;·&nbsp; {sector} &nbsp;·&nbsp; {exchange}</p>",
            unsafe_allow_html=True,
        )
    with hcol2:
        arrow = "▲" if period_chg >= 0 else "▼"
        col = "#10b981" if period_chg >= 0 else "#ef4444"
        st.markdown(
            f"<div style='text-align:right;padding-top:.4rem'>"
            f"<span style='color:{col};font-size:1.05rem;font-weight:800'>"
            f"{arrow} {abs(period_chg)*100:.2f}%</span>"
            f"<div style='color:#334155;font-size:0.72rem'>{period_lbl} change</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── KPI row ──
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Price",       f"${price_now:,.2f}", pct(period_chg))
    k2.metric("Market Cap",  bignum(mktcap, "$"))
    k3.metric("20-Day MA",   f"${tr['ma20']:,.2f}")
    k4.metric("50-Day MA",   f"${tr['ma50']:,.2f}")
    k5.metric("RSI (14)",    f"{mom['rsi']:.1f}",  mom["label"])

    st.markdown("")

    # ── tabs ──
    t1, t2, t3 = st.tabs(["📈  Price & Volume", "🔬  Indicators", "📋  Summary & Signals"])

    # ── TAB 1 ──
    with t1:
        ctype = st.radio("Chart", ["Candlestick", "Line", "Area"],
                         horizontal=True, label_visibility="collapsed")

        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            row_heights=[0.73, 0.27],
            vertical_spacing=0.02,
        )

        if ctype == "Candlestick":
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"].squeeze(), high=df["High"].squeeze(),
                low=df["Low"].squeeze(),   close=close,
                increasing_line_color="#10b981", increasing_fillcolor="#10b981",
                decreasing_line_color="#ef4444", decreasing_fillcolor="#ef4444",
                name=ticker, showlegend=False,
            ), row=1, col=1)
        elif ctype == "Line":
            fig.add_trace(go.Scatter(
                x=df.index, y=close, name=ticker,
                line=dict(color="#3b82f6", width=2.2), showlegend=False,
            ), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(
                x=df.index, y=close, name=ticker,
                fill="tozeroy", fillcolor="rgba(59,130,246,0.08)",
                line=dict(color="#3b82f6", width=2.2), showlegend=False,
            ), row=1, col=1)

        # MAs
        fig.add_trace(go.Scatter(x=df.index, y=close.rolling(20).mean(),
            name="MA 20", line=dict(color="#f59e0b", width=1.5, dash="dot")), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=close.rolling(50).mean(),
            name="MA 50", line=dict(color="#ef4444", width=1.5, dash="dot")), row=1, col=1)

        # Bollinger Bands
        fig.add_trace(go.Scatter(x=df.index, y=bb_up,
            name="BB Upper", line=dict(color="#8b5cf6", width=1, dash="dash")), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=bb_lo,
            name="BB Lower", line=dict(color="#8b5cf6", width=1, dash="dash"),
            fill="tonexty", fillcolor="rgba(139,92,246,0.05)"), row=1, col=1)

        # Volume
        vc = ["#10b981" if float(c) >= float(o) else "#ef4444"
              for c, o in zip(df["Close"].squeeze(), df["Open"].squeeze())]
        fig.add_trace(go.Bar(x=df.index, y=df["Volume"].squeeze(),
            marker_color=vc, opacity=0.55, name="Volume", showlegend=False), row=2, col=1)

        apply_layout(fig, dict(height=540))
        fig.update_xaxes(**GRID, rangeslider_visible=False)
        fig.update_yaxes(**GRID)
        fig.update_yaxes(title_text="Volume", row=2, col=1,
                         title_font=dict(size=9, color="#475569"))
        st.plotly_chart(fig, use_container_width=True)

    # ── TAB 2 ──
    with t2:
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<p class="section-title">RSI (14-Day)</p>', unsafe_allow_html=True)
            rsi_s = mom["series"]
            fig_r = go.Figure()
            fig_r.add_hrect(y0=70, y1=100, fillcolor="rgba(239,68,68,0.06)",  line_width=0)
            fig_r.add_hrect(y0=0,  y1=30,  fillcolor="rgba(16,185,129,0.06)", line_width=0)
            fig_r.add_hline(y=70, line_dash="dot", line_color="#ef4444",  line_width=1,
                            annotation_text="Overbought 70",
                            annotation_font=dict(color="#ef4444", size=10),
                            annotation_position="top right")
            fig_r.add_hline(y=30, line_dash="dot", line_color="#10b981",  line_width=1,
                            annotation_text="Oversold 30",
                            annotation_font=dict(color="#10b981", size=10),
                            annotation_position="bottom right")
            fig_r.add_trace(go.Scatter(
                x=rsi_s.index, y=rsi_s, name="RSI",
                line=dict(color="#60a5fa", width=2.2),
                fill="tozeroy", fillcolor="rgba(96,165,250,0.06)",
            ))
            apply_layout(fig_r, dict(height=290))
            fig_r.update_xaxes(**GRID)
            fig_r.update_yaxes(range=[0, 100], **GRID)
            st.plotly_chart(fig_r, use_container_width=True)

        with col_b:
            st.markdown('<p class="section-title">MACD (12 / 26 / 9)</p>', unsafe_allow_html=True)
            hcolors = ["#10b981" if v >= 0 else "#ef4444" for v in macd_hist.fillna(0)]
            fig_m = go.Figure()
            fig_m.add_trace(go.Bar(x=df.index, y=macd_hist,
                marker_color=hcolors, opacity=0.7, name="Histogram"))
            fig_m.add_trace(go.Scatter(x=df.index, y=macd,
                line=dict(color="#3b82f6", width=2), name="MACD"))
            fig_m.add_trace(go.Scatter(x=df.index, y=macd_sig,
                line=dict(color="#f59e0b", width=1.5, dash="dot"), name="Signal"))
            apply_layout(fig_m, dict(height=290))
            fig_m.update_xaxes(**GRID)
            fig_m.update_yaxes(**GRID)
            st.plotly_chart(fig_m, use_container_width=True)

        st.markdown('<p class="section-title">Bollinger Bands + Price</p>',
                    unsafe_allow_html=True)
        fig_bb = go.Figure()
        fig_bb.add_trace(go.Scatter(x=df.index, y=bb_up, name="Upper",
            line=dict(color="#8b5cf6", width=1.2, dash="dash")))
        fig_bb.add_trace(go.Scatter(x=df.index, y=bb_mid, name="Mid",
            line=dict(color="#475569", width=1, dash="dot")))
        fig_bb.add_trace(go.Scatter(x=df.index, y=bb_lo, name="Lower",
            line=dict(color="#8b5cf6", width=1.2, dash="dash"),
            fill="tonexty", fillcolor="rgba(139,92,246,0.06)"))
        fig_bb.add_trace(go.Scatter(x=df.index, y=close, name="Price",
            line=dict(color="#3b82f6", width=2)))
        apply_layout(fig_bb, dict(height=260))
        fig_bb.update_xaxes(**GRID)
        fig_bb.update_yaxes(**GRID)
        st.plotly_chart(fig_bb, use_container_width=True)

        st.markdown('<p class="section-title">Annualized Volatility Gauge (20-Day)</p>',
                    unsafe_allow_html=True)
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=vlt["vol"],
            number=dict(suffix="%", font=dict(color="#f1f5f9", size=38, family="Inter")),
            gauge=dict(
                axis=dict(range=[0, 80], tickcolor="#1e2a45",
                          tickfont=dict(color="#475569", size=10)),
                bar=dict(color=vlt["color"], thickness=0.28),
                bgcolor="#111827",
                borderwidth=0,
                steps=[
                    dict(range=[0,  25], color="#0f2d1c"),
                    dict(range=[25, 40], color="#2d1f0a"),
                    dict(range=[40, 80], color="#2d0a0a"),
                ],
            ),
            title=dict(
                text=f"Volatility Level: <b style='color:{vlt['color']}'>{vlt['label']}</b>",
                font=dict(size=13, color="#64748b", family="Inter"),
            ),
        ))
        fig_g.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=240,
            font=dict(family="Inter", color="#64748b"),
            margin=dict(l=20, r=20, t=20, b=10),
        )
        st.plotly_chart(fig_g, use_container_width=True)

    # ── TAB 3 ──
    with t3:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="el-card">
                <div class="el-label">📊 Trend</div>
                <div class="el-value" style="color:{tr['color']};font-size:1.15rem">{tr['label']}</div>
                <div class="el-sub">
                    Price &nbsp;<strong style="color:#f1f5f9">${tr['price']:,.2f}</strong><br>
                    MA 20 &nbsp;<strong style="color:#f59e0b">${tr['ma20']:,.2f}</strong><br>
                    MA 50 &nbsp;<strong style="color:#ef4444">${tr['ma50']:,.2f}</strong>
                </div>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="el-card">
                <div class="el-label">⚡ Momentum</div>
                <div class="el-value" style="color:{mom['color']};font-size:1.15rem">{mom['label']}</div>
                <div class="el-sub">
                    RSI&nbsp;&nbsp;<strong style="color:#f1f5f9">{mom['rsi']:.2f}</strong><br>
                    <span style="color:#10b981">＜ 30 = Oversold</span><br>
                    <span style="color:#ef4444">＞ 70 = Overbought</span>
                </div>
            </div>""", unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="el-card">
                <div class="el-label">🌊 Volatility</div>
                <div class="el-value" style="color:{vlt['color']};font-size:1.15rem">{vlt['label']}</div>
                <div class="el-sub">
                    Ann. Vol&nbsp;<strong style="color:#f1f5f9">{vlt['vol']:.1f}%</strong><br>
                    <span style="color:#10b981">＜ 25% Low</span><br>
                    <span style="color:#f59e0b">25–40% Medium</span><br>
                    <span style="color:#ef4444">＞ 40% High</span>
                </div>
            </div>""", unsafe_allow_html=True)

        # Recommendation panel
        st.markdown(f"""
        <div class="rec-panel {rec_panel}">
            <div style="display:flex;align-items:center;gap:1rem;margin-bottom:.9rem">
                <span class="badge {rec_badge}" style="font-size:1rem;padding:7px 22px">
                    ⬟ {rec}
                </span>
                <div>
                    <div style="color:#f1f5f9;font-weight:700;font-size:1rem">
                        Trading Recommendation
                    </div>
                    <div style="color:#94a3b8;font-size:0.85rem;margin-top:2px">
                        {rec_reason}
                    </div>
                </div>
            </div>
            <p style="color:#334155;font-size:0.72rem;margin:0;
                      border-top:1px solid #1e2a45;padding-top:.7rem">
                ⚠ Based on technical indicators only. Not financial advice.
                Always conduct your own due diligence before investing.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Fundamentals
        pe  = info.get("trailingPE")
        eps = info.get("trailingEps")
        h52 = info.get("fiftyTwoWeekHigh")
        l52 = info.get("fiftyTwoWeekLow")
        dy  = info.get("dividendYield")
        beta = info.get("beta")

        if any([pe, eps, h52, l52]):
            st.markdown("---")
            st.markdown('<p class="section-title">Fundamentals</p>', unsafe_allow_html=True)
            f1, f2, f3, f4, f5, f6 = st.columns(6)
            f1.metric("P/E",        f"{pe:.1f}x"    if pe   else "—")
            f2.metric("EPS (TTM)",  f"${eps:.2f}"   if eps  else "—")
            f3.metric("52W High",   f"${h52:,.2f}"  if h52  else "—")
            f4.metric("52W Low",    f"${l52:,.2f}"  if l52  else "—")
            f5.metric("Div. Yield", f"{dy*100:.2f}%" if dy  else "—")
            f6.metric("Beta",       f"{beta:.2f}"   if beta else "—")


# ════════════════════════════════════════════
# PAGE 2 — PORTFOLIO
# ════════════════════════════════════════════
elif page == "💼  Portfolio":

    if not go_port:
        st.markdown("""
        <div class="hero-container">
            <div class="hero-icon">💼</div>
            <div class="hero-title">Portfolio Dashboard</div>
            <p class="hero-sub">
                Set your tickers and weights in the sidebar, choose a period,
                then click <strong>Run Analysis</strong>.
            </p>
        </div>""", unsafe_allow_html=True)
        st.stop()

    with st.spinner("Running portfolio analysis…"):
        m = portfolio_calc(ptickers, weights_raw, pper)

    if m is None:
        st.error("Could not fetch data. Check your tickers.")
        st.stop()

    # header
    st.markdown(
        f"<h1 style='color:#f1f5f9;font-weight:800;font-size:1.9rem;"
        f"letter-spacing:-0.03em;margin:0'>Portfolio Dashboard</h1>"
        f"<p style='color:#475569;font-size:0.85rem;margin:4px 0 0'>"
        f"{' · '.join(ptickers)} &nbsp;·&nbsp; {pper_lbl} &nbsp;·&nbsp; Benchmark: SPY</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("Total Return",    pct(m["total"]),
              f"SPY {pct(m['bench'])}")
    k2.metric("vs Benchmark",    pct(m["outperf"]),
              "Outperform" if m["outperf"]>0 else "Underperform")
    k3.metric("Ann. Volatility", f"{m['ann_vol']*100:.1f}%")
    k4.metric("Sharpe Ratio",    f"{m['sharpe']:.2f}",
              "≥1 Good · ≥2 Excellent")
    k5.metric("Max Drawdown",    f"{m['dd'].min():.1f}%")

    st.markdown("")
    pt1, pt2, pt3, pt4 = st.tabs(
        ["📈  Performance", "🥧  Allocation", "⚡  Risk", "🔬  Holdings"]
    )

    # ── Performance ──
    with pt1:
        cum, bc = m["cum"], m["bench_cum"]
        fig_p = go.Figure()
        fig_p.add_trace(go.Scatter(
            x=cum.index, y=(cum-1)*100, name="Portfolio",
            fill="tozeroy", fillcolor="rgba(59,130,246,0.07)",
            line=dict(color="#3b82f6", width=2.5),
        ))
        if bc is not None:
            fig_p.add_trace(go.Scatter(
                x=bc.index, y=(bc-1)*100, name="SPY",
                line=dict(color="#64748b", width=1.5, dash="dot"),
            ))
        fig_p.add_hline(y=0, line_color="#1e2a45", line_width=1)
        apply_layout(fig_p, dict(
            height=400,
            title=dict(text="Cumulative Return vs SPY",
                       font=dict(color="#94a3b8", size=14)),
        ))
        fig_p.update_xaxes(**GRID)
        fig_p.update_yaxes(**GRID, ticksuffix="%")
        st.plotly_chart(fig_p, use_container_width=True)

        # Rolling Sharpe
        pr   = m["port_r"]
        rsh  = (pr.rolling(21).mean() / pr.rolling(21).std()) * np.sqrt(252)
        fig_rs = go.Figure()
        fig_rs.add_trace(go.Scatter(x=rsh.index, y=rsh, name="Rolling Sharpe (21d)",
            line=dict(color="#8b5cf6", width=2), fill="tozeroy",
            fillcolor="rgba(139,92,246,0.06)"))
        fig_rs.add_hline(y=1,  line_dash="dot", line_color="#10b981", line_width=1)
        fig_rs.add_hline(y=0,  line_color="#1e2a45",                   line_width=1)
        apply_layout(fig_rs, dict(
            height=230,
            title=dict(text="Rolling 21-Day Sharpe Ratio",
                       font=dict(color="#94a3b8", size=14)),
        ))
        fig_rs.update_xaxes(**GRID)
        fig_rs.update_yaxes(**GRID)
        st.plotly_chart(fig_rs, use_container_width=True)

    # ── Allocation ──
    with pt2:
        ac1, ac2 = st.columns(2)

        with ac1:
            labels  = list(weights_raw.keys())
            vals    = [weights_raw[t]*100 for t in labels]
            pie_col = COLORS[:len(labels)]
            fig_pie = go.Figure(go.Pie(
                labels=labels, values=vals, hole=0.58,
                marker=dict(colors=pie_col, line=dict(color="#0a0e1a", width=2.5)),
                textinfo="label+percent",
                textfont=dict(color="#f1f5f9", size=11),
                hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
            ))
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                height=320, margin=dict(l=8, r=8, t=36, b=8),
                title=dict(text="Allocation", font=dict(color="#94a3b8", size=14)),
                annotations=[dict(text="Weights", x=0.5, y=0.5,
                                  font=dict(size=12, color="#475569"), showarrow=False)],
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with ac2:
            ind_rets = {}
            for t in ptickers:
                df_t = load_prices(t, pper)
                if not df_t.empty:
                    c = df_t["Close"].squeeze()
                    ind_rets[t] = float((c.iloc[-1]/c.iloc[0]-1)*100)
            sorted_r = dict(sorted(ind_rets.items(), key=lambda x: x[1], reverse=True))
            bc_list  = [COLORS[0] if v>=0 else "#ef4444" for v in sorted_r.values()]
            fig_bar  = go.Figure(go.Bar(
                x=list(sorted_r.keys()), y=list(sorted_r.values()),
                marker_color=bc_list,
                text=[f"{v:.1f}%" for v in sorted_r.values()],
                textposition="outside", textfont=dict(color="#94a3b8", size=11),
                hovertemplate="<b>%{x}</b><br>%{y:.2f}%<extra></extra>",
            ))
            apply_layout(fig_bar, dict(
                height=320,
                title=dict(text="Individual Returns", font=dict(color="#94a3b8", size=14)),
            ))
            fig_bar.update_xaxes(**GRID)
            fig_bar.update_yaxes(**GRID, ticksuffix="%")
            st.plotly_chart(fig_bar, use_container_width=True)

        # weight table
        tbl = pd.DataFrame({
            "Ticker":  list(weights_raw.keys()),
            "Weight":  [f"{v*100:.1f}%" for v in weights_raw.values()],
            "Return":  [f"{ind_rets.get(t,0):.2f}%" for t in weights_raw],
        })
        st.dataframe(tbl, use_container_width=True, hide_index=True)

    # ── Risk ──
    with pt3:
        rc1, rc2 = st.columns(2)

        with rc1:
            pr = m["port_r"]
            fig_h = go.Figure()
            fig_h.add_trace(go.Histogram(
                x=pr*100, nbinsx=40, name="Daily Returns",
                marker_color="#3b82f6", opacity=0.75,
                hovertemplate="%{x:.2f}%<extra></extra>",
            ))
            fig_h.add_vline(x=float(pr.mean()*100), line_dash="dot",
                            line_color="#10b981", line_width=1.5,
                            annotation_text="Mean",
                            annotation_font=dict(color="#10b981", size=10))
            apply_layout(fig_h, dict(
                height=300,
                title=dict(text="Daily Return Distribution",
                           font=dict(color="#94a3b8", size=14)),
            ))
            fig_h.update_xaxes(**GRID, ticksuffix="%")
            fig_h.update_yaxes(**GRID)
            st.plotly_chart(fig_h, use_container_width=True)

        with rc2:
            rets = m["rets"]
            if rets.shape[1] > 1:
                corr = rets.corr().round(2)
                z    = corr.values
                fig_hm = go.Figure(go.Heatmap(
                    z=z, x=corr.columns.tolist(), y=corr.index.tolist(),
                    colorscale=[[0,"#ef4444"],[0.5,"#111827"],[1,"#3b82f6"]],
                    zmin=-1, zmax=1,
                    text=[[f"{v:.2f}" for v in row] for row in z],
                    texttemplate="%{text}",
                    textfont=dict(size=11, color="#f1f5f9"),
                    hovertemplate="%{x} / %{y}: %{z:.2f}<extra></extra>",
                ))
                fig_hm.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    height=300, margin=dict(l=8, r=8, t=36, b=8),
                    font=dict(family="Inter", color="#64748b"),
                    title=dict(text="Correlation Matrix",
                               font=dict(color="#94a3b8", size=14)),
                )
                fig_hm.update_xaxes(showgrid=False)
                fig_hm.update_yaxes(showgrid=False)
                st.plotly_chart(fig_hm, use_container_width=True)

        # drawdown
        dd  = m["dd"]
        fig_dd = go.Figure()
        fig_dd.add_trace(go.Scatter(
            x=dd.index, y=dd, name="Drawdown",
            fill="tozeroy", fillcolor="rgba(239,68,68,0.10)",
            line=dict(color="#ef4444", width=1.5),
        ))
        apply_layout(fig_dd, dict(
            height=230,
            title=dict(text=f"Portfolio Drawdown  (Max: {dd.min():.1f}%)",
                       font=dict(color="#94a3b8", size=14)),
        ))
        fig_dd.update_xaxes(**GRID)
        fig_dd.update_yaxes(**GRID, ticksuffix="%")
        st.plotly_chart(fig_dd, use_container_width=True)

    # ── Holdings ──
    with pt4:
        for t in ptickers:
            df_t = load_prices(t, pper)
            if df_t.empty:
                continue
            tr_t  = trend_signal(df_t)
            mom_t = momentum_signal(df_t)
            vlt_t = vol_signal(df_t)
            r_t, _, rb_t, _, _ = get_rec(tr_t, mom_t, vlt_t)
            ret_t = (df_t["Close"].squeeze().iloc[-1] /
                     df_t["Close"].squeeze().iloc[0] - 1) * 100
            rc_t  = "#10b981" if ret_t >= 0 else "#ef4444"
            st.markdown(f"""
            <div class="el-card" style="display:flex;align-items:center;justify-content:space-between">
                <div>
                    <strong style="color:#f1f5f9;font-size:1.05rem">{t}</strong>
                    <span style="color:#475569;font-size:0.78rem;margin-left:.6rem">
                        {tr_t['label']} &nbsp;·&nbsp;
                        RSI {mom_t['rsi']:.0f} &nbsp;·&nbsp;
                        Vol {vlt_t['vol']:.1f}%
                    </span>
                </div>
                <div style="display:flex;align-items:center;gap:1rem">
                    <span style="color:{rc_t};font-weight:700;font-size:1rem">
                        {ret_t:+.2f}%
                    </span>
                    <span class="badge {rb_t}">{r_t}</span>
                </div>
            </div>""", unsafe_allow_html=True)

        # interpretation
        out   = m["outperf"]
        shr   = m["sharpe"]
        av    = m["ann_vol"]
        perf_i = "✅" if out  > 0 else "❌"
        risk_i = "✅" if av   < 0.2  else "⚠️"
        sr_i   = "✅" if shr >= 1    else ("⚠️" if shr >= 0.5 else "❌")
        out_lbl = "Outperformed" if out > 0 else "Underperformed"
        sr_lbl  = ("Excellent" if shr >= 2 else "Good" if shr >= 1
                   else "Fair" if shr >= 0.5 else "Poor — consider rebalancing")

        st.markdown(f"""
        <div class="interp-box" style="margin-top:1rem">
            <p style="color:#64748b;font-size:0.72rem;text-transform:uppercase;
               letter-spacing:.08em;font-weight:700;margin:0 0 .8rem">
               Portfolio Interpretation
            </p>
            <div class="interp-row">
                <span class="interp-icon">{perf_i}</span>
                <span>Portfolio returned <strong style="color:#f1f5f9">{pct(m['total'])}</strong>
                vs SPY <strong style="color:#94a3b8">{pct(m['bench'])}</strong>
                — <strong style="color:{'#10b981' if out>0 else '#ef4444'}">
                {out_lbl} by {pct(abs(out))}</strong></span>
            </div>
            <div class="interp-row">
                <span class="interp-icon">{risk_i}</span>
                <span>Annualized volatility of <strong style="color:#f1f5f9">{av*100:.1f}%</strong>
                — {"lower" if av < 0.20 else "higher"} than a typical 20% equity threshold</span>
            </div>
            <div class="interp-row">
                <span class="interp-icon">{sr_i}</span>
                <span>Sharpe ratio of <strong style="color:#f1f5f9">{shr:.2f}</strong>
                — {sr_lbl} risk-adjusted return</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# PAGE 3 — SCREENER
# ════════════════════════════════════════════
else:
    if not go_scr:
        st.markdown("""
        <div class="hero-container">
            <div class="hero-icon">🔍</div>
            <div class="hero-title">Stock Screener</div>
            <p class="hero-sub">
                Compare multiple stocks side-by-side with normalized performance,
                signal summaries, and ranked metrics. Add tickers and click
                <strong>Screen</strong>.
            </p>
        </div>""", unsafe_allow_html=True)
        st.stop()

    st.markdown(
        f"<h1 style='color:#f1f5f9;font-weight:800;font-size:1.9rem;"
        f"letter-spacing:-0.03em;margin:0'>Stock Screener</h1>"
        f"<p style='color:#475569;font-size:0.85rem;margin:4px 0 0'>"
        f"Comparing {len(stickers)} stocks &nbsp;·&nbsp; 6-Month window</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    rows = []
    bar  = st.progress(0, text="Fetching data…")
    for i, t in enumerate(stickers):
        df_t   = load_prices(t, "6mo")
        info_t = load_info(t)
        bar.progress((i+1)/len(stickers), text=f"Loading {t}…")
        if df_t.empty:
            continue
        tr_t   = trend_signal(df_t)
        mom_t  = momentum_signal(df_t)
        vlt_t  = vol_signal(df_t)
        rec_t, _, rb_t, _, _ = get_rec(tr_t, mom_t, vlt_t)
        ct = df_t["Close"].squeeze()
        r6 = float((ct.iloc[-1]/ct.iloc[0]-1)*100)
        r1 = float((ct.iloc[-1]/ct.iloc[-21]-1)*100) if len(ct)>=21 else None
        rows.append(dict(
            Ticker=t,
            Company=info_t.get("shortName", t),
            Price=f"${tr_t['price']:,.2f}",
            _6m=r6,
            **{"6M Ret": f"{r6:+.1f}%"},
            **{"1M Ret": f"{r1:+.1f}%" if r1 else "—"},
            RSI=f"{mom_t['rsi']:.1f}",
            Volatility=f"{vlt_t['vol']:.1f}%",
            **{"Vol Level": vlt_t["label"]},
            Trend=tr_t["label"],
            Signal=mom_t["label"],
            Rec=rec_t,
        ))
    bar.empty()

    if not rows:
        st.error("No data returned. Verify your tickers.")
        st.stop()

    # normalised chart
    fig_sc = go.Figure()
    for idx, t in enumerate(stickers):
        df_t = load_prices(t, "6mo")
        if df_t.empty:
            continue
        ct   = df_t["Close"].squeeze()
        norm = (ct / ct.iloc[0] - 1) * 100
        fig_sc.add_trace(go.Scatter(
            x=norm.index, y=norm, name=t,
            line=dict(color=COLORS[idx % len(COLORS)], width=2),
            hovertemplate=f"<b>{t}</b>: %{{y:.2f}}%<extra></extra>",
        ))
    fig_sc.add_hline(y=0, line_color="#1e2a45", line_width=1)
    apply_layout(fig_sc, dict(
        height=400,
        title=dict(text="6-Month Normalized Performance",
                   font=dict(color="#94a3b8", size=14)),
    ))
    fig_sc.update_xaxes(**GRID)
    fig_sc.update_yaxes(**GRID, ticksuffix="%")
    st.plotly_chart(fig_sc, use_container_width=True)

    # table
    st.markdown('<p class="section-title">Screener Results</p>', unsafe_allow_html=True)
    display_rows = [{k: v for k, v in r.items() if k != "_6m"} for r in rows]
    disp_df = pd.DataFrame(display_rows).set_index("Ticker")
    st.dataframe(disp_df, use_container_width=True,
                 height=min(42*len(disp_df)+52, 520))

    # signal tally
    st.markdown("---")
    buys  = [r["Ticker"] for r in rows if r["Rec"] == "BUY"]
    holds = [r["Ticker"] for r in rows if r["Rec"] == "HOLD"]
    sells = [r["Ticker"] for r in rows if r["Rec"] == "SELL"]

    sc1, sc2, sc3 = st.columns(3)
    for col, label, badge, tlist in [
        (sc1, "BUY Signals",  "badge-buy",  buys),
        (sc2, "HOLD Signals", "badge-hold", holds),
        (sc3, "SELL Signals", "badge-sell", sells),
    ]:
        chips = " ".join(
            f"<span class='badge {badge}'>{t}</span>" for t in tlist
        ) or "<span style='color:#334155'>None</span>"
        col.markdown(f"""
        <div class="el-card" style="text-align:center">
            <div class="el-label">{label}</div>
            <div class="el-value" style="margin:.4rem 0">{len(tlist)}</div>
            <div style="display:flex;flex-wrap:wrap;gap:5px;justify-content:center;margin-top:.5rem">
                {chips}
            </div>
        </div>""", unsafe_allow_html=True)
