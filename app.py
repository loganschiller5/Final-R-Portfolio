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

# ── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(
    page_title="EquityLens",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── SESSION STATE ──────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state.view = "home"
if "ticker" not in st.session_state:
    st.session_state.ticker = None

# ── CONSTANTS ──────────────────────────────────────────────────
WATCHLIST = [
    {"ticker": "AAPL",  "name": "Apple Inc.",      "sector": "Technology"},
    {"ticker": "MSFT",  "name": "Microsoft Corp.",  "sector": "Technology"},
    {"ticker": "NVDA",  "name": "NVIDIA Corp.",     "sector": "Semiconductors"},
    {"ticker": "GOOGL", "name": "Alphabet Inc.",    "sector": "Communication"},
    {"ticker": "JPM",   "name": "JPMorgan Chase",   "sector": "Financials"},
]
PORT_TICKERS = ["AAPL", "MSFT", "GOOGL", "NVDA", "JPM"]
PORT_WEIGHTS = {"AAPL": 0.25, "MSFT": 0.25, "GOOGL": 0.20, "NVDA": 0.20, "JPM": 0.10}
PALETTE = ["#3b82f6","#10b981","#f59e0b","#ef4444","#8b5cf6",
           "#06b6d4","#f97316","#84cc16","#ec4899","#14b8a6"]

# ── CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html,body,[class*="css"]{font-family:'Inter',sans-serif!important;background:#080c14!important;color:#e2e8f0!important}
.main .block-container{padding:2rem 2.5rem 3rem!important;max-width:100%!important;background:#080c14!important}
#MainMenu,footer,header{visibility:hidden}
section[data-testid="stSidebar"]{display:none}

/* ── metric cards ── */
[data-testid="metric-container"]{background:#0f1623!important;border:1px solid #1a2540!important;border-radius:14px!important;padding:1rem 1.25rem!important;transition:all .2s}
[data-testid="metric-container"]:hover{border-color:#3b82f6!important;box-shadow:0 0 18px rgba(59,130,246,.1)!important}
[data-testid="metric-container"] label{color:#4b5a72!important;font-size:.68rem!important;text-transform:uppercase!important;letter-spacing:.09em!important;font-weight:700!important}
[data-testid="stMetricValue"]{color:#f1f5f9!important;font-weight:800!important;font-size:1.35rem!important}
[data-testid="stMetricDelta"]{font-size:.78rem!important;font-weight:600!important}

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"]{background:#0f1623!important;border-radius:12px!important;padding:4px!important;border:1px solid #1a2540!important;gap:2px!important}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:#4b5a72!important;border-radius:9px!important;padding:9px 26px!important;font-weight:600!important;font-size:.84rem!important;border:none!important;transition:all .18s!important}
.stTabs [aria-selected="true"]{background:#1d4ed8!important;color:#fff!important;box-shadow:0 2px 12px rgba(29,78,216,.4)!important}

/* ── STOCK CARD BUTTONS — the key trick ── */
/* Each card is a full-width st.button styled to look like a card */
div[data-testid="stButton"].card-btn > button{
    background:linear-gradient(145deg,#0f1623,#0b101c)!important;
    border:1px solid #1a2540!important;
    border-radius:18px!important;
    padding:1.4rem 1.6rem!important;
    width:100%!important;
    text-align:left!important;
    cursor:pointer!important;
    transition:all .22s ease!important;
    color:#e2e8f0!important;
    font-family:'Inter',sans-serif!important;
    white-space:pre-wrap!important;
    height:auto!important;
    line-height:1.5!important;
}
div[data-testid="stButton"].card-btn > button:hover{
    border-color:#2563eb!important;
    box-shadow:0 8px 36px rgba(37,99,235,.18)!important;
    transform:translateY(-3px)!important;
    background:linear-gradient(145deg,#111d33,#0e1524)!important;
}

/* ── back button ── */
div[data-testid="stButton"].back-btn > button{
    background:#0f1623!important;color:#64748b!important;
    border:1px solid #1a2540!important;border-radius:9px!important;
    font-weight:600!important;font-size:.82rem!important;
    padding:.45rem 1.1rem!important;width:auto!important;
    transition:all .15s!important;
}
div[data-testid="stButton"].back-btn > button:hover{border-color:#3b82f6!important;color:#93c5fd!important;background:#0f1623!important}

/* ── generic buttons ── */
.stButton>button{background:#0f1623!important;color:#64748b!important;border:1px solid #1a2540!important;border-radius:9px!important;font-weight:600!important;font-size:.83rem!important;transition:all .18s!important}
.stButton>button:hover{background:#1a2540!important;color:#f1f5f9!important;border-color:#3b82f6!important}

/* ── radio ── */
.stRadio>div{flex-direction:row!important;gap:6px!important}
.stRadio label{background:#0f1623!important;border:1px solid #1a2540!important;border-radius:8px!important;padding:5px 14px!important;cursor:pointer!important;color:#64748b!important;font-size:.8rem!important;font-weight:600!important;transition:all .15s!important}
.stRadio label:has(input:checked){background:#1e3a8a!important;border-color:#3b82f6!important;color:#93c5fd!important}

/* ── selectbox ── */
.stSelectbox>div>div{background:#0f1623!important;border:1px solid #1a2540!important;border-radius:9px!important;color:#f1f5f9!important}

/* ── progress ── */
.stProgress>div>div>div{background:#3b82f6!important}

/* ── dataframe ── */
[data-testid="stDataFrame"]{border-radius:12px!important;border:1px solid #1a2540!important;overflow:hidden!important}

/* ── divider ── */
hr{border-color:#1a2540!important;margin:1.2rem 0!important}

/* ── custom components ── */
.logo{font-size:1.6rem;font-weight:800;letter-spacing:-.04em;color:#f1f5f9;line-height:1}
.logo-dot{color:#3b82f6}
.logo-sub{font-size:.7rem;color:#1e3a5f;text-transform:uppercase;letter-spacing:.1em;font-weight:700;margin-top:3px}

.mkt-bar{display:flex;gap:1.8rem;align-items:center;padding:.7rem 1.3rem;background:#0f1623;border-radius:12px;border:1px solid #1a2540;font-size:.79rem;flex-wrap:wrap}
.mkt-item{display:flex;gap:8px;align-items:center}
.mkt-label{color:#334155;font-weight:600}
.mkt-val{color:#f1f5f9;font-weight:700}
.mkt-pos{color:#10b981;font-weight:600}
.mkt-neg{color:#ef4444;font-weight:600}

.sec-label{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#1e3a5f;margin:1.5rem 0 .9rem;display:flex;align-items:center;gap:.8rem}
.sec-label::after{content:'';flex:1;height:1px;background:#111827}

.badge{display:inline-flex;align-items:center;padding:5px 16px;border-radius:99px;font-size:.78rem;font-weight:700;letter-spacing:.06em}
.badge-buy{background:rgba(16,185,129,.12);color:#10b981;border:1px solid rgba(16,185,129,.3)}
.badge-sell{background:rgba(239,68,68,.12);color:#ef4444;border:1px solid rgba(239,68,68,.3)}
.badge-hold{background:rgba(245,158,11,.12);color:#f59e0b;border:1px solid rgba(245,158,11,.3)}

.info-card{background:#0f1623;border:1px solid #1a2540;border-radius:14px;padding:1.2rem 1.4rem;height:100%}
.ic-label{font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;color:#1e3a5f;font-weight:700;margin-bottom:.4rem}
.ic-val{font-size:1.05rem;font-weight:800;line-height:1.1}
.ic-sub{font-size:.78rem;color:#334155;margin-top:.5rem;line-height:1.7}

.rec-panel{background:#0f1623;border-radius:16px;padding:1.5rem 1.8rem;position:relative;overflow:hidden;margin-top:1rem}
.rec-panel-buy{border:1px solid rgba(16,185,129,.22)}
.rec-panel-sell{border:1px solid rgba(239,68,68,.22)}
.rec-panel-hold{border:1px solid rgba(245,158,11,.22)}
.rec-panel::after{content:'';position:absolute;top:0;left:0;width:4px;height:100%;border-radius:16px 0 0 16px}
.rec-panel-buy::after{background:#10b981}
.rec-panel-sell::after{background:#ef4444}
.rec-panel-hold::after{background:#f59e0b}

.sec-title{font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:#1e3a5f;font-weight:700;margin-bottom:.9rem;padding-bottom:.5rem;border-bottom:1px solid #111827}

.weight-pill{display:inline-block;background:#111827;border:1px solid #1a2540;border-radius:6px;padding:2px 9px;font-size:.72rem;font-weight:700;color:#3b82f6}

.holding-row{background:#0f1623;border:1px solid #1a2540;border-radius:12px;padding:.85rem 1.2rem;margin-bottom:.5rem;display:flex;align-items:center;justify-content:space-between}

.interp-box{background:#0f1623;border:1px solid #1a2540;border-radius:14px;padding:1.3rem 1.5rem;margin-top:.8rem}
.interp-row{display:flex;align-items:flex-start;gap:.7rem;padding:.55rem 0;border-bottom:1px solid #080c14;font-size:.87rem;color:#64748b;line-height:1.6}
.interp-row:last-child{border-bottom:none}
</style>
""", unsafe_allow_html=True)


# ── PLOTLY HELPERS ─────────────────────────────────────────────
GRID = dict(gridcolor="#111827", zeroline=False, showline=False,
            tickfont=dict(size=10, color="#334155"))
BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#4b5a72", size=11),
    legend=dict(bgcolor="rgba(15,22,35,.9)", bordercolor="#1a2540",
                borderwidth=1, font=dict(size=11)),
    margin=dict(l=6, r=6, t=40, b=6),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#0f1623", bordercolor="#1a2540",
                    font=dict(family="Inter", size=11, color="#e2e8f0")),
)

def lay(fig, h=420, title=""):
    cfg = dict(**BASE, height=h)
    if title:
        cfg["title"] = dict(text=title, font=dict(color="#475569", size=13), x=0)
    fig.update_layout(**cfg)
    fig.update_xaxes(**GRID, rangeslider_visible=False)
    fig.update_yaxes(**GRID)
    return fig


# ── DATA ───────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def prices(ticker: str, period: str = "6mo") -> pd.DataFrame:
    try:
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]
        df.index = pd.to_datetime(df.index)
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=600, show_spinner=False)
def info(ticker: str) -> dict:
    try:
        return yf.Ticker(ticker).info or {}
    except Exception:
        return {}

@st.cache_data(ttl=300, show_spinner=False)
def quick(ticker: str):
    df = prices(ticker, "1mo")
    if df.empty:
        return None, None, None
    c = df["Close"].squeeze()
    return float(c.iloc[-1]), float((c.iloc[-1] - c.iloc[0]) / c.iloc[0]), c


# ── INDICATORS ─────────────────────────────────────────────────
def calc_rsi(s: pd.Series, n=14) -> pd.Series:
    d  = s.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    return (100 - 100 / (1 + up / dn.replace(0, np.nan))).rename("RSI")

def calc_macd(s: pd.Series):
    m   = (s.ewm(span=12,adjust=False).mean() - s.ewm(span=26,adjust=False).mean()).rename("MACD")
    sig = m.ewm(span=9, adjust=False).mean().rename("Signal")
    return m, sig, (m - sig).rename("Hist")

def calc_bb(s: pd.Series, n=20):
    mid = s.rolling(n).mean()
    std = s.rolling(n).std()
    return (mid+2*std).rename("U"), mid.rename("M"), (mid-2*std).rename("L")

def ann_vol(s: pd.Series) -> float:
    return float(s.pct_change().dropna().rolling(20).std().iloc[-1] * np.sqrt(252) * 100)


# ── SIGNALS ────────────────────────────────────────────────────
def trend_sig(df):
    c = df["Close"].squeeze()
    px, m20, m50 = float(c.iloc[-1]), float(c.rolling(20).mean().iloc[-1]), float(c.rolling(50).mean().iloc[-1])
    if px > m20 > m50:   lbl, col = "Strong Uptrend",   "#10b981"
    elif px < m20 < m50: lbl, col = "Strong Downtrend", "#ef4444"
    else:                lbl, col = "Mixed / Sideways", "#f59e0b"
    return dict(px=px, m20=m20, m50=m50, lbl=lbl, col=col)

def mom_sig(df):
    r  = calc_rsi(df["Close"].squeeze())
    rv = float(r.iloc[-1])
    if rv > 70:   lbl, col = "Overbought", "#ef4444"
    elif rv < 30: lbl, col = "Oversold",   "#10b981"
    else:         lbl, col = "Neutral",    "#64748b"
    return dict(val=rv, lbl=lbl, col=col, series=r)

def vol_sig(df):
    v = ann_vol(df["Close"].squeeze())
    if v > 40:   lbl, col = "High",   "#ef4444"
    elif v > 25: lbl, col = "Medium", "#f59e0b"
    else:        lbl, col = "Low",    "#10b981"
    return dict(val=v, lbl=lbl, col=col)

def get_rec(tr, mo, vl):
    if "Uptrend" in tr["lbl"] and mo["val"] < 70 and vl["val"] < 55:
        return ("BUY","#10b981","badge-buy","rec-panel-buy",
                f"Price above both MAs. RSI {mo['val']:.0f} — trend intact, volatility manageable at {vl['val']:.0f}%.")
    elif "Downtrend" in tr["lbl"] or mo["val"] > 75:
        return ("SELL","#ef4444","badge-sell","rec-panel-sell",
                f"Bearish structure or overbought RSI ({mo['val']:.0f}). Consider reducing exposure.")
    else:
        return ("HOLD","#f59e0b","badge-hold","rec-panel-hold",
                f"Mixed signals — RSI {mo['val']:.0f}, trend unclear. Monitor for directional break.")


# ── PORTFOLIO CALC ─────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def port_calc(tickers: tuple, weights: tuple, period: str):
    frames = {}
    for t in tickers:
        df = prices(t, period)
        if not df.empty:
            frames[t] = df["Close"].squeeze()
    if not frames:
        return None
    px_df  = pd.DataFrame(frames).dropna()
    rets   = px_df.pct_change().dropna()
    wd     = dict(zip(tickers, weights))
    w      = np.array([wd.get(t, 0) for t in px_df.columns], dtype=float)
    w     /= w.sum()
    pr     = rets.dot(w)
    spy_df = prices("SPY", period)
    sr     = spy_df["Close"].squeeze().pct_change().dropna() if not spy_df.empty else None
    total  = float((1+pr).prod()-1)
    av     = float(pr.std()*np.sqrt(252))
    sharpe = float((pr.mean()*252)/av) if av>0 else 0.0
    bt     = float((1+sr).prod()-1) if sr is not None else 0.0
    cum    = (1+pr).cumprod()
    bc     = (1+sr).cumprod() if sr is not None else None
    dd     = (cum-cum.cummax())/cum.cummax()*100
    return dict(total=total, av=av, sharpe=sharpe, bt=bt,
                outperf=total-bt, cum=cum, bc=bc, rets=rets, pr=pr, dd=dd)


# ── FORMAT ─────────────────────────────────────────────────────
def pct(v, signed=True):
    return f"{'+'if signed and v>=0 else''}{v*100:.2f}%"

def bignum(v, pre="$"):
    if not v: return "—"
    if v>=1e12: return f"{pre}{v/1e12:.2f}T"
    if v>=1e9:  return f"{pre}{v/1e9:.2f}B"
    if v>=1e6:  return f"{pre}{v/1e6:.2f}M"
    return f"{pre}{v:,.0f}"

def spark_svg(s: pd.Series, chg: float, idx: int) -> str:
    if s is None or len(s) < 2: return ""
    norm = (s - s.min()) / (s.max() - s.min() + 1e-9)
    pts  = list(norm.values)
    W, H = 160, 38
    step = W / max(len(pts)-1, 1)
    path = " ".join(f"{'M' if j==0 else 'L'}{x*step:.1f},{(1-y)*(H-4)+2:.1f}"
                    for j,(x,y) in enumerate(zip(range(len(pts)), pts)))
    lx = (len(pts)-1)*step; ly = (1-pts[-1])*(H-4)+2
    sc = "#10b981" if chg >= 0 else "#ef4444"
    gid = f"sg{idx}"
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" height="{H}" preserveAspectRatio="none" style="display:block;margin-top:6px">'
            f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{sc}" stop-opacity="0.2"/>'
            f'<stop offset="100%" stop-color="{sc}" stop-opacity="0.01"/>'
            f'</linearGradient></defs>'
            f'<path d="{path} L{lx:.1f},{H} L0,{H} Z" fill="url(#{gid})"/>'
            f'<path d="{path}" fill="none" stroke="{sc}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="2.5" fill="{sc}"/>'
            f'</svg>')


# ════════════════════════════════════════════════════════════════
# HOME PAGE
# ════════════════════════════════════════════════════════════════
def render_home():
    # ── Logo + Market Bar ──────────────────────────
    col_logo, col_mkt = st.columns([1, 2])
    with col_logo:
        st.markdown("""
        <div style="padding:.2rem 0 1rem">
          <div class="logo">Equity<span class="logo-dot">Lens</span></div>
          <div class="logo-sub">Market Dashboard · Live Data</div>
        </div>""", unsafe_allow_html=True)
    with col_mkt:
        mkt_parts = []
        for sym, label in {"SPY":"S&P 500","QQQ":"NASDAQ","DIA":"DOW JONES"}.items():
            px_, chg_, _ = quick(sym)
            if px_ is not None:
                css = "mkt-pos" if chg_ >= 0 else "mkt-neg"
                arr = "▲" if chg_ >= 0 else "▼"
                mkt_parts.append(
                    f"<div class='mkt-item'><span class='mkt-label'>{label}</span>"
                    f"<span class='mkt-val'>${px_:,.2f}</span>"
                    f"<span class='{css}'>{arr} {abs(chg_)*100:.2f}%</span></div>")
        st.markdown(f"<div class='mkt-bar' style='margin-top:.3rem'>{''.join(mkt_parts)}</div>",
                    unsafe_allow_html=True)

    st.markdown("<div class='sec-label'>Watchlist — select a stock to explore</div>",
                unsafe_allow_html=True)

    # ── 5 Stock Cards ─────────────────────────────
    cols = st.columns(5, gap="small")
    for i, stock in enumerate(WATCHLIST):
        t = stock["ticker"]
        px_, chg_, spark = quick(t)
        pos  = (chg_ or 0) >= 0
        arr  = "▲" if pos else "▼"
        css  = "#10b981" if pos else "#ef4444"
        svg  = spark_svg(spark, chg_ or 0, i)
        px_s = f"${px_:,.2f}" if px_ else "—"
        c_s  = f"{arr} {abs(chg_ or 0)*100:.2f}%" if chg_ is not None else "—"

        # Build the card label that goes INSIDE the button
        label = (
            f"{stock['sector']}\n"
            f"{t}  ·  {stock['name']}\n"
            f"{px_s}  {c_s} 1M"
        )

        with cols[i]:
            # Render sparkline above the button area
            st.markdown(f"""
            <div style="background:linear-gradient(145deg,#0f1623,#0b101c);
                        border:1px solid #1a2540;border-radius:18px;
                        padding:1.4rem 1.6rem 0.2rem;margin-bottom:-2px;
                        border-bottom:none;border-radius:18px 18px 0 0">
              <div style="font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;
                          color:#1e3a5f;font-weight:700;margin-bottom:.35rem">{stock['sector']}</div>
              <div style="font-size:.82rem;color:#475569;margin-bottom:.1rem;font-weight:500">{stock['name']}</div>
              <div style="font-size:1.7rem;font-weight:800;color:#f1f5f9;
                          letter-spacing:-.03em;line-height:1.1">{t}</div>
              <div style="font-size:1.1rem;font-weight:700;color:#f1f5f9;margin-top:.5rem">{px_s}</div>
              <div style="color:{css};font-size:.82rem;font-weight:600">{c_s}
                <span style="color:#1e3a5f;font-size:.68rem;margin-left:4px">1M</span>
              </div>
              {svg}
            </div>""", unsafe_allow_html=True)

            # Real Streamlit button — styled via CSS class below the card visual
            st.markdown(f"""
            <style>
            div[data-testid="stButton"]:has(button[kind="secondary"]#btn_{t}) > button {{
                border-radius: 0 0 18px 18px !important;
                border-top: none !important;
                background: linear-gradient(145deg,#0f1623,#0b101c) !important;
                color: #3b82f6 !important;
                font-size: .78rem !important;
                font-weight: 700 !important;
                padding: .6rem 1.6rem .9rem !important;
                letter-spacing: .04em !important;
                text-transform: uppercase !important;
            }}
            div[data-testid="stButton"]:has(button[kind="secondary"]#btn_{t}) > button:hover {{
                background: linear-gradient(145deg,#111d33,#0e1524) !important;
                border-color: #2563eb !important;
                color: #60a5fa !important;
                transform: none !important;
            }}
            </style>
            """, unsafe_allow_html=True)

            clicked = st.button(
                f"Open {t}  →",
                key=f"btn_{t}",
                use_container_width=True,
            )
            if clicked:
                st.session_state.view   = "stock"
                st.session_state.ticker = t
                st.rerun()

    # ── Portfolio Strip ────────────────────────────
    st.markdown("<div class='sec-label' style='margin-top:2rem'>Portfolio Snapshot · 1 Year</div>",
                unsafe_allow_html=True)
    m = port_calc(tuple(PORT_TICKERS),
                  tuple(PORT_WEIGHTS[t] for t in PORT_TICKERS), "1y")
    if m:
        pm1,pm2,pm3,pm4,pm5 = st.columns(5)
        pm1.metric("Portfolio Return", pct(m["total"]),    f"SPY {pct(m['bt'])}")
        pm2.metric("vs Benchmark",     pct(m["outperf"]),  "Outperform ↑" if m["outperf"]>0 else "Underperform ↓")
        pm3.metric("Ann. Volatility",  f"{m['av']*100:.1f}%")
        pm4.metric("Sharpe Ratio",     f"{m['sharpe']:.2f}", "≥1 Good")
        pm5.metric("Max Drawdown",     f"{m['dd'].min():.1f}%")

        cum, bc = m["cum"], m["bc"]
        fp = go.Figure()
        fp.add_trace(go.Scatter(x=cum.index, y=(cum-1)*100, name="Portfolio",
            fill="tozeroy", fillcolor="rgba(59,130,246,.07)",
            line=dict(color="#3b82f6", width=2.2)))
        if bc is not None:
            fp.add_trace(go.Scatter(x=bc.index, y=(bc-1)*100, name="SPY",
                line=dict(color="#1e3a5f", width=1.3, dash="dot")))
        fp.add_hline(y=0, line_color="#111827", line_width=1)
        lay(fp, h=210, title="1-Year Cumulative Return vs SPY")
        fp.update_yaxes(ticksuffix="%", **GRID)
        st.plotly_chart(fp, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# STOCK DETAIL PAGE
# ════════════════════════════════════════════════════════════════
def render_stock(ticker: str):

    # ── Back ──────────────────────────────────────
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Back to Dashboard", key="back"):
        st.session_state.view   = "home"
        st.session_state.ticker = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Fetch ──────────────────────────────────────
    with st.spinner(f"Loading {ticker}…"):
        df   = prices(ticker, "6mo")
        nfo  = info(ticker)

    if df.empty:
        st.error(f"No data for {ticker}. Check the symbol.")
        return

    close = df["Close"].squeeze()

    # ── Compute all indicators ──────────────────────
    tr  = trend_sig(df)
    mo  = mom_sig(df)
    vl  = vol_sig(df)
    rec, rec_col, rec_badge, rec_panel, rec_reason = get_rec(tr, mo, vl)

    rsi_s             = mo["series"]
    m_macd, m_sig_l, m_hist = calc_macd(close)
    b_up, b_mid, b_lo = calc_bb(close)

    px_now = tr["px"]
    chg_6m = (px_now - float(close.iloc[0])) / float(close.iloc[0])

    name   = nfo.get("longName",          ticker)
    sector = nfo.get("sector",            "—")
    mkcap  = nfo.get("marketCap",         0)
    pe     = nfo.get("trailingPE",        None)
    eps_v  = nfo.get("trailingEps",       None)
    h52    = nfo.get("fiftyTwoWeekHigh",  None)
    l52    = nfo.get("fiftyTwoWeekLow",   None)
    beta   = nfo.get("beta",              None)
    dy     = nfo.get("dividendYield",     None)

    # ── Stock header ──────────────────────────────
    ch_col = "#10b981" if chg_6m >= 0 else "#ef4444"
    ch_arr = "▲" if chg_6m >= 0 else "▼"

    hc1, hc2, hc3 = st.columns([3,1,1])
    with hc1:
        st.markdown(f"""
        <div>
          <div style="color:#1e3a5f;font-size:.68rem;text-transform:uppercase;
                      letter-spacing:.1em;font-weight:700;margin-bottom:4px">{sector}</div>
          <div style="font-size:2rem;font-weight:800;color:#f1f5f9;
                      letter-spacing:-.04em;line-height:1.1">{name}</div>
          <div style="margin-top:3px">
            <span style="color:#3b82f6;font-weight:700;font-size:.9rem">{ticker}</span>
            <span style="color:#1a2540;margin:0 6px">·</span>
            <span style="color:#334155;font-size:.85rem">{bignum(mkcap)} Market Cap</span>
          </div>
        </div>""", unsafe_allow_html=True)
    with hc2:
        st.markdown(f"""
        <div style="text-align:right;padding-top:.4rem">
          <div style="font-size:2rem;font-weight:800;color:#f1f5f9">${px_now:,.2f}</div>
          <div style="color:{ch_col};font-size:.9rem;font-weight:700">
            {ch_arr} {abs(chg_6m)*100:.2f}%
            <span style="color:#1e3a5f;font-size:.7rem"> 6M</span>
          </div>
        </div>""", unsafe_allow_html=True)
    with hc3:
        st.markdown(
            f"<div style='text-align:right;padding-top:.7rem'>"
            f"<span class='badge {rec_badge}' style='font-size:.9rem;padding:8px 22px'>⬟ {rec}</span>"
            f"</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── KPI Row ───────────────────────────────────
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.metric("Price",      f"${px_now:,.2f}",  pct(chg_6m))
    k2.metric("20-Day MA",  f"${tr['m20']:,.2f}")
    k3.metric("50-Day MA",  f"${tr['m50']:,.2f}")
    k4.metric("RSI (14)",   f"{mo['val']:.1f}",  mo["lbl"])
    k5.metric("Ann. Vol",   f"{vl['val']:.1f}%", vl["lbl"])
    k6.metric("Beta",       f"{beta:.2f}" if beta else "—")

    st.markdown("")

    # ════════ TABS ════════════════════════════════
    tab_a, tab_p = st.tabs(["📊  Technical Analysis", "💼  Portfolio"])

    # ── TAB: TECHNICAL ANALYSIS ────────────────────────────────
    with tab_a:

        # Chart type radio
        ct_c, _ = st.columns([2, 6])
        with ct_c:
            chart_type = st.radio("Chart", ["Candlestick", "Line"],
                                  horizontal=True, key="ctype",
                                  label_visibility="collapsed")

        # ── Main Price + Volume Chart ──
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.73, 0.27], vertical_spacing=0.02)

        if chart_type == "Candlestick":
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"].squeeze(), high=df["High"].squeeze(),
                low=df["Low"].squeeze(),   close=close,
                increasing_line_color="#10b981", increasing_fillcolor="#10b981",
                decreasing_line_color="#ef4444", decreasing_fillcolor="#ef4444",
                name=ticker, showlegend=False,
            ), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(
                x=df.index, y=close, name=ticker,
                line=dict(color="#3b82f6", width=2.3), showlegend=False,
            ), row=1, col=1)

        # MA 20
        fig.add_trace(go.Scatter(
            x=df.index, y=close.rolling(20).mean(), name="MA 20",
            line=dict(color="#f59e0b", width=1.5, dash="dot"),
        ), row=1, col=1)
        # MA 50
        fig.add_trace(go.Scatter(
            x=df.index, y=close.rolling(50).mean(), name="MA 50",
            line=dict(color="#ef4444", width=1.5, dash="dot"),
        ), row=1, col=1)
        # Bollinger Bands
        fig.add_trace(go.Scatter(
            x=df.index, y=b_up, name="BB Upper",
            line=dict(color="#8b5cf6", width=1, dash="dash"),
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=b_lo, name="BB Lower",
            line=dict(color="#8b5cf6", width=1, dash="dash"),
            fill="tonexty", fillcolor="rgba(139,92,246,.05)",
        ), row=1, col=1)
        # Volume
        vc = ["#10b981" if float(c_)>=float(o_) else "#ef4444"
              for c_,o_ in zip(df["Close"].squeeze(), df["Open"].squeeze())]
        fig.add_trace(go.Bar(
            x=df.index, y=df["Volume"].squeeze(),
            marker_color=vc, opacity=0.5, name="Volume", showlegend=False,
        ), row=2, col=1)

        lay(fig, h=520)
        fig.update_yaxes(row=2, col=1, title_text="Volume",
                         title_font=dict(size=9, color="#1e3a5f"), **GRID)
        st.plotly_chart(fig, use_container_width=True)

        # ── RSI + MACD side-by-side ──
        ic1, ic2 = st.columns(2)

        with ic1:
            st.markdown('<p class="sec-title">RSI — 14 Day</p>', unsafe_allow_html=True)
            fr = go.Figure()
            fr.add_hrect(y0=70, y1=100, fillcolor="rgba(239,68,68,.05)", line_width=0)
            fr.add_hrect(y0=0,  y1=30,  fillcolor="rgba(16,185,129,.05)", line_width=0)
            fr.add_hline(y=70, line_dash="dot", line_color="#ef4444", line_width=1,
                         annotation_text="Overbought 70",
                         annotation_font=dict(size=9, color="#ef4444"),
                         annotation_position="top right")
            fr.add_hline(y=30, line_dash="dot", line_color="#10b981", line_width=1,
                         annotation_text="Oversold 30",
                         annotation_font=dict(size=9, color="#10b981"),
                         annotation_position="bottom right")
            fr.add_trace(go.Scatter(
                x=rsi_s.index, y=rsi_s, name="RSI",
                line=dict(color="#60a5fa", width=2.2),
                fill="tozeroy", fillcolor="rgba(96,165,250,.05)",
            ))
            lay(fr, h=265)
            fr.update_yaxes(range=[0, 100], **GRID)
            st.plotly_chart(fr, use_container_width=True)

        with ic2:
            st.markdown('<p class="sec-title">MACD — 12 / 26 / 9</p>', unsafe_allow_html=True)
            fm = go.Figure()
            hc = ["#10b981" if v>=0 else "#ef4444" for v in m_hist.fillna(0)]
            fm.add_trace(go.Bar(x=df.index, y=m_hist, marker_color=hc, opacity=0.7, name="Histogram"))
            fm.add_trace(go.Scatter(x=df.index, y=m_macd,
                                    line=dict(color="#3b82f6", width=2), name="MACD"))
            fm.add_trace(go.Scatter(x=df.index, y=m_sig_l,
                                    line=dict(color="#f59e0b", width=1.5, dash="dot"), name="Signal"))
            lay(fm, h=265)
            st.plotly_chart(fm, use_container_width=True)

        # ── Bollinger standalone ──
        st.markdown('<p class="sec-title">Bollinger Bands (20-Day, ±2σ)</p>', unsafe_allow_html=True)
        fbb = go.Figure()
        fbb.add_trace(go.Scatter(x=df.index, y=b_up, name="Upper Band",
                                  line=dict(color="#8b5cf6", width=1.2, dash="dash")))
        fbb.add_trace(go.Scatter(x=df.index, y=b_mid, name="Middle Band (MA 20)",
                                  line=dict(color="#475569", width=1, dash="dot")))
        fbb.add_trace(go.Scatter(x=df.index, y=b_lo, name="Lower Band",
                                  line=dict(color="#8b5cf6", width=1.2, dash="dash"),
                                  fill="tonexty", fillcolor="rgba(139,92,246,.06)"))
        fbb.add_trace(go.Scatter(x=df.index, y=close, name="Price",
                                  line=dict(color="#3b82f6", width=2)))
        lay(fbb, h=260)
        st.plotly_chart(fbb, use_container_width=True)

        # ── Volatility Gauge ──
        st.markdown('<p class="sec-title">Annualized Volatility — 20 Day</p>', unsafe_allow_html=True)
        fg = go.Figure(go.Indicator(
            mode="gauge+number",
            value=vl["val"],
            number=dict(suffix="%", font=dict(color="#f1f5f9", size=34, family="Inter")),
            gauge=dict(
                axis=dict(range=[0,80], tickcolor="#1a2540",
                          tickfont=dict(color="#1e3a5f", size=9)),
                bar=dict(color=vl["col"], thickness=0.25),
                bgcolor="#0f1623", borderwidth=0,
                steps=[dict(range=[0,25],  color="#051209"),
                       dict(range=[25,40], color="#120d02"),
                       dict(range=[40,80], color="#120202")],
            ),
            title=dict(text=f"Level: <b style='color:{vl['col']}'>{vl['lbl']}</b>",
                       font=dict(size=12, color="#334155", family="Inter")),
        ))
        fg.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=230,
                         font=dict(family="Inter", color="#334155"),
                         margin=dict(l=20,r=20,t=20,b=10))
        st.plotly_chart(fg, use_container_width=True)

        # ── Signal Cards ──
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"""
            <div class="info-card">
              <div class="ic-label">📊 Trend Analysis</div>
              <div class="ic-val" style="color:{tr['col']}">{tr['lbl']}</div>
              <div class="ic-sub">
                Price &nbsp;<b style="color:#f1f5f9">${tr['px']:,.2f}</b><br>
                MA 20 &nbsp;<b style="color:#f59e0b">${tr['m20']:,.2f}</b><br>
                MA 50 &nbsp;<b style="color:#ef4444">${tr['m50']:,.2f}</b><br>
                <span style="color:#10b981">Price &gt; MA20 &gt; MA50 = Uptrend</span>
              </div>
            </div>""", unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
            <div class="info-card">
              <div class="ic-label">⚡ Momentum (RSI 14)</div>
              <div class="ic-val" style="color:{mo['col']}">{mo['lbl']}</div>
              <div class="ic-sub">
                RSI &nbsp;<b style="color:#f1f5f9">{mo['val']:.2f}</b><br>
                <span style="color:#10b981">＜ 30 = Oversold → Buy Signal</span><br>
                <span style="color:#ef4444">＞ 70 = Overbought → Sell Signal</span><br>
                <span style="color:#64748b">30–70 = Neutral</span>
              </div>
            </div>""", unsafe_allow_html=True)
        with sc3:
            st.markdown(f"""
            <div class="info-card">
              <div class="ic-label">🌊 Volatility (20D Ann.)</div>
              <div class="ic-val" style="color:{vl['col']}">{vl['lbl']}</div>
              <div class="ic-sub">
                Ann. Vol &nbsp;<b style="color:#f1f5f9">{vl['val']:.1f}%</b><br>
                <span style="color:#10b981">＜ 25% = Low risk</span><br>
                <span style="color:#f59e0b">25–40% = Medium risk</span><br>
                <span style="color:#ef4444">＞ 40% = High risk</span>
              </div>
            </div>""", unsafe_allow_html=True)

        # ── Recommendation Panel ──
        st.markdown(f"""
        <div class="rec-panel {rec_panel}">
          <div style="display:flex;align-items:center;gap:1.1rem;margin-bottom:.75rem">
            <span class="badge {rec_badge}" style="font-size:1rem;padding:8px 24px">⬟ {rec}</span>
            <div>
              <div style="color:#f1f5f9;font-weight:700;font-size:.95rem;margin-bottom:3px">
                Trading Recommendation
              </div>
              <div style="color:#475569;font-size:.84rem">{rec_reason}</div>
            </div>
          </div>
          <p style="color:#1e3a5f;font-size:.68rem;margin:0;
                    border-top:1px solid #111827;padding-top:.65rem">
            ⚠ Based on technical indicators only. Not investment advice. Always do your own research.
          </p>
        </div>""", unsafe_allow_html=True)

        # ── Fundamentals ──
        if any([pe, eps_v, h52, l52, beta, dy]):
            st.markdown("---")
            st.markdown('<p class="sec-title">Company Fundamentals</p>', unsafe_allow_html=True)
            fb1,fb2,fb3,fb4,fb5,fb6 = st.columns(6)
            fb1.metric("P/E Ratio",  f"{pe:.1f}×"      if pe    else "—")
            fb2.metric("EPS (TTM)",  f"${eps_v:.2f}"   if eps_v else "—")
            fb3.metric("52W High",   f"${h52:,.2f}"    if h52   else "—")
            fb4.metric("52W Low",    f"${l52:,.2f}"    if l52   else "—")
            fb5.metric("Div Yield",  f"{dy*100:.2f}%"  if dy    else "—")
            fb6.metric("Beta",       f"{beta:.2f}"     if beta  else "—")

    # ── TAB: PORTFOLIO ─────────────────────────────────────────
    with tab_p:
        PPER_MAP = {"6 Months":"6mo","1 Year":"1y","2 Years":"2y"}
        pc1,_ = st.columns([2,5])
        with pc1:
            pper_lbl = st.selectbox("Period", list(PPER_MAP.keys()), index=1, key="pp")
        pper = PPER_MAP[pper_lbl]

        m = port_calc(tuple(PORT_TICKERS),
                      tuple(PORT_WEIGHTS[t] for t in PORT_TICKERS), pper)
        if m is None:
            st.error("Could not load portfolio data.")
            return

        pills = " ".join(f"<span class='weight-pill'>{t} {PORT_WEIGHTS[t]*100:.0f}%</span>"
                         for t in PORT_TICKERS)
        st.markdown(f"<div style='margin:.2rem 0 1rem;display:flex;flex-wrap:wrap;gap:5px'>{pills}</div>",
                    unsafe_allow_html=True)

        pk1,pk2,pk3,pk4,pk5 = st.columns(5)
        pk1.metric("Total Return",    pct(m["total"]),      f"SPY {pct(m['bt'])}")
        pk2.metric("vs Benchmark",    pct(m["outperf"]),    "Outperform ↑" if m["outperf"]>0 else "Underperform ↓")
        pk3.metric("Ann. Volatility", f"{m['av']*100:.1f}%")
        pk4.metric("Sharpe Ratio",    f"{m['sharpe']:.2f}", "≥1 Good · ≥2 Excellent")
        pk5.metric("Max Drawdown",    f"{m['dd'].min():.1f}%")

        st.markdown("")
        pt1,pt2,pt3 = st.tabs(["📈  Performance","🥧  Allocation","⚡  Risk"])

        # ── Performance ──
        with pt1:
            cum, bc = m["cum"], m["bc"]
            fpp = go.Figure()
            fpp.add_trace(go.Scatter(x=cum.index, y=(cum-1)*100, name="Portfolio",
                fill="tozeroy", fillcolor="rgba(59,130,246,.07)",
                line=dict(color="#3b82f6", width=2.5)))
            if bc is not None:
                fpp.add_trace(go.Scatter(x=bc.index, y=(bc-1)*100, name="SPY",
                    line=dict(color="#1e3a5f", width=1.4, dash="dot")))
            fpp.add_hline(y=0, line_color="#111827", line_width=1)
            lay(fpp, h=360, title="Cumulative Return vs SPY")
            fpp.update_yaxes(ticksuffix="%", **GRID)
            st.plotly_chart(fpp, use_container_width=True)

            pr_  = m["pr"]
            rsh  = (pr_.rolling(21).mean()/pr_.rolling(21).std())*np.sqrt(252)
            frsh = go.Figure()
            frsh.add_trace(go.Scatter(x=rsh.index, y=rsh, name="Rolling Sharpe (21d)",
                fill="tozeroy", fillcolor="rgba(139,92,246,.06)",
                line=dict(color="#8b5cf6", width=2)))
            frsh.add_hline(y=1, line_dash="dot", line_color="#10b981", line_width=1,
                           annotation_text="Sharpe = 1",
                           annotation_font=dict(size=9, color="#10b981"))
            frsh.add_hline(y=0, line_color="#111827", line_width=1)
            lay(frsh, h=205, title="Rolling 21-Day Sharpe Ratio")
            frsh.update_yaxes(**GRID)
            st.plotly_chart(frsh, use_container_width=True)

        # ── Allocation ──
        with pt2:
            ac1, ac2 = st.columns(2)
            with ac1:
                fpie = go.Figure(go.Pie(
                    labels=PORT_TICKERS,
                    values=[PORT_WEIGHTS[t]*100 for t in PORT_TICKERS],
                    hole=0.58,
                    marker=dict(colors=PALETTE[:len(PORT_TICKERS)],
                                line=dict(color="#080c14", width=2.5)),
                    textinfo="label+percent",
                    textfont=dict(color="#f1f5f9", size=11),
                ))
                fpie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                    height=300, margin=dict(l=6,r=6,t=36,b=6),
                    font=dict(family="Inter"),
                    title=dict(text="Allocation Weights", font=dict(color="#475569",size=13), x=0),
                    annotations=[dict(text="Portfolio",x=0.5,y=0.5,
                                      font=dict(size=11,color="#1e3a5f"), showarrow=False)],
                )
                st.plotly_chart(fpie, use_container_width=True)

            with ac2:
                ind_r = {}
                for t_ in PORT_TICKERS:
                    dft = prices(t_, pper)
                    if not dft.empty:
                        c_ = dft["Close"].squeeze()
                        ind_r[t_] = float((c_.iloc[-1]/c_.iloc[0]-1)*100)
                s_r  = dict(sorted(ind_r.items(), key=lambda x:x[1], reverse=True))
                fbar = go.Figure(go.Bar(
                    x=list(s_r.keys()), y=list(s_r.values()),
                    marker_color=[PALETTE[0] if v>=0 else "#ef4444" for v in s_r.values()],
                    text=[f"{v:.1f}%" for v in s_r.values()],
                    textposition="outside", textfont=dict(color="#475569",size=11),
                ))
                lay(fbar, h=300, title="Individual Stock Returns")
                fbar.update_yaxes(ticksuffix="%", **GRID)
                st.plotly_chart(fbar, use_container_width=True)

            st.markdown('<p class="sec-title" style="margin-top:.8rem">Holdings</p>',
                        unsafe_allow_html=True)
            for t_ in PORT_TICKERS:
                dft = prices(t_, pper)
                if dft.empty: continue
                trt = trend_sig(dft); mot = mom_sig(dft); vlt = vol_sig(dft)
                rt,_,rbt,_,_ = get_rec(trt, mot, vlt)
                rv  = (dft["Close"].squeeze().iloc[-1]/dft["Close"].squeeze().iloc[0]-1)*100
                rc_ = "#10b981" if rv>=0 else "#ef4444"
                wt_ = f"{PORT_WEIGHTS.get(t_,0)*100:.0f}%"
                st.markdown(f"""
                <div class="holding-row">
                  <div style="display:flex;align-items:center;gap:.9rem">
                    <span style="color:#f1f5f9;font-weight:700">{t_}</span>
                    <span class="weight-pill">{wt_}</span>
                    <span style="color:#1e3a5f;font-size:.76rem">
                      {trt['lbl']} · RSI {mot['val']:.0f} · Vol {vlt['val']:.0f}%
                    </span>
                  </div>
                  <div style="display:flex;align-items:center;gap:.9rem">
                    <span style="color:{rc_};font-weight:700">{rv:+.2f}%</span>
                    <span class="badge {rbt}">{rt}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

        # ── Risk ──
        with pt3:
            rr1, rr2 = st.columns(2)
            with rr1:
                pr_ = m["pr"]
                fh  = go.Figure()
                fh.add_trace(go.Histogram(x=pr_*100, nbinsx=40, name="Daily Returns",
                    marker_color="#3b82f6", opacity=0.7))
                fh.add_vline(x=float(pr_.mean()*100), line_dash="dot",
                             line_color="#10b981", line_width=1.5,
                             annotation_text="Mean",
                             annotation_font=dict(size=9,color="#10b981"))
                lay(fh, h=280, title="Daily Return Distribution")
                fh.update_xaxes(ticksuffix="%", **GRID)
                fh.update_yaxes(**GRID)
                st.plotly_chart(fh, use_container_width=True)

            with rr2:
                rets = m["rets"]
                if rets.shape[1] > 1:
                    corr = rets.corr().round(2)
                    fhm  = go.Figure(go.Heatmap(
                        z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
                        colorscale=[[0,"#ef4444"],[0.5,"#0f1623"],[1,"#3b82f6"]],
                        zmin=-1, zmax=1,
                        text=[[f"{v:.2f}" for v in row] for row in corr.values],
                        texttemplate="%{text}", textfont=dict(size=11,color="#f1f5f9"),
                    ))
                    fhm.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        height=280, margin=dict(l=6,r=6,t=36,b=6),
                        font=dict(family="Inter",color="#4b5a72"),
                        title=dict(text="Correlation Matrix",
                                   font=dict(color="#475569",size=13),x=0),
                    )
                    fhm.update_xaxes(showgrid=False)
                    fhm.update_yaxes(showgrid=False)
                    st.plotly_chart(fhm, use_container_width=True)

            dd = m["dd"]
            fdd = go.Figure()
            fdd.add_trace(go.Scatter(x=dd.index, y=dd, name="Drawdown",
                fill="tozeroy", fillcolor="rgba(239,68,68,.08)",
                line=dict(color="#ef4444", width=1.5)))
            lay(fdd, h=210, title=f"Portfolio Drawdown  (Max: {dd.min():.1f}%)")
            fdd.update_yaxes(ticksuffix="%", **GRID)
            st.plotly_chart(fdd, use_container_width=True)

            out_=m["outperf"]; sh_=m["sharpe"]; av_=m["av"]
            pi="✅" if out_>0 else "❌"
            ri="✅" if av_<.20 else "⚠️"
            si="✅" if sh_>=1 else ("⚠️" if sh_>=.5 else "❌")
            ol="Outperformed" if out_>0 else "Underperformed"
            sl=("Excellent" if sh_>=2 else "Good" if sh_>=1 else "Fair" if sh_>=.5 else "Poor — consider rebalancing")
            st.markdown(f"""
            <div class="interp-box">
              <p style="color:#1e3a5f;font-size:.68rem;text-transform:uppercase;
                        letter-spacing:.1em;font-weight:700;margin:0 0 .8rem">Portfolio Interpretation</p>
              <div class="interp-row">{pi}&nbsp;
                Portfolio returned <b style="color:#f1f5f9">{pct(m['total'])}</b>
                vs SPY <b style="color:#334155">{pct(m['bt'])}</b>
                — <b style="color:{'#10b981' if out_>0 else '#ef4444'}">{ol} by {pct(abs(out_))}</b>
              </div>
              <div class="interp-row">{ri}&nbsp;
                Ann. volatility <b style="color:#f1f5f9">{av_*100:.1f}%</b>
                — {"below" if av_<.20 else "above"} the 20% equity benchmark
              </div>
              <div class="interp-row">{si}&nbsp;
                Sharpe ratio <b style="color:#f1f5f9">{sh_:.2f}</b>
                — {sl} risk-adjusted return
              </div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# ROUTER
# ════════════════════════════════════════════════════════════════
if st.session_state.view == "stock" and st.session_state.ticker:
    render_stock(st.session_state.ticker)
else:
    render_home()
