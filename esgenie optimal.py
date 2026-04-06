# ─────────────────────────────────────────────
# Imports + Page Setup
# ─────────────────────────────────────────────
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="ESGenie", layout="wide")

st.title("🌱 ESGenie: Sustainable Portfolio Advisor")
st.write("Optimise your portfolio based on risk, return, and ESG preferences.")

# ─────────────────────────────────────────────
# Investor Presets
# ─────────────────────────────────────────────
st.subheader("Quick Start (Optional)")

preset = st.selectbox(
    "Choose an investor profile:",
    ["Custom", "Eco Investor", "Balanced", "Return Focused"]
)

if preset == "Eco Investor":
    theta_default = 3.5
    risk_default = 10
elif preset == "Balanced":
    theta_default = 2.0
    risk_default = 5
elif preset == "Return Focused":
    theta_default = 0.5
    risk_default = 2
else:
    theta_default = 2.0
    risk_default = 5

# ─────────────────────────────────────────────
# Financial Inputs
# ─────────────────────────────────────────────
st.header("1. Financial Data")

col1, col2 = st.columns(2)

with col1:
    r_h = st.number_input("Asset 1 Return (%)", value=8.0) / 100
    sd_h = st.number_input("Asset 1 Risk (%)", value=20.0) / 100

with col2:
    r_f = st.number_input("Asset 2 Return (%)", value=4.0) / 100
    sd_f = st.number_input("Asset 2 Risk (%)", value=10.0) / 100

rho_hf = st.slider("Correlation", -1.0, 1.0, 0.2)
r_free = st.number_input("Risk-Free Rate (%)", value=2.0) / 100

# ─────────────────────────────────────────────
# Risk Profile
# ─────────────────────────────────────────────
st.header("2. Risk Profile")

risk_options = ["Conservative", "Balanced", "Aggressive"]
default_index = {10: 0, 5: 1, 2: 2}[risk_default]

risk_choice = st.selectbox("Select risk tolerance:", risk_options, index=default_index)

risk_map = {"Conservative": 10, "Balanced": 5, "Aggressive": 2}
risk_aversion = risk_map[risk_choice]

# ─────────────────────────────────────────────
# ESG Preferences
# ─────────────────────────────────────────────
st.header("3. ESG Preferences")

theta = st.slider("Importance of ESG (θ)", 0.0, 4.0, theta_default)

# ─────────────────────────────────────────────
# ESG Scores
# ─────────────────────────────────────────────
st.header("4. Asset ESG Scores")

E1 = st.slider("Asset 1 Environmental", 0, 100, 60)
S1 = st.slider("Asset 1 Social", 0, 100, 60)
G1 = st.slider("Asset 1 Governance", 0, 100, 60)

E2 = st.slider("Asset 2 Environmental", 0, 100, 40)
S2 = st.slider("Asset 2 Social", 0, 100, 40)
G2 = st.slider("Asset 2 Governance", 0, 100, 40)

w_e, w_s, w_g = 0.34, 0.33, 0.33

# ─────────────────────────────────────────────
# Ethical Screening
# ─────────────────────────────────────────────
st.header("5. Ethical Screening")

exclude_asset1 = st.checkbox("Exclude Asset 1")
exclude_asset2 = st.checkbox("Exclude Asset 2")

threshold = st.slider("Minimum ESG Threshold", 0, 100, 0)
strict_esg = st.checkbox("Apply Strict ESG Constraint")

# ─────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────
def compute_esg(E, S, G):
    return w_e * E + w_s * S + w_g * G

def portfolio_ret(w):
    return w * r_h + (1 - w) * r_f

def portfolio_sd(w):
    return np.sqrt(
        w**2 * sd_h**2 +
        (1 - w)**2 * sd_f**2 +
        2 * rho_hf * w * (1 - w) * sd_h * sd_f
    )

def portfolio_esg(w):
    return w * esg_h + (1 - w) * esg_f

def classify_esg(score):
    if score >= 80:
        return "High ESG"
    elif score >= 50:
        return "Moderate ESG"
    else:
        return "Low ESG"

def utility(w):
    ret = portfolio_ret(w)
    sd = portfolio_sd(w)
    esg = portfolio_esg(w)

    u = (ret - r_free) - (risk_aversion / 2) * sd**2 + theta * (esg / 100)

    if exclude_asset1:
        u -= 1e6 * w
    if exclude_asset2:
        u -= 1e6 * (1 - w)

    if threshold > 0 and esg < threshold:
        u -= 0.01 * theta

    return u

