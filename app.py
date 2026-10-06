import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

DATA_FILE = "data/expenses.csv"


def load_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
        df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.read_csv(DATA_FILE)
    return df


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# ---------- PAGE CONFIG + TITLE ----------
st.set_page_config(
    page_title="Smart Finance Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 13px;
        opacity: 0.85;
        margin-bottom: 1rem;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Smart Finance Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Personal expense tracking and analytics</div>',
    unsafe_allow_html=True,
)

# ---------- SIDEBAR ----------
st.sidebar.markdown("### Navigation")
menu = st.sidebar.radio(
    "",
    ["Dashboard", "Add Expense", "Analytics", "About"],
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Settings")

df = load_data()

# ---------- DASHBOARD PAGE ----------
if menu == "Dashboard":
    st.subheader("Overview")

    if df.empty:
        st.info("No expenses yet. Use **Add Expense** to start tracking.")
    else:
        df["Date"] = pd.to_datetime(df["Date"])
        current_month = df["Date"].dt.to_period("M").max()
        current_month_df = df[df["Date"].dt.to_period("M") == current_month]

        total = df["Amount"].sum()
        count = len(df)
        avg = df["Amount"].mean()
        this_month_spent = current_month_df["Amount"].sum()

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total Spent (All Time)", f"₹{total:.2f}")
        kpi2.metric("Entries", count)
        kpi3.metric("Avg per Expense", f"₹{avg:.2f}")
        kpi4.metric(f"Spent in {str(current_month)}", f"₹{this_month_spent:.2f}")

        st.markdown("---")
        st.markdown("#### Recent Transactions")
        st.dataframe(
            df.sort_values("Date", ascending=False).head(15),
            use_container_width=True,
        )

# ---------- ADD EXPENSE PAGE ----------
elif menu == "Add Expense":
    st.subheader("Add Expense")
    st.markdown("Fill in the details below to record a new transaction.")

    with st.form("expense_form"):
        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Date", datetime.now())
            amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")

        with col2:
            category = st.text_input("Category (e.g., Food, Transport, Shopping)")
            description = st.text_input("Description")

        submitted = st.form_submit_button("Save")

    if submitted:
        new_row = {
            "Date": date.strftime("%Y-%m-%d"),
            "Amount": amount,
            "Category": category,
            "Description": description,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("Expense added.")

# ---------- ANALYTICS PAGE ----------
elif menu == "Analytics":
    st.subheader("Spending Analytics")

    if df.empty:
        st.info("No data available. Add expenses to see analytics.")
    else:
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.to_period("M")

        tab1, tab2, tab3 = st.tabs(["By Category", "Monthly Trend", "High-Spending Days"])

        # By Category
        with tab1:
            st.markdown("##### Category Breakdown")
            by_cat = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            col_chart, col_table = st.columns((2, 1))

            with col_chart:
                fig1, ax1 = plt.subplots()
                by_cat.plot(kind="bar", ax=ax1, color="#60A5FA")
                ax1.set_ylabel("Amount (₹)")
                ax1.set_xlabel("Category")
                ax1.tick_params(axis="x", rotation=45)
                ax1.grid(alpha=0.25, axis="y")
                st.pyplot(fig1)

            with col_table:
                st.dataframe(by_cat.rename("Amount (₹)"))

        # Monthly Trend
        with tab2:
            st.markdown("##### Monthly Spending Trend")
            monthly = df.groupby("Month")["Amount"].sum()
            if not monthly.empty:
                fig2, ax2 = plt.subplots()
                ax2.plot(
                    monthly.index.astype(str),
                    monthly.values,
                    marker="o",
                    linewidth=2,
                    color="#34D399",
                )
                ax2.set_ylabel("Amount (₹)")
                ax2.set_xlabel("Month")
                ax2.grid(alpha=0.25)
                st.pyplot(fig2)
            else:
                st.write("Not enough data to show monthly trend.")

        # High-Spending Days
        with tab3:
            st.markdown("##### High-Spending Days")
            daily = df.groupby(df["Date"].dt.date)["Amount"].sum()
            if not daily.empty:
                mean_daily = daily.mean()
                high_days = daily[daily > 2 * mean_daily]
                if high_days.empty:
                    st.success("No high-spending days above 2× average.")
                else:
                    st.dataframe(high_days.rename("Amount (₹)"))
            else:
                st.write("Not enough data to compute daily statistics.")

# ---------- ABOUT PAGE ----------
elif menu == "About":
    st.subheader("About")
    st.markdown(
        """
        **Smart Finance Dashboard** is a personal finance project built with:

        - Python  
        - Pandas and Matplotlib for data processing and visualization  
        - Streamlit for the web interface  

        It provides expense tracking, monthly overview, and basic analytics
        for spending patterns. This project was developed as a portfolio
        piece to demonstrate data analysis and dashboard development skills.
        """
    )