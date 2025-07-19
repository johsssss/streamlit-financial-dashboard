import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📉 Business Failure Forecast", layout="wide")
st.title("📉 Business Failure Simulation (5-Year Forecast)")

st.sidebar.header("📋 Base Year Financial Data")
base_assets = st.sidebar.number_input("🧾 Total Assets (Year 0)", 1_000_000, 10_000_000, 2_676_930, step=100_000)
base_liabilities = st.sidebar.number_input("📉 Total Liabilities (Year 0)", 500_000, 10_000_000, 2_000_489, step=100_000)
base_revenue = st.sidebar.number_input("💰 Gross Revenue (Year 0)", 1_000_000, 10_000_000, 1_575_379, step=100_000)
base_net_income = st.sidebar.number_input("💸 Net Income (Year 0)", -500_000, 500_000, 36_675, step=10_000)

years = [f"Year {i}" for i in range(6)]

def simulate_decline(base, decline_rate):
    return [base * ((1 - decline_rate) ** i) for i in range(6)]

# Define 3 scenarios
scenarios = {
    "Mild Decline (10%)": 0.10,
    "Moderate Decline (20%)": 0.20,
    "Severe Decline (30%)": 0.30
}

# Display each scenario
for label, rate in scenarios.items():
    st.subheader(f"📉 Scenario: {label}")

    df = pd.DataFrame({
        "Total Assets": simulate_decline(base_assets, rate),
        "Total Liabilities": simulate_decline(base_liabilities, rate),
        "Gross Revenue": simulate_decline(base_revenue, rate),
        "Net Income": simulate_decline(base_net_income, rate)
    }, index=years)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Financial Deterioration")
        fig, ax = plt.subplots(figsize=(8, 4))
        df[["Total Assets", "Total Liabilities"]].plot(ax=ax, marker='o')
        ax.set_title("Assets vs Liabilities Over 5 Years")
        ax.set_ylabel("PHP")
        ax.grid(True)
        st.pyplot(fig)

    with col2:
        st.markdown("#### 💸 Revenue and Net Income")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        df[["Gross Revenue", "Net Income"]].plot(ax=ax2, marker='o', linestyle='--')
        ax2.set_title("Revenue and Net Income Over 5 Years")
        ax2.set_ylabel("PHP")
        ax2.grid(True)
        st.pyplot(fig2)

    st.markdown("#### 📋 Detailed Forecast Table")
    st.dataframe(df.style.format("{:,.0f}"))