# ─────────────────────────────────────────────
# Compute ESG first
# ─────────────────────────────────────────────
esg_h = compute_esg(E1, S1, G1)
esg_f = compute_esg(E2, S2, G2)

# ─────────────────────────────────────────────
# Optimisation
# ─────────────────────────────────────────────
weights = np.linspace(0, 1, 1000)
utilities = np.array([utility(w) for w in weights])

w_opt = weights[np.argmax(utilities)]

# Financial-only benchmark
sharpes = [
    (portfolio_ret(w) - r_free) / portfolio_sd(w)
    if portfolio_sd(w) > 0 else 0
    for w in weights
]
w_tan = weights[np.argmax(sharpes)]

# ─────────────────────────────────────────────
# Outputs
# ─────────────────────────────────────────────
ret_opt = portfolio_ret(w_opt)
sd_opt = portfolio_sd(w_opt)
esg_opt = portfolio_esg(w_opt)

ret_tan = portfolio_ret(w_tan)
sd_tan = portfolio_sd(w_tan)

# ESG Premium
sharpe_opt = (ret_opt - r_free) / sd_opt if sd_opt > 0 else 0
sharpe_tan = max(sharpes)
esg_premium = sharpe_tan - sharpe_opt

# ─────────────────────────────────────────────
# Results
# ─────────────────────────────────────────────
st.header("📊 Results")

st.write(f"Optimal weight in Asset 1: {w_opt*100:.1f}%")
st.write(f"Expected Return: {ret_opt*100:.2f}%")
st.write(f"Risk: {sd_opt*100:.2f}%")
st.write(f"ESG Score: {esg_opt:.1f}")
st.write(f"ESG Class: {classify_esg(esg_opt)}")

st.write(f"ESG Premium: {esg_premium:.3f}")

# ─────────────────────────────────────────────
# Investor Identity
# ─────────────────────────────────────────────
if theta > 3:
    st.success("🌱 You are an Impact Investor")
elif theta > 1.5:
    st.info("⚖️ You are a Balanced ESG Investor")
else:
    st.warning("💰 You are a Return-Focused Investor")

# ─────────────────────────────────────────────
# Interpretation
# ─────────────────────────────────────────────
st.subheader("💬 Recommendation")

st.info(
    f"Based on your risk profile (γ={risk_aversion}) and ESG preference (θ={theta}), "
    f"the optimal portfolio allocates {w_opt*100:.1f}% to Asset 1."
)

# ─────────────────────────────────────────────
# ESG Constraint Check
# ─────────────────────────────────────────────
if strict_esg and esg_opt < 50:
    st.error("⚠️ Portfolio does not meet strict ESG requirements")

# ─────────────────────────────────────────────
# ESG-Coloured Frontier
# ─────────────────────────────────────────────
returns = [portfolio_ret(w) for w in weights]
risks = [portfolio_sd(w) for w in weights]
esg_vals = [portfolio_esg(w) for w in weights]

plt.figure()
plt.scatter(risks, returns, c=esg_vals, cmap='RdYlGn')
plt.colorbar(label="ESG Score")
plt.scatter(sd_opt, ret_opt, color='black', label='Optimal')
plt.scatter(sd_tan, ret_tan, color='blue', label='Tangency')
plt.legend()
plt.xlabel("Risk")
plt.ylabel("Return")
st.pyplot(plt)

# ─────────────────────────────────────────────
# Sensitivity Analysis
# ─────────────────────────────────────────────
theta_range = np.linspace(0, 4, 50)
weights_sa = []

for t in theta_range:
    temp_utils = [
        (portfolio_ret(w) - r_free) - (risk_aversion / 2) * portfolio_sd(w)**2 + t * (portfolio_esg(w)/100)
        for w in weights
    ]
    weights_sa.append(weights[np.argmax(temp_utils)])

plt.figure()
plt.plot(theta_range, weights_sa)
plt.axvline(theta, linestyle='--', label='Your θ')
plt.legend()
plt.xlabel("θ")
plt.ylabel("Optimal Weight")
st.pyplot(plt)

# ─────────────────────────────────────────────
# Download
# ─────────────────────────────────────────────
summary = f"""
Optimal weight: {w_opt*100:.1f}%
Return: {ret_opt*100:.2f}%
Risk: {sd_opt*100:.2f}%
ESG: {esg_opt:.1f}
"""

st.download_button("Download Summary", summary)

# ─────────────────────────────────────────────
# Final Insight
# ─────────────────────────────────────────────
st.caption(
    "This app extends traditional portfolio theory by incorporating ESG preferences directly into investor utility, "
    "allowing for realistic sustainable investment decisions."
)