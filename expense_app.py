import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from datetime import datetime

DATA_FILE = "data/expenses.csv"

def load_data():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
        df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.read_csv(DATA_FILE)
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finesse · Finance Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=DM+Mono:wght@300;400&family=Outfit:wght@300;400;500&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0A0C10;
    --surface:   #0F1218;
    --card:      #13171F;
    --border:    #1E2530;
    --border2:   #252D3A;
    --gold:      #C9A96E;
    --gold-dim:  #8A6E42;
    --teal:      #4ECDC4;
    --teal-dim:  #2A7A75;
    --red:       #E05C5C;
    --green:     #5CBF87;
    --text:      #E8EAF0;
    --muted:     #6B7585;
    --muted2:    #4A5260;
}

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 300;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    font-family: 'Outfit', sans-serif !important;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.5rem 2.5rem 2rem !important;
    max-width: 1400px !important;
}

/* ── Sidebar nav ── */
[data-testid="stSidebar"] .stRadio > label {
    display: none;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    display: block !important;
    padding: 10px 16px !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    border: 1px solid transparent !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: var(--card) !important;
    color: var(--text) !important;
    border-color: var(--border2) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] input:checked + div {
    background: var(--card) !important;
    color: var(--gold) !important;
    border-color: var(--gold-dim) !important;
}

/* ── Cards ── */
.fin-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 28px;
    position: relative;
    overflow: hidden;
}
.fin-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold-dim), transparent);
}

/* ── KPI cards ── */
.kpi-wrap {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.kpi-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 24px 18px;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 24px; right: 24px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border2), transparent);
}
.kpi-label {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
    font-family: 'DM Mono', monospace;
}
.kpi-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 34px;
    font-weight: 300;
    color: var(--text);
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-value.gold { color: var(--gold); }
.kpi-value.teal { color: var(--teal); }
.kpi-sub {
    font-size: 11px;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
}

/* ── Section headers ── */
.sec-header {
    font-family: 'Cormorant Garamond', serif;
    font-size: 26px;
    font-weight: 300;
    color: var(--text);
    letter-spacing: 0.02em;
    margin-bottom: 4px;
}
.sec-sub {
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    margin-bottom: 20px;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 32px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
}
.page-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 42px;
    font-weight: 300;
    color: var(--text);
    letter-spacing: -0.01em;
    line-height: 1;
}
.page-title span { color: var(--gold); }
.page-date {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 0.1em;
}

/* ── Table ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] table {
    background: var(--card) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}
[data-testid="stDataFrame"] th {
    background: var(--surface) !important;
    color: var(--muted) !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 12px 16px !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text) !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 10px 16px !important;
}
[data-testid="stDataFrame"] tr:hover td {
    background: var(--surface) !important;
}

/* ── Form inputs ── */
.stTextInput input, .stNumberInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--gold-dim) !important;
    box-shadow: 0 0 0 2px rgba(201,169,110,0.08) !important;
}
[data-testid="stDateInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 11px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace !important;
    margin-bottom: 6px !important;
}

/* ── Submit button ── */
.stFormSubmitButton button {
    background: linear-gradient(135deg, #C9A96E 0%, #A07840 100%) !important;
    color: #0A0C10 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 12px 32px !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stFormSubmitButton button:hover {
    opacity: 0.88 !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 4px !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    border: none !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--card) !important;
    color: var(--gold) !important;
    border: 1px solid var(--border2) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: var(--card) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 24px 0 !important;
}

