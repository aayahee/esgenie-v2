# app.py
# ESGenie 🧞 — Sustainable Portfolio Optimiser

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="ESGenie 🧞",
    page_icon="🧞",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

:root {
    --sage:       #4a7c59;
    --sage-light: #6a9e76;
    --sage-pale:  #c8dfc0;
    --sage-faint: #e8f2e4;
    --forest:     #2d5016;
    --text:       #0a0a0a;
    --white:      #ffffff;
    --amber:      #b87828;
    --red-soft:   #9e4444;
    --radius:     10px;
    --shadow:     0 1px 12px rgba(45,80,22,0.09);
}

/* ── Page ── */
.stApp {
    background-color: #edf4e8 !important;
    background-image:
        radial-gradient(ellipse at 8% 0%,   rgba(106,158,118,0.16) 0%, transparent 50%),
        radial-gradient(ellipse at 92% 100%, rgba(74,124,89,0.10)  0%, transparent 50%);
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

/* Hide sidebar entirely */
section[data-testid="stSidebar"] { display: none !important; }

/* ── Hero ── */
.hero-banner {
    background: linear-gradient(120deg, #e8f2e4 0%, #d4eacc 60%, #c8dfc0 100%);
    border: 1px solid var(--sage-pale);
    border-radius: 14px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    box-shadow: var(--shadow);
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.5rem;
    color: var(--forest);
    letter-spacing: -0.02em;
    margin: 0;
    line-height: 1.1;
}
.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.96rem;
    color: #111111;
    margin: 0.2rem 0 0;
    font-style: italic;
}
.hero-badge {
    background: var(--sage-pale);
    color: var(--forest);
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    display: inline-block;
    margin-top: 0.45rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Input expanders ── */
details[data-testid="stExpander"] {
    background: var(--white) !important;
    border: 1px solid var(--sage-pale) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow) !important;
    margin-bottom: 0.75rem !important;
    overflow: hidden !important;
}
details[data-testid="stExpander"] summary {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: #111111 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    padding: 0.9rem 1.1rem !important;
    background: #e8f2e4 !important;
    border-bottom: 1px solid #c8dfc0 !important;
}
details[data-testid="stExpander"] summary:hover {
    background: #daecd4 !important;
    color: #111111 !important;
}
details[data-testid="stExpander"] summary * { color: #111111 !important; }
details[data-testid="stExpander"] > div {
    background: #ffffff !important;
    padding: 1rem 1.25rem 1.25rem !important;
    color: #111111 !important;
}
details[data-testid="stExpander"] > div * { color: #111111 !important; }

/* ── Section label inside expanders ── */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    color: #444441;
    margin-bottom: 0.4rem;
    margin-top: 0.6rem;
}

/* ── Section header (results) ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--forest);
    border-left: 4px solid var(--sage);
    padding-left: 0.65rem;
    margin: 1.25rem 0 0.7rem;
}

/* ── Metric cards ── */
.metric-card {
    background: var(--white);
    border: 1px solid var(--sage-pale);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    text-align: center;
    box-shadow: var(--shadow);
    height: 100%;
}
.metric-card-label {
    font-size: 0.72rem;
    color: #444441;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 0.3rem;
}
.metric-card-value {
    font-family: 'DM Serif Display', serif;
    color: var(--forest);
    font-size: 1.45rem;
    line-height: 1.1;
}
.metric-card-delta {
    font-size: 0.75rem;
    color: var(--sage);
    margin-top: 0.25rem;
}

/* ── Reco box ── */
.reco-box {
    background: rgba(200,223,192,0.25);
    border: 1px solid var(--sage);
    border-left: 5px solid var(--sage);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 1.1rem 1.4rem;
    color: var(--forest);
    font-size: 0.93rem;
    line-height: 1.65;
}

/* ── ESG pills ── */
.esg-high { background:#d4edda; color:#155724; padding:2px 9px; border-radius:20px; font-size:0.78rem; font-weight:600; border:1px solid #c3e6cb; }
.esg-mid  { background:#fff3cd; color:#856404; padding:2px 9px; border-radius:20px; font-size:0.78rem; font-weight:600; border:1px solid #ffeeba; }
.esg-low  { background:#f8d7da; color:#721c24; padding:2px 9px; border-radius:20px; font-size:0.78rem; font-weight:600; border:1px solid #f5c6cb; }

/* ── Run button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #5a9068 0%, #3d6b45 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2rem !important;
    box-shadow: 0 3px 12px rgba(45,80,22,0.28) !important;
    transition: all 0.18s ease !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #6aa87a 0%, #4d7d55 100%) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:not([kind="primary"]) {
    background: var(--white) !important;
    border: 1px solid var(--sage-pale) !important;
    color: var(--forest) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid var(--sage-pale) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.87rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    color: #111111 !important;
    padding: 0.6rem 1.3rem !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    background: transparent !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--forest) !important;
    border-bottom-color: var(--sage) !important;
    font-weight: 600 !important;
}

/* ── Alerts ── */
[data-testid="stInfo"]    { background:rgba(200,223,192,0.28)!important; border-left:3px solid var(--sage)!important; }
[data-testid="stWarning"] { background:rgba(184,120,40,0.10)!important;  border-left:3px solid var(--amber)!important; }
[data-testid="stSuccess"] { background:rgba(74,124,89,0.10)!important;   border-left:3px solid var(--sage)!important; }
[data-testid="stError"]   { background:rgba(158,68,68,0.09)!important;   border-left:3px solid var(--red-soft)!important; }

/* ── Dataframes ── */
[data-testid="stDataFrame"] {
    background: var(--white) !important;
    border: 1px solid var(--sage-pale) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow) !important;
}

/* ── Charts ── */
[data-testid="stPyplotRootElement"] {
    background: var(--white) !important;
    border: 1px solid var(--sage-pale) !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem !important;
    box-shadow: var(--shadow) !important;
}

/* ── Download ── */
.stDownloadButton > button {
    background: var(--white) !important;
    border: 1px solid var(--sage-pale) !important;
    color: var(--forest) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}

hr { border:none!important; border-top:1px solid var(--sage-pale)!important; margin:1.25rem 0!important; }
.stCaption, [data-testid="stCaptionContainer"] { color:#444441!important; font-size:0.76rem!important; }
</style>
/* FIX TEXT VISIBILITY */
body, .stApp, p, span, div, label {
    color: #111111 !important;
}

.stCaption, [data-testid="stCaptionContainer"] {
    color: #333333 !important;
}

details[data-testid="stExpander"] summary,
details[data-testid="stExpander"] * {
    color: #111111 !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    color: #111111 !important;
}
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PURE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def classify_esg(score):
    if score >= 80:   return "High ESG",     f'<span class="esg-high">🟢 High ESG</span>'
    elif score >= 50: return "Moderate ESG", f'<span class="esg-mid">🟡 Moderate ESG</span>'
    else:             return "Low ESG",      f'<span class="esg-low">🔴 Low ESG</span>'

def compute_esg(E, S, G, w_e, w_s, w_g):
    return w_e * E + w_s * S + w_g * G

def portfolio_ret(w1, r1, r2):
    return w1 * r1 + (1 - w1) * r2

def portfolio_sd(w1, sd1, sd2, rho):
    var = (w1**2 * sd1**2
           + (1 - w1)**2 * sd2**2
           + 2 * rho * w1 * (1 - w1) * sd1 * sd2)
    return np.sqrt(np.maximum(var, 0.0))

def portfolio_esg(w1, esg1, esg2):
    return w1 * esg1 + (1 - w1) * esg2

def sharpe_ratio(w1, r1, r2, sd1, sd2, rho, r_free):
    ret = portfolio_ret(w1, r1, r2)
    sd  = portfolio_sd(w1, sd1, sd2, rho)
    if sd == 0: return 0.0
    return (ret - r_free) / sd

def utility(w1, r1, r2, sd1, sd2, rho, r_free,
            gamma, theta, esg1, esg2,
            sin_choice, excluded, name1, name2,
            apply_threshold, threshold, penalty_strength):
    """
    ESG-adjusted mean-variance utility (Lecture 6):
      U = (E[r_p] - r_f) - (γ/2)·σ²_p + θ·(ESG_p/100)
    Plus linear shortfall penalty and hard sin stock exclusion.
    """
    ret = portfolio_ret(w1, r1, r2)
    sd  = portfolio_sd(w1, sd1, sd2, rho)
    esg = portfolio_esg(w1, esg1, esg2)
    base = (ret - r_free) - (gamma / 2) * sd**2 + theta * (esg / 100)
    excl = 0.0
    if sin_choice == 1:
        if name1 in excluded and w1 > 0:  excl -= 1e6 * w1
        if name2 in excluded and w1 < 1:  excl -= 1e6 * (1 - w1)
    thr = 0.0
    if apply_threshold and esg < threshold:
        thr = -penalty_strength * ((threshold - esg) / 100) ** 2
    return base + excl + thr

def run_optimisation(r1, r2, sd1, sd2, rho, r_free,
                     gamma, theta, esg1, esg2,
                     sin_choice, excluded, name1, name2,
                     apply_threshold, threshold, penalty_strength, n=1000):
    weights = np.linspace(0, 1, n)
    utils   = np.array([utility(w, r1, r2, sd1, sd2, rho, r_free, gamma, theta,
                                esg1, esg2, sin_choice, excluded, name1, name2,
                                apply_threshold, threshold, penalty_strength)
                        for w in weights])
    sharpes = np.array([sharpe_ratio(w, r1, r2, sd1, sd2, rho, r_free) for w in weights])
    rets    = np.array([portfolio_ret(w, r1, r2)       for w in weights])
    risks   = np.array([portfolio_sd(w, sd1, sd2, rho) for w in weights])
    esgs    = np.array([portfolio_esg(w, esg1, esg2)   for w in weights])
    oi, ti, mi = np.argmax(utils), np.argmax(sharpes), np.argmin(risks)
    return dict(
        weights=weights, utils=utils, sharpes=sharpes,
        rets=rets, risks=risks, esgs=esgs,
        w1_optimal  =weights[oi], ret_optimal  =rets[oi],
        sd_optimal  =risks[oi],   esg_optimal  =esgs[oi],  sr_optimal  =sharpes[oi],
        w1_tangency =weights[ti], ret_tangency =rets[ti],
        sd_tangency =risks[ti],   esg_tangency =esgs[ti],  sr_tangency =sharpes[ti],
        w1_min_var  =weights[mi], ret_min_var  =rets[mi],
        sd_min_var  =risks[mi],   esg_min_var  =esgs[mi],  sr_min_var  =sharpes[mi],
    )

@st.cache_data(show_spinner=False)
def cached_sensitivity(r1, r2, sd1, sd2, rho, r_free,
                       gamma, theta, esg1, esg2,
                       sin_choice, excluded_tuple, name1, name2,
                       apply_threshold, threshold, penalty_strength):
    excluded = dict(excluded_tuple)
    weights  = np.linspace(0, 1, 500)

    theta_range = np.linspace(0, 4, 60)
    gamma_range = np.linspace(1, 15, 60)
    theta_grid  = np.linspace(0, 4, 12)
    gamma_grid  = np.linspace(1, 15, 12)

    def opt(t, g):
        res = run_optimisation(r1, r2, sd1, sd2, rho, r_free, g, t,
                               esg1, esg2, sin_choice, excluded, name1, name2,
                               apply_threshold, threshold, penalty_strength, n=500)
        return res["w1_optimal"]

    sa_w, sa_esg, sa_sr = [], [], []
    for t in theta_range:
        w = opt(t, gamma)
        sa_w.append(w * 100)
        sa_esg.append(portfolio_esg(w, esg1, esg2))
        sa_sr.append(sharpe_ratio(w, r1, r2, sd1, sd2, rho, r_free))

    sg_sr = []
    for g in gamma_range:
        w = opt(theta, g)
        sg_sr.append(sharpe_ratio(w, r1, r2, sd1, sd2, rho, r_free))

    heatmap = np.zeros((len(gamma_grid), len(theta_grid)))
    for i, g in enumerate(gamma_grid):
        for j, t in enumerate(theta_grid):
            heatmap[i, j] = portfolio_esg(opt(t, g), esg1, esg2)

    return (theta_range, gamma_range, theta_grid, gamma_grid,
            np.array(sa_w), np.array(sa_esg), np.array(sa_sr),
            np.array(sg_sr), heatmap)


# ══════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════
PRESETS = {
    "🌿 Eco-First":          dict(r1=8,  sd1=22, r2=4,  sd2=10, rho=0.15, rfree=2.0, risk=0, theta=3.8, focus=0, thr=60,  use_thr=True),
    "⚖️ Balanced":           dict(r1=8,  sd1=20, r2=4,  sd2=10, rho=0.20, rfree=2.0, risk=1, theta=2.0, focus=3, thr=0,   use_thr=False),
    "🛡️ Conservative Green": dict(r1=6,  sd1=14, r2=3,  sd2=7,  rho=0.10, rfree=2.0, risk=0, theta=2.5, focus=3, thr=50,  use_thr=True),
    "🚀 Growth Hunter":      dict(r1=14, sd1=30, r2=5,  sd2=12, rho=0.25, rfree=2.0, risk=2, theta=0.5, focus=3, thr=0,   use_thr=False),
    "🤝 Social Impact":      dict(r1=7,  sd1=18, r2=4,  sd2=9,  rho=0.18, rfree=2.0, risk=1, theta=3.0, focus=1, thr=55,  use_thr=True),
}
PILLAR_OPTIONS = [
    "🌍 Environmental focus  (E=0.60, S=0.20, G=0.20)",
    "🤝 Social focus         (E=0.20, S=0.60, G=0.20)",
    "🏛️ Governance focus     (E=0.20, S=0.20, G=0.60)",
    "⚖️ Balanced ESG         (E=0.34, S=0.33, G=0.33)",
]
PILLAR_WEIGHTS = {
    0: (0.60, 0.20, 0.20, "Environmental focus"),
    1: (0.20, 0.60, 0.20, "Social focus"),
    2: (0.20, 0.20, 0.60, "Governance focus"),
    3: (0.34, 0.33, 0.33, "Balanced ESG"),
}
RISK_MAP    = {0: (10, "Conservative"), 1: (5, "Balanced"), 2: (2, "Aggressive")}
SIN_SECTORS = {"Tobacco", "Weapons & Defence", "Gambling", "Fossil Fuels"}
SECTORS     = ["Technology", "Healthcare", "Financial Services", "Consumer Goods",
               "Energy", "Fossil Fuels", "Tobacco", "Weapons & Defence", "Gambling", "Other"]

if "preset" not in st.session_state:
    st.session_state.preset = None


# ══════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
  <div style="font-size:3rem;line-height:1;">🧞</div>
  <div>
    <p class="hero-title">ESGenie</p>
    <p class="hero-subtitle">Your personalised sustainable investment portfolio advisor</p>
    <span class="hero-badge">🌿 Sustainable Finance · ESG Optimisation · Retail Investing</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# QUICK-START PRESETS + EXAMPLE LOADER
# ══════════════════════════════════════════════════════════════════════
st.markdown("#### ⚡ Quick-Start — choose an investor profile or load an example")
st.caption("Select a preset to auto-fill all inputs, or load the Apple vs BP worked example.")

preset_cols = st.columns(len(PRESETS) + 1)
for col, pname in zip(preset_cols, PRESETS):
    with col:
        if st.button(pname, key=f"pre_{pname}", use_container_width=True):
            st.session_state.preset = pname
            st.rerun()

with preset_cols[-1]:
    if st.button("📋 Apple vs BP", use_container_width=True):
        st.session_state.update(dict(
            _name1="Apple", _name2="BP",
            _r1=12.0, _r2=6.0, _sd1=18.0, _sd2=22.0, _rho=-0.1, _rfree=4.5,
            _E1=78.0, _S1=72.0, _G1=81.0,
            _E2=32.0, _S2=41.0, _G2=55.0,
            _risk=0, _theta=2.5, _focus=0,
            _use_thr=True, _thr=50.0,
        ))
        st.session_state.preset = None
        st.rerun()

p = PRESETS.get(st.session_state.preset, {})

st.markdown("---")


# ══════════════════════════════════════════════════════════════════════
# INPUT SECTIONS — numbered expanders
# ══════════════════════════════════════════════════════════════════════
st.markdown("#### Configure your portfolio parameters")
st.caption("Expand each section, fill in your inputs, then click Run Optimisation.")

# ── 01 Financial Data ─────────────────────────────────────────────────
with st.expander("01  —  Financial Data", expanded=True):
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown('<p class="section-label">Asset 1</p>', unsafe_allow_html=True)
        name1 = st.text_input("Name", value=st.session_state.get("_name1", "Asset 1"), key="n1")
        r1    = st.number_input("Expected Return (%)", -50.0, 50.0,
                                float(p.get("r1",  st.session_state.get("_r1",  8.0))),  step=0.5) / 100
        sd1   = st.number_input("Standard Deviation (%)", 0.0, 100.0,
                                float(p.get("sd1", st.session_state.get("_sd1", 20.0))), step=0.5) / 100
    with col_b:
        st.markdown('<p class="section-label">Asset 2</p>', unsafe_allow_html=True)
        name2 = st.text_input("Name", value=st.session_state.get("_name2", "Asset 2"), key="n2")
        r2    = st.number_input("Expected Return (%)", -50.0, 50.0,
                                float(p.get("r2",  st.session_state.get("_r2",  4.0))),  step=0.5, key="r2i") / 100
        sd2   = st.number_input("Standard Deviation (%)", 0.0, 100.0,
                                float(p.get("sd2", st.session_state.get("_sd2", 10.0))), step=0.5, key="sd2i") / 100

    col_c, col_d = st.columns(2, gap="large")
    with col_c:
        st.markdown('<p class="section-label">Correlation</p>', unsafe_allow_html=True)
        rho = st.slider("ρ between assets", -1.0, 1.0,
                        float(p.get("rho", st.session_state.get("_rho", 0.2))), step=0.05)
    with col_d:
        st.markdown('<p class="section-label">Risk-Free Rate</p>', unsafe_allow_html=True)
        r_free = st.number_input("Risk-Free Rate (%)", 0.0, 15.0,
                                 float(p.get("rfree", st.session_state.get("_rfree", 2.0))),
                                 step=0.25) / 100

# ── 02 Risk Profile ───────────────────────────────────────────────────
with st.expander("02  —  Risk Profile", expanded=False):
    risk_idx = st.radio(
        "Your attitude to investment risk:",
        [0, 1, 2],
        format_func=lambda x: ["🛡️ Conservative — prioritise capital protection",
                                "⚖️ Balanced — moderate risk for moderate returns",
                                "🚀 Aggressive — comfortable with high risk"][x],
        index=int(p.get("risk", st.session_state.get("_risk", 1))),
        horizontal=True,
    )
    gamma, risk_label = RISK_MAP[risk_idx]
    st.caption(f"Risk aversion coefficient γ = {gamma}  ·  Used in utility: U = (E[r] - r_f) - (γ/2)·σ²  + θ·ESG")

# ── 03 ESG Preferences ────────────────────────────────────────────────
with st.expander("03  —  ESG Preferences", expanded=False):
    col_e, col_f = st.columns(2, gap="large")
    with col_e:
        st.markdown('<p class="section-label">ESG Weight in Utility (θ)</p>', unsafe_allow_html=True)
        theta = st.slider("0 = financial only  ·  4 = ESG first",
                          0.0, 4.0, float(p.get("theta", st.session_state.get("_theta", 2.0))), step=0.1)
        st.caption(
            "Utility function: U = (E[rₚ] - r_f) - (γ/2)σ²ₚ + θ·(ESGₚ/100)"
        )
    with col_f:
        st.markdown('<p class="section-label">ESG Pillar Focus</p>', unsafe_allow_html=True)
        focus_idx = st.radio(
            "Select ESG pillar weighting:",
            [0, 1, 2, 3],
            format_func=lambda x: PILLAR_OPTIONS[x],
            index=int(p.get("focus", st.session_state.get("_focus", 3))),
        )
    w_e, w_s, w_g, esg_focus_label = PILLAR_WEIGHTS[focus_idx]

# ── 04 Asset ESG Scores ───────────────────────────────────────────────
with st.expander("04  —  Asset ESG Scores", expanded=False):
    st.caption("Rate each asset from 0 (worst) to 100 (best) across the three ESG pillars.")
    col_g, col_h = st.columns(2, gap="large")
    with col_g:
        st.markdown(f'<p class="section-label">{name1}</p>', unsafe_allow_html=True)
        sector1 = st.selectbox("Sector", SECTORS, key="sec1")
        E1 = st.slider("Environmental (E)", 0, 100, int(st.session_state.get("_E1", 60)), key="e1")
        S1 = st.slider("Social (S)",        0, 100, int(st.session_state.get("_S1", 60)), key="s1")
        G1 = st.slider("Governance (G)",    0, 100, int(st.session_state.get("_G1", 60)), key="g1")
    with col_h:
        st.markdown(f'<p class="section-label">{name2}</p>', unsafe_allow_html=True)
        sector2 = st.selectbox("Sector", SECTORS, key="sec2")
        E2 = st.slider("Environmental (E)", 0, 100, int(st.session_state.get("_E2", 40)), key="e2")
        S2 = st.slider("Social (S)",        0, 100, int(st.session_state.get("_S2", 40)), key="s2")
        G2 = st.slider("Governance (G)",    0, 100, int(st.session_state.get("_G2", 40)), key="g2")

# ── 05 Ethical Screening ──────────────────────────────────────────────
with st.expander("05  —  Ethical Screening", expanded=False):
    excluded = {}
    for aname, sector in [(name1, sector1), (name2, sector2)]:
        if sector in SIN_SECTORS:
            excluded[aname] = sector

    if excluded:
        st.warning(f"⚠️ Restricted sector detected: {', '.join(excluded.values())}")
        sin_choice = st.radio(
            "How to handle restricted sectors?",
            [1, 2, 3],
            format_func=lambda x: {1: "❌ Exclude entirely (weight = 0%)",
                                    2: "⚠️ Apply utility penalty",
                                    3: "✅ Proceed without restriction"}[x],
        )
    else:
        st.success("✅ No restricted sectors detected.")
        sin_choice = 3

    st.markdown('<p class="section-label">Minimum ESG Threshold</p>', unsafe_allow_html=True)
    use_thr = st.checkbox(
        "Set a minimum portfolio ESG score threshold",
        value=bool(p.get("use_thr", st.session_state.get("_use_thr", False)))
    )
    if use_thr:
        threshold = st.slider("Minimum ESG score", 0.0, 100.0,
                              float(p.get("thr", st.session_state.get("_thr", 50.0))), step=1.0)
    else:
        threshold = 0.0

    apply_threshold  = use_thr and threshold > 0
    penalty_strength = 0.01 * theta

# ── Run button ─────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
col_run, _ = st.columns([1, 3])
with col_run:
    run = st.button("✨ Run Optimisation", type="primary", use_container_width=True)


# ══════════════════════════════════════════════════════════════════════
# LANDING STATE
# ══════════════════════════════════════════════════════════════════════
if not run:
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(74,124,89,0.08) 0%,rgba(200,223,192,0.18) 100%);
                border:1px solid rgba(74,124,89,0.22); border-radius:12px;
                padding:1.8rem 2.2rem; margin-top:0.5rem;">
      <p style="font-family:'DM Serif Display',serif; font-size:1.15rem; color:#2d5016;
                margin:0 0 0.4rem; font-style:italic;">How to use ESGenie</p>
      <p style="color:#111111; font-size:0.92rem; margin:0; line-height:1.7;">
        Complete the five input sections above, then click
        <strong style="color:#2d5016;">✨ Run Optimisation</strong> to generate your
        personalised sustainable portfolio. Results appear across three tabs —
        <em>Portfolio Results</em>, <em>Charts</em>, and <em>Sensitivity Analysis</em>.
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════
# GUARDS
# ══════════════════════════════════════════════════════════════════════
if sin_choice == 1 and len(excluded) == 2:
    st.error("❌ Both assets are in restricted sectors. No valid portfolio can be constructed.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════
# COMPUTE
# ══════════════════════════════════════════════════════════════════════
esg1 = compute_esg(E1, S1, G1, w_e, w_s, w_g)
esg2 = compute_esg(E2, S2, G2, w_e, w_s, w_g)

with st.spinner("🧞 ESGenie is working its magic..."):
    res = run_optimisation(
        r1, r2, sd1, sd2, rho, r_free,
        gamma, theta, esg1, esg2,
        sin_choice, excluded, name1, name2,
        apply_threshold, threshold, penalty_strength,
    )

w1_opt = res["w1_optimal"];  w2_opt = 1 - w1_opt
w1_tan = res["w1_tangency"]; w2_tan = 1 - w1_tan
w1_mv  = res["w1_min_var"];  w2_mv  = 1 - w1_mv
esg_premium = res["sr_tangency"] - res["sr_optimal"]

if theta <= 1:     esg_importance_label = "Low ESG preference"
elif theta <= 2.5: esg_importance_label = "Moderate ESG preference"
else:              esg_importance_label = "High ESG preference"

dominant = name1 if w1_opt >= w2_opt else name2
dom_esg  = esg1  if w1_opt >= w2_opt else esg2
sec_esg  = esg2  if w1_opt >= w2_opt else esg1

if theta > 3:     identity = ("🌱 Impact Investor",       "identity-impact")
elif theta > 1.5: identity = ("⚖️ Balanced ESG Investor", "identity-balanced")
else:             identity = ("💰 Return-Focused Investor","identity-financial")


# ══════════════════════════════════════════════════════════════════════
# INVESTOR PROFILE STRIP
# ══════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown('<div class="section-header">👤 Investor Profile</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
for col, label, value, delta in [
    (c1, "Risk Profile",   risk_label,           f"γ = {gamma}"),
    (c2, "ESG Importance", esg_importance_label, f"θ = {theta}"),
    (c3, "ESG Focus",      esg_focus_label,      ""),
    (c4, "Threshold",      f"{threshold:.0f}" if apply_threshold else "None", "min ESG score"),
    (c5, "Identity",       identity[0],          ""),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-card-label">{label}</div>
          <div class="metric-card-value" style="font-size:1.05rem;">{value}</div>
          <div class="metric-card-delta">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# ESG SCORE SUMMARY
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🌱 ESG Score Summary</div>', unsafe_allow_html=True)

ca, cb = st.columns(2)
for col, aname, sector, esg_score, E, S, G in [
    (ca, name1, sector1, esg1, E1, S1, G1),
    (cb, name2, sector2, esg2, E2, S2, G2),
]:
    _, pill = classify_esg(esg_score)
    with col:
        st.markdown(f"""
        <div class="metric-card" style="text-align:left; padding:1.1rem 1.4rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <span style="font-weight:700; color:var(--forest); font-size:1rem;">{aname}</span>
            {pill}
          </div>
          <div style="font-size:0.78rem; color:#5a6e55; margin-bottom:0.5rem;">{sector}</div>
          <div style="font-size:1.6rem; font-family:'DM Serif Display',serif; color:var(--forest);">
            {esg_score:.1f}<span style="font-size:0.85rem; color:#5a6e55;"> / 100</span>
          </div>
          <div style="font-size:0.78rem; color:#5a6e55; margin-top:0.4rem;">
            🌿 E={E} × {w_e:.2f} &nbsp;+&nbsp; 🤝 S={S} × {w_s:.2f} &nbsp;+&nbsp; 🏛️ G={G} × {w_g:.2f}
          </div>
        </div>
        """, unsafe_allow_html=True)

if apply_threshold:
    if esg1 < threshold: st.warning(f"⚠️ {name1} ESG ({esg1:.1f}) is below your threshold of {threshold:.0f}.")
    if esg2 < threshold: st.warning(f"⚠️ {name2} ESG ({esg2:.1f}) is below your threshold of {threshold:.0f}.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")


# ══════════════════════════════════════════════════════════════════════
# THREE RESULT TABS
# ══════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["📊 Portfolio Results", "📈 Charts", "🔬 Sensitivity Analysis"])


# ─────────────────────────────────────────────────────────────────────
# TAB 1 — Portfolio Results
# ─────────────────────────────────────────────────────────────────────
with tab1:

    st.markdown('<div class="section-header">📐 Recommended Portfolio</div>', unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    for col, label, value, delta in [
        (m1, "Expected Return",  f"{res['ret_optimal']*100:.2f}%",  "annualised"),
        (m2, "Risk (Std Dev)",   f"{res['sd_optimal']*100:.2f}%",   "annualised"),
        (m3, "Sharpe Ratio",     f"{res['sr_optimal']:.3f}",        "risk-adjusted"),
        (m4, "ESG Score",        f"{res['esg_optimal']:.1f} / 100", classify_esg(res['esg_optimal'])[0]),
        (m5, "ESG Premium",      f"{esg_premium:+.3f}",             "vs tangency Sharpe"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-card-label">{label}</div>
              <div class="metric-card-value">{value}</div>
              <div class="metric-card-delta">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Asset allocation table
    st.markdown('<div class="section-header">💼 Asset Allocation</div>', unsafe_allow_html=True)
    _, p1 = classify_esg(esg1)
    _, p2 = classify_esg(esg2)
    _, pp = classify_esg(res["esg_optimal"])
    st.markdown(f"""
    <table style="width:100%;border-collapse:collapse;font-size:0.9rem;
                  background:white;border-radius:10px;overflow:hidden;box-shadow:var(--shadow);">
      <thead><tr style="background:#e8f2e4;">
        <th style="text-align:left;padding:10px 14px;color:var(--forest);">Asset</th>
        <th style="text-align:right;padding:10px 14px;color:var(--forest);">Weight</th>
        <th style="text-align:right;padding:10px 14px;color:var(--forest);">ESG Score</th>
        <th style="text-align:center;padding:10px 14px;color:var(--forest);">ESG Class</th>
      </tr></thead>
      <tbody>
        <tr>
          <td style="padding:9px 14px;">{name1}</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;">{w1_opt*100:.1f}%</td>
          <td style="text-align:right;padding:9px 14px;">{esg1:.1f}</td>
          <td style="text-align:center;padding:9px 14px;">{p1}</td>
        </tr>
        <tr style="background:#f9faf8;">
          <td style="padding:9px 14px;">{name2}</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;">{w2_opt*100:.1f}%</td>
          <td style="text-align:right;padding:9px 14px;">{esg2:.1f}</td>
          <td style="text-align:center;padding:9px 14px;">{p2}</td>
        </tr>
        <tr style="border-top:2px solid var(--sage-pale);">
          <td style="padding:9px 14px;font-weight:700;">Portfolio (weighted)</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;">100.0%</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;">{res['esg_optimal']:.1f}</td>
          <td style="text-align:center;padding:9px 14px;">{pp}</td>
        </tr>
      </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Three-portfolio comparison
    st.markdown('<div class="section-header">📋 Portfolio Comparison</div>', unsafe_allow_html=True)
    st.caption("How your ESG-optimal recommendation compares to purely financial alternatives.")
    chars_df = pd.DataFrame({
        "Metric": ["Expected Return","Risk (Std Dev)","Sharpe Ratio","ESG Score","ESG Class"],
        f"🟢 Recommended ({w1_opt*100:.0f}% {name1})": [
            f"{res['ret_optimal']*100:.2f}%",  f"{res['sd_optimal']*100:.2f}%",
            f"{res['sr_optimal']:.3f}",         f"{res['esg_optimal']:.1f}",
            classify_esg(res['esg_optimal'])[0]],
        f"📐 Tangency ({w1_tan*100:.0f}% {name1})": [
            f"{res['ret_tangency']*100:.2f}%",  f"{res['sd_tangency']*100:.2f}%",
            f"{res['sr_tangency']:.3f}",         f"{res['esg_tangency']:.1f}",
            classify_esg(res['esg_tangency'])[0]],
        f"🛡️ Min Variance ({w1_mv*100:.0f}% {name1})": [
            f"{res['ret_min_var']*100:.2f}%",   f"{res['sd_min_var']*100:.2f}%",
            f"{res['sr_min_var']:.3f}",          f"{res['esg_min_var']:.1f}",
            classify_esg(res['esg_min_var'])[0]],
    })
    st.dataframe(chars_df, use_container_width=True, hide_index=True)

    if esg_premium > 0:
        st.warning(f"📉 **ESG Premium: {esg_premium:+.3f} Sharpe points** — your ESG preferences reduce risk-adjusted return relative to the purely financial tangency portfolio.")
    else:
        st.success(f"📈 **ESG Premium: {esg_premium:+.3f} Sharpe points** — your ESG preferences align with financial performance. No sacrifice detected.")
    st.markdown("#### 📉 ESG Trade-off Insight")

    if esg_premium > 0:
        st.warning(
            f"Increasing ESG preference reduces risk-adjusted return by {esg_premium:.3f} Sharpe points "
            f"relative to the purely financial portfolio."
        )
    else:
        st.success(
            f"No trade-off detected: ESG preferences align with financial performance."
        )
    # Recommendation narrative
    st.markdown('<div class="section-header">💬 Why This Portfolio?</div>', unsafe_allow_html=True)
    driver = (
        f"The tilt toward <strong>{dominant}</strong> is partly driven by its stronger ESG score "
        f"({dom_esg:.1f} vs {sec_esg:.1f}), consistent with your {esg_focus_label.lower()} and θ={theta}."
        if dom_esg > sec_esg else
        f"The tilt toward <strong>{dominant}</strong> is driven primarily by its superior "
        f"risk-return profile rather than ESG performance."
    )
    st.markdown(f"""
    <div class="reco-box">
    Based on your <strong>{risk_label.lower()} risk profile</strong> (γ={gamma}) and
    <strong>{esg_importance_label.lower()}</strong> (θ={theta}), ESGenie recommends allocating
    <strong>{w1_opt*100:.1f}% to {name1}</strong> and
    <strong>{w2_opt*100:.1f}% to {name2}</strong>.<br><br>{driver}
    </div>
    """, unsafe_allow_html=True)

    if apply_threshold and (esg1 < threshold or esg2 < threshold):
        st.warning(f"One or more assets fell below your minimum ESG threshold of {threshold:.0f}. A utility penalty was applied.")
    if sin_choice == 1 and excluded:
        for aname, sec in excluded.items():
            st.error(f"**{aname}** ({sec}) was excluded per your ethical screening preferences.")

    # Download
    st.markdown("<br>", unsafe_allow_html=True)
    summary_txt = (
        f"ESGenie 🧞 — Portfolio Summary\n{'='*40}\n"
        f"Risk Profile:    {risk_label}  (γ={gamma})\n"
        f"ESG Importance:  θ={theta}  ({esg_importance_label})\n"
        f"ESG Focus:       {esg_focus_label}\n"
        f"Investor Type:   {identity[0]}\n\n"
        f"Recommended Allocation\n{'-'*40}\n"
        f"  {name1}: {w1_opt*100:.1f}%\n"
        f"  {name2}: {w2_opt*100:.1f}%\n\n"
        f"Portfolio Metrics\n{'-'*40}\n"
        f"  Expected Return : {res['ret_optimal']*100:.2f}%\n"
        f"  Risk (Std Dev)  : {res['sd_optimal']*100:.2f}%\n"
        f"  Sharpe Ratio    : {res['sr_optimal']:.3f}\n"
        f"  ESG Score       : {res['esg_optimal']:.1f} / 100  ({classify_esg(res['esg_optimal'])[0]})\n"
        f"  ESG Premium     : {esg_premium:+.3f} vs tangency Sharpe\n"
    )
    st.download_button(
        label="⬇️ Download Portfolio Summary",
        data=summary_txt,
        file_name="esgenie_summary.txt",
        mime="text/plain",
    )


# ─────────────────────────────────────────────────────────────────────
# TAB 2 — Charts
# ─────────────────────────────────────────────────────────────────────
with tab2:

    weights_plot = res["weights"]
    ret_plot     = res["rets"]
    risk_plot    = res["risks"]
    esg_plot     = res["esgs"]
    util_plot    = res["utils"]

    # Plotly interactive frontier
    st.markdown('<div class="section-header">📈 ESG-Efficient Frontier</div>', unsafe_allow_html=True)
    fig_f = go.Figure()
    fig_f.add_trace(go.Scatter(
        x=risk_plot * 100, y=ret_plot * 100, mode="markers",
        marker=dict(color=esg_plot, colorscale="RdYlGn", cmin=0, cmax=100,
                    size=5, opacity=0.85,
                    colorbar=dict(title="ESG Score", thickness=14,
                                  tickfont=dict(color="#2d5016"),
                                  titlefont=dict(color="#2d5016"))),
        text=[f"{name1}: {w*100:.1f}%<br>Return: {r*100:.2f}%<br>Risk: {s*100:.2f}%<br>ESG: {e:.1f}"
              for w, r, s, e in zip(weights_plot, ret_plot, risk_plot, esg_plot)],
        hoverinfo="text", showlegend=False,
    ))
    cml_x = np.linspace(0, max(risk_plot) * 1.2, 100)
    cml_s = (res["ret_tangency"] - r_free) / res["sd_tangency"] if res["sd_tangency"] > 0 else 0
    fig_f.add_trace(go.Scatter(
        x=cml_x * 100, y=(r_free + cml_s * cml_x) * 100,
        mode="lines", line=dict(dash="dash", color="#4a7c59", width=1.5),
        name="Capital Market Line",
    ))
    for sx, ry, label, colour, sym, sz, w in [
        (0,                  r_free,              f"Risk-Free ({r_free*100:.1f}%)", "#4a7c59", "diamond",     10, None),
        (res["sd_min_var"],  res["ret_min_var"],   "Min Variance",                  "#7b5ea7", "square",      12, w1_mv),
        (res["sd_tangency"], res["ret_tangency"],  "Tangency",                      "#2979aa", "triangle-up", 14, w1_tan),
        (res["sd_optimal"],  res["ret_optimal"],   "✨ Recommended",                "#2d5016", "star",        20, w1_opt),
    ]:
        hover = (f"{label}<br>{name1}: {w*100:.1f}% | {name2}: {(1-w)*100:.1f}%<br>"
                 f"Return: {ry*100:.2f}% | Risk: {sx*100:.2f}%" if w is not None else label)
        fig_f.add_trace(go.Scatter(
            x=[sx * 100], y=[ry * 100], mode="markers+text",
            marker=dict(symbol=sym, color=colour, size=sz, line=dict(color="white", width=1.5)),
            text=[label], textposition="top right",
            textfont=dict(color=colour, size=9),
            hovertext=[hover], hoverinfo="text", name=label,
        ))
    fig_f.update_layout(
        xaxis_title="Risk — Standard Deviation (%)",
        yaxis_title="Expected Return (%)",
        height=430,
        paper_bgcolor="#ffffff", plot_bgcolor="#f9faf8",
        font=dict(family="DM Sans", color="#2d5016"),
        margin=dict(l=50, r=20, t=20, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.38,
                    xanchor="left", x=0,
                    bgcolor="rgba(255,255,255,0.85)",
                    bordercolor="#c8dfc0", borderwidth=1),
        xaxis=dict(gridcolor="#e8f2e4", zerolinecolor="#c8dfc0"),
        yaxis=dict(gridcolor="#e8f2e4", zerolinecolor="#c8dfc0"),
    )
    st.plotly_chart(fig_f, use_container_width=True)

    # Utility vs weight
    st.markdown('<div class="section-header">📉 Utility Function vs Portfolio Weight</div>',
                unsafe_allow_html=True)
    fig_u, ax = plt.subplots(figsize=(10, 4))
    fig_u.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f9faf8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#c8dfc0"); spine.set_linewidth(0.8)
    if np.all(util_plot == util_plot[0]):
        st.warning("Utility function is flat — check inputs.")
    ax.plot(weights_plot * 100, util_plot, color="#4a7c59", linewidth=2.5, label="Utility U(w)")
    ax.fill_between(weights_plot * 100, util_plot, alpha=0.07, color="#4a7c59")
    ax.axvline(x=w1_opt * 100, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8)
    ax.scatter(w1_opt * 100, res["utils"][np.argmax(res["utils"])],
               marker="*", color="#2d5016", s=250, zorder=5,
               label=f"✨ Optimal: {w1_opt*100:.1f}%")
    ax.axvline(x=w1_tan * 100, color="#6a9e76", linestyle=":", linewidth=1.5, alpha=0.8,
               label=f"Tangency: {w1_tan*100:.1f}%")
    ax.set_xlabel(f"Weight in {name1} (%)", color="#5a6e55")
    ax.set_ylabel("Utility", color="#5a6e55")
    ax.set_title("Utility Function vs Portfolio Weight", color="#2d5016", fontweight="bold")
    ax.tick_params(colors="#5a6e55")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25, color="#c8dfc0")
    fig_u.tight_layout()
    st.pyplot(fig_u)
    plt.close(fig_u)


# ─────────────────────────────────────────────────────────────────────
# TAB 3 — Sensitivity Analysis (cached)
# ─────────────────────────────────────────────────────────────────────
with tab3:

    st.markdown('<div class="section-header">🔬 Sensitivity Analysis</div>', unsafe_allow_html=True)
    st.caption("How would your recommendation change under different preferences? Cached — no recomputing unless inputs change.")
    st.caption(
        "Higher θ increases ESG focus, while higher γ reduces risk exposure. "
        "This shows how investor preferences shape optimal portfolio allocation."
    )
    with st.spinner("🧞 Computing sensitivity across parameter space..."):
        (theta_range, gamma_range, theta_grid, gamma_grid,
         sa_w, sa_esg, sa_sr, sg_sr, heatmap) = cached_sensitivity(
            r1, r2, sd1, sd2, rho, r_free,
            gamma, theta, esg1, esg2,
            sin_choice, tuple(excluded.items()), name1, name2,
            apply_threshold, threshold, penalty_strength,
        )

    # Table
    st.markdown(f'<div class="section-header">📋 θ Sensitivity Table  (γ fixed at {gamma})</div>',
                unsafe_allow_html=True)
    rows = []
    for idx in np.linspace(0, len(theta_range) - 1, 9, dtype=int):
        t_val = theta_range[idx]
        rows.append({
            "θ":                    f"{t_val:.2f}" + (" ← your θ" if abs(t_val - theta) < 0.25 else ""),
            f"Weight in {name1}":   f"{sa_w[idx]:.1f}%",
            "Portfolio ESG":        f"{sa_esg[idx]:.1f}",
            "ESG Class":            classify_esg(sa_esg[idx])[0],
            "Sharpe":               f"{sa_sr[idx]:.3f}",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # 2×2 plots
    fig_sa, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig_sa.patch.set_facecolor("#ffffff")
    for row in axes:
        for ax in row:
            ax.set_facecolor("#f9faf8")
            for spine in ax.spines.values():
                spine.set_edgecolor("#c8dfc0"); spine.set_linewidth(0.8)
            ax.tick_params(colors="#5a6e55")
    fig_sa.suptitle("ESGenie — Sensitivity Analysis", fontsize=13,
                    fontweight="bold", color="#2d5016")

    ax = axes[0, 0]
    ax.plot(theta_range, sa_w, color="#4a7c59", linewidth=2.5)
    ax.fill_between(theta_range, sa_w, alpha=0.07, color="#4a7c59")
    ax.axvline(x=theta, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8,
               label=f"Your θ = {theta}")
    ax.axhline(y=sa_w[np.argmin(np.abs(theta_range - theta))],
               color="#c8dfc0", linestyle=":", linewidth=1, alpha=0.8)
    ax.set_xlabel("ESG Preference (θ)", color="#5a6e55")
    ax.set_ylabel(f"Weight in {name1} (%)", color="#5a6e55")
    ax.set_title(f"Allocation vs ESG Preference  (γ = {gamma})", color="#2d5016", fontweight="bold")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.2, color="#c8dfc0"); ax.set_xlim(0, 4)

    ax = axes[0, 1]
    ax.plot(theta_range, sa_esg, color="#6a9e76", linewidth=2.5)
    ax.fill_between(theta_range, sa_esg, alpha=0.07, color="#6a9e76")
    ax.axvline(x=theta, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8,
               label=f"Your θ = {theta}")
    ax.axhspan(80, 100, alpha=0.07, color="green",  label="High ESG (≥80)")
    ax.axhspan(50,  80, alpha=0.07, color="yellow", label="Moderate ESG (50–80)")
    ax.axhspan(0,   50, alpha=0.07, color="red",    label="Low ESG (<50)")
    ax.set_xlabel("ESG Preference (θ)", color="#5a6e55")
    ax.set_ylabel("Portfolio ESG Score", color="#5a6e55")
    ax.set_title(f"ESG Score vs ESG Preference  (γ = {gamma})", color="#2d5016", fontweight="bold")
    ax.legend(fontsize=7); ax.grid(True, alpha=0.2, color="#c8dfc0")
    ax.set_xlim(0, 4); ax.set_ylim(0, 100)

    ax = axes[1, 0]
    ax.plot(gamma_range, sg_sr, color="#4a7c59", linewidth=2.5, label="Sharpe ratio")
    ax.fill_between(gamma_range, sg_sr, alpha=0.07, color="#4a7c59")
    ax.axvline(x=gamma, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8,
               label=f"Your γ = {gamma}")
    ax.set_xlabel("Risk Aversion (γ)", color="#5a6e55")
    ax.set_ylabel("Portfolio Sharpe Ratio", color="#5a6e55")
    ax.set_title(f"Sharpe Ratio vs Risk Aversion  (θ = {theta})", color="#2d5016", fontweight="bold")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.2, color="#c8dfc0")

    ax = axes[1, 1]
    im = ax.imshow(heatmap, aspect="auto", origin="lower", cmap="RdYlGn",
                   vmin=min(heatmap.flatten()), vmax=max(heatmap.flatten()),                   extent=[theta_grid[0], theta_grid[-1],
                           gamma_grid[0], gamma_grid[-1]])
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Portfolio ESG Score", color="#5a6e55")
    cbar.ax.yaxis.set_tick_params(color="#5a6e55")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#5a6e55")
    ax.scatter(theta, gamma, marker="*", color="#2d5016", s=250, zorder=5, label="✨ Your profile")
    ax.set_xlabel("ESG Preference (θ)", color="#5a6e55")
    ax.set_ylabel("Risk Aversion (γ)", color="#5a6e55")
    ax.set_title("ESG Score across Parameter Space", color="#2d5016", fontweight="bold")
    ax.legend(fontsize=8, loc="upper left")

    plt.tight_layout()
    st.pyplot(fig_sa)
    plt.close(fig_sa)


# ── Footer ────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("#### ⚠️ Model Limitations")
st.caption(
    "This model assumes normally distributed returns, constant correlations, and static ESG scores. "
    "In practice, ESG ratings differ across providers and financial markets are dynamic."
)
st.caption("ESGenie 🧞 · Sustainable Portfolio Advisor · Built with Streamlit · Sustainable Finance")