import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit configuration
st.set_page_config(page_title="📊 Interactive Financial Dashboard", layout="wide")
st.title("📊 Interactive Financial Dashboard")

# Sidebar: Controls for data inputs
st.sidebar.header("📋 Input Financial Data")

with st.sidebar.form("financial_form"):
    st.subheader("Balance Sheet")
    ta_prev = st.slider("Total Assets - Previous Year", 1_000_000, 5_000_000, 2_459_365, step=100_000)
    ta_curr = st.slider("Total Assets - Current Year", 1_000_000, 5_000_000, 2_676_930, step=100_000)

    tl_prev = st.slider("Total Liabilities - Previous Year", 1_000_000, 5_000_000, 1_794_199, step=100_000)
    tl_curr = st.slider("Total Liabilities - Current Year", 1_000_000, 5_000_000, 2_000_489, step=100_000)

    eq_prev = st.slider("Stockholders' Equity - Previous Year", 500_000, 2_000_000, 665_166, step=50_000)
    eq_curr = st.slider("Stockholders' Equity - Current Year", 500_000, 2_000_000, 676_441, step=50_000)

    st.subheader("Income Statement")
    rev_prev = st.slider("Gross Revenue - Previous Year", 1_000_000, 3_000_000, 1_446_703, step=50_000)
    rev_curr = st.slider("Gross Revenue - Current Year", 1_000_000, 3_000_000, 1_575_379, step=50_000)

    exp_prev = st.slider("Gross Expense - Previous Year", 1_000_000, 3_000_000, 1_302_218, step=50_000)
    exp_curr = st.slider("Gross Expense - Current Year", 1_000_000, 3_000_000, 1_414_563, step=50_000)

    net_prev = st.slider("Net Income - Previous Year", -50_000, 100_000, 44_699, step=1000)
    net_curr = st.slider("Net Income - Current Year", -50_000, 100_000, 36_675, step=1000)

    eps_prev = st.number_input("EPS - Previous Year", value=-2.51, step=0.1)
    eps_curr = st.number_input("EPS - Current Year", value=-7.10, step=0.1)

    submitted = st.form_submit_button("Update Dashboard")

# If submitted, show output
data_submitted = submitted or 'ta_curr' in locals()
if data_submitted:
    years = ["Previous Year", "Current Year"]
    summary = {
        "Total Assets": [ta_prev, ta_curr],
        "Total Liabilities": [tl_prev, tl_curr],
        "Stockholders' Equity": [eq_prev, eq_curr],
        "Gross Revenue": [rev_prev, rev_curr],
        "Gross Expense": [exp_prev, exp_curr],
        "Net Income": [net_prev, net_curr],
        "EPS": [eps_prev, eps_curr]
    }
    df = pd.DataFrame(summary, index=years).T

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Balance Sheet Trends")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(years, df.loc["Total Assets"], marker='o', label='Total Assets')
        ax.plot(years, df.loc["Total Liabilities"], marker='o', label='Total Liabilities')
        ax.plot(years, df.loc["Stockholders' Equity"], marker='o', label='Equity')
        ax.set_title("Assets vs Liabilities vs Equity")
        ax.set_ylabel("Amount (PHP)")
        ax.legend()
        st.pyplot(fig)

    with col2:
        st.subheader("📊 Income vs Expenses")
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        df_income = df.loc[["Gross Revenue", "Gross Expense", "Net Income"]].T
        df_income.plot(kind='bar', ax=ax2)
        ax2.set_ylabel("Amount (PHP)")
        ax2.set_title("Income Statement Components")
        ax2.grid(axis='y')
        st.pyplot(fig2)

    st.subheader("💵 Earnings Per Share")
    eps_colors = ['green' if v > 0 else 'red' for v in df.loc["EPS"]]
    fig3, ax3 = plt.subplots(figsize=(6, 3))
    ax3.bar(years, df.loc["EPS"], color=eps_colors)
    ax3.set_ylabel("EPS")
    ax3.set_title("EPS Comparison")
    for i, val in enumerate(df.loc["EPS"]):
        ax3.text(i, val + (0.5 if val > 0 else -1), f"{val:.2f}", ha='center')
    st.pyplot(fig3)

    st.subheader("📋 Financial Summary Table")
    st.dataframe(df.style.format("{:.2f}"))