/* ── Sidebar brand ── */
.sidebar-brand {
    padding: 8px 0 24px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.brand-mark {
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px;
    font-weight: 300;
    color: var(--gold);
    letter-spacing: 0.08em;
}
.brand-sub {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: var(--muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 2px;
}
.nav-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: var(--muted2);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 8px;
    padding-left: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme ─────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#13171F",
    "axes.facecolor":    "#13171F",
    "axes.edgecolor":    "#1E2530",
    "axes.labelcolor":   "#6B7585",
    "axes.grid":         True,
    "grid.color":        "#1E2530",
    "grid.linewidth":    0.5,
    "xtick.color":       "#6B7585",
    "ytick.color":       "#6B7585",
    "text.color":        "#E8EAF0",
    "font.family":       "monospace",
    "font.size":         10,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.spines.left":  False,
})

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-mark">◈ FINESSE</div>
        <div class="brand-sub">Finance Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)
    menu = st.radio("", ["Dashboard", "Add Expense", "Analytics", "About"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="nav-label">Current Period</div>', unsafe_allow_html=True)
    now = datetime.now()
    st.markdown(f"""
    <div style="font-family:'DM Mono',monospace; font-size:11px; color:#6B7585; padding: 0 4px;">
        {now.strftime("%B %Y")}<br>
        <span style="font-size:10px; color:#4A5260;">{now.strftime("%A, %d %b")}</span>
    </div>
    """, unsafe_allow_html=True)

df = load_data()

# ── Page header ───────────────────────────────────────────────────────────────
page_titles = {
    "Dashboard":   ("Overview", "Financial Summary"),
    "Add Expense": ("New Entry", "Record a Transaction"),
    "Analytics":   ("Analytics", "Spending Insights"),
    "About":       ("About", "Project Information"),
}
title, subtitle = page_titles[menu]

st.markdown(f"""
<div class="page-header">
    <div>
        <div class="page-title">{title}<span>.</span></div>
        <div style="font-family:'DM Mono',monospace; font-size:10px; color:#4A5260;
                    letter-spacing:0.15em; text-transform:uppercase; margin-top:6px;">
            {subtitle}
        </div>
    </div>
    <div class="page-date">{now.strftime("%d %b %Y · %H:%M")}</div>
</div>
""", unsafe_allow_html=True)

# ── Dashboard ─────────────────────────────────────────────────────────────────
if menu == "Dashboard":
    if df.empty:
        st.markdown("""
        <div class="fin-card" style="text-align:center; padding: 48px;">
            <div style="font-family:'Cormorant Garamond',serif; font-size:48px; 
                        color:#1E2530; margin-bottom:12px;">◈</div>
            <div style="font-family:'Cormorant Garamond',serif; font-size:22px; 
                        color:#6B7585; font-weight:300;">No transactions yet</div>
            <div style="font-family:'DM Mono',monospace; font-size:11px; 
                        color:#4A5260; margin-top:8px;">
                Navigate to Add Expense to begin tracking
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df["Date"] = pd.to_datetime(df["Date"])
        current_month = df["Date"].dt.to_period("M").max()
        cm_df = df[df["Date"].dt.to_period("M") == current_month]

        total        = df["Amount"].sum()
        count        = len(df)
        avg          = df["Amount"].mean()
        month_spent  = cm_df["Amount"].sum()
        top_cat      = df.groupby("Category")["Amount"].sum().idxmax() if not df.empty else "—"

        # KPI cards
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-card">
                <div class="kpi-label">Total Spent</div>
                <div class="kpi-value gold">₹{total:,.0f}</div>
                <div class="kpi-sub">all time · {count} entries</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">This Month</div>
                <div class="kpi-value teal">₹{month_spent:,.0f}</div>
                <div class="kpi-sub">{str(current_month)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avg per Entry</div>
                <div class="kpi-value">₹{avg:,.0f}</div>
                <div class="kpi-sub">across all transactions</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Top Category</div>
                <div class="kpi-value" style="font-size:24px;">{top_cat}</div>
                <div class="kpi-sub">highest spend</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Recent transactions
        st.markdown("""
        <div style="font-family:'DM Mono',monospace; font-size:10px; color:#4A5260;
                    letter-spacing:0.15em; text-transform:uppercase; margin-bottom:12px;">
            Recent Transactions
        </div>
        """, unsafe_allow_html=True)

        display_df = df.sort_values("Date", ascending=False).head(15).copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%d %b %Y")
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── Add Expense ───────────────────────────────────────────────────────────────
elif menu == "Add Expense":
    col_form, col_gap = st.columns([1, 1])
    with col_form:
        st.markdown('<div class="fin-card">', unsafe_allow_html=True)
        with st.form("expense_form", clear_on_submit=True):
            date     = st.date_input("Date", datetime.now())
            amount   = st.number_input("Amount (₹)", min_value=0.0, step=1.0, format="%.2f")
            category = st.text_input("Category", placeholder="Food, Transport, Shopping…")
            desc     = st.text_input("Description", placeholder="Brief note…")
            submitted = st.form_submit_button("Record Transaction")
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if amount <= 0:
                st.error("Amount must be greater than zero.")
            elif not category.strip():
                st.error("Please enter a category.")
            else:
                new_row = {
                    "Date":        date.strftime("%Y-%m-%d"),
                    "Amount":      amount,
                    "Category":    category.strip(),
                    "Description": desc.strip(),
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.success(f"Recorded · ₹{amount:,.2f} · {category}")

    with col_gap:
        # Quick tip card
        st.markdown("""
        <div class="fin-card" style="height:100%; box-sizing:border-box;">
            <div style="font-family:'Cormorant Garamond',serif; font-size:20px;
                        color:#C9A96E; margin-bottom:16px; font-weight:300;">
                Quick Guide
            </div>
            <div style="font-family:'DM Mono',monospace; font-size:11px;
                        color:#6B7585; line-height:2;">
                ◦ &nbsp;Use consistent category names<br>
                ◦ &nbsp;Add descriptions for clarity<br>
                ◦ &nbsp;Track daily for best insights<br>
                ◦ &nbsp;View Analytics after 7+ entries
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Analytics ─────────────────────────────────────────────────────────────────
elif menu == "Analytics":
    if df.empty:
        st.markdown("""
        <div class="fin-card" style="text-align:center; padding:48px;">
            <div style="font-family:'Cormorant Garamond',serif; font-size:22px;
                        color:#6B7585; font-weight:300;">
                No data to analyse
            </div>
            <div style="font-family:'DM Mono',monospace; font-size:11px;
                        color:#4A5260; margin-top:8px;">
                Add at least a few expenses to unlock insights
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df["Date"]  = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.to_period("M")

        tab1, tab2, tab3 = st.tabs(["By Category", "Monthly Trend", "High-Spend Days"])

        # ── By Category
        with tab1:
            by_cat = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            col_c, col_t = st.columns([3, 1])

            with col_c:
                fig, ax = plt.subplots(figsize=(9, 4))
                bars = ax.bar(
                    by_cat.index, by_cat.values,
                    color="#C9A96E", width=0.55,
                    edgecolor="none",
                )
                # Gradient effect — darken alternates
                for i, bar in enumerate(bars):
                    bar.set_alpha(1.0 if i % 2 == 0 else 0.65)

                ax.set_ylabel("Amount (₹)", color="#6B7585", fontsize=9)
                ax.set_xlabel("")
                ax.tick_params(axis="x", rotation=30, labelsize=9)
                ax.yaxis.set_tick_params(labelsize=9)
                fig.tight_layout(pad=1.5)
                st.pyplot(fig)
                plt.close(fig)

            with col_t:
                st.markdown("""
                <div style="font-family:'DM Mono',monospace; font-size:10px;
                            color:#4A5260; letter-spacing:0.12em; text-transform:uppercase;
                            margin-bottom:10px;">Breakdown</div>
                """, unsafe_allow_html=True)
                total_cat = by_cat.sum()
                for cat, amt in by_cat.items():
                    pct = (amt / total_cat) * 100
                    st.markdown(f"""
                    <div style="margin-bottom:10px;">
                        <div style="font-family:'Outfit',sans-serif; font-size:12px;
                                    color:#E8EAF0;">{cat}</div>
                        <div style="font-family:'DM Mono',monospace; font-size:11px;
                                    color:#C9A96E;">₹{amt:,.0f}
                            <span style="color:#4A5260;">· {pct:.1f}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # ── Monthly Trend
        with tab2:
            monthly = df.groupby("Month")["Amount"].sum()
            if len(monthly) < 1:
                st.info("Need at least 1 month of data.")
            else:
                fig, ax = plt.subplots(figsize=(10, 4))
                x = list(range(len(monthly)))
                ax.fill_between(
                    x, monthly.values,
                    alpha=0.12, color="#4ECDC4"
                )
                ax.plot(
                    x, monthly.values,
                    color="#4ECDC4", linewidth=2,
                    marker="o", markersize=6,
                    markerfacecolor="#13171F",
                    markeredgecolor="#4ECDC4",
                    markeredgewidth=2,
                )
                ax.set_xticks(x)
                ax.set_xticklabels(monthly.index.astype(str), rotation=30, fontsize=9)
                ax.set_ylabel("Amount (₹)", color="#6B7585", fontsize=9)
                fig.tight_layout(pad=1.5)
                st.pyplot(fig)
                plt.close(fig)

                # Month summary
                cols = st.columns(min(len(monthly), 4))
                for i, (month, amt) in enumerate(monthly.items()):
                    if i < 4:
                        cols[i].markdown(f"""
                        <div class="kpi-card" style="margin-top:16px;">
                            <div class="kpi-label">{str(month)}</div>
                            <div class="kpi-value teal" style="font-size:24px;">₹{amt:,.0f}</div>
                        </div>
                        """, unsafe_allow_html=True)

        # ── High Spend Days
        with tab3:
            daily     = df.groupby(df["Date"].dt.date)["Amount"].sum()
            mean_d    = daily.mean()
            high_days = daily[daily > 2 * mean_d].sort_values(ascending=False)

            st.markdown(f"""
            <div style="font-family:'DM Mono',monospace; font-size:11px;
                        color:#6B7585; margin-bottom:16px;">
                Daily average: <span style="color:#C9A96E;">₹{mean_d:,.0f}</span> &nbsp;·&nbsp;
                Threshold (2×): <span style="color:#E05C5C;">₹{2*mean_d:,.0f}</span>
            </div>
            """, unsafe_allow_html=True)

            if high_days.empty:
                st.markdown("""
                <div class="fin-card" style="text-align:center; padding:28px;">
                    <div style="font-family:'Cormorant Garamond',serif; font-size:20px;
                                color:#5CBF87; font-weight:300;">
                        All clear — no high-spend days detected
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.bar(
                    [str(d) for d in high_days.index],
                    high_days.values,
                    color="#E05C5C", alpha=0.85, width=0.5, edgecolor="none"
                )
                ax.axhline(2 * mean_d, color="#C9A96E", linewidth=1,
                           linestyle="--", alpha=0.6, label=f"2× avg")
                ax.legend(fontsize=9, framealpha=0)
                ax.set_ylabel("Amount (₹)", color="#6B7585", fontsize=9)
                ax.tick_params(axis="x", rotation=30, labelsize=9)
                fig.tight_layout(pad=1.5)
                st.pyplot(fig)
                plt.close(fig)

# ── About ─────────────────────────────────────────────────────────────────────
elif menu == "About":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="fin-card">
            <div style="font-family:'Cormorant Garamond',serif; font-size:32px;
                        font-weight:300; color:#C9A96E; margin-bottom:6px;">
                Finesse
            </div>
            <div style="font-family:'DM Mono',monospace; font-size:10px;
                        color:#4A5260; letter-spacing:0.2em; text-transform:uppercase;
                        margin-bottom:24px;">
                Personal Finance Dashboard
            </div>
            <div style="font-family:'Outfit',sans-serif; font-size:14px;
                        color:#6B7585; line-height:1.8;">
                A refined expense tracking and analytics tool built to give you
                clear visibility into your spending patterns — without the clutter.
                <br><br>
                Track daily expenses, analyse monthly trends, and identify
                unusual spending days — all from a single dashboard.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="fin-card">
            <div style="font-family:'DM Mono',monospace; font-size:10px;
                        color:#4A5260; letter-spacing:0.15em; text-transform:uppercase;
                        margin-bottom:16px;">Tech Stack</div>
            <div style="font-family:'Outfit',sans-serif; font-size:13px;
                        color:#6B7585; line-height:2.2;">
                <span style="color:#C9A96E;">◦</span> &nbsp;Python 3<br>
                <span style="color:#C9A96E;">◦</span> &nbsp;Streamlit<br>
                <span style="color:#C9A96E;">◦</span> &nbsp;Pandas<br>
                <span style="color:#C9A96E;">◦</span> &nbsp;Matplotlib<br>
                <span style="color:#C9A96E;">◦</span> &nbsp;CSV storage
            </div>
        </div>
        """, unsafe_allow_html=True)