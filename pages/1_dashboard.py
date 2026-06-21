import streamlit as st
import pandas as pd
from datetime import datetime
from utils.db import get_expenses_by_month, get_monthly_summary
import plotly.graph_objects as go

st.set_page_config(page_title="Spending Console", layout="wide", initial_sidebar_state="collapsed")

# ── SHARED DESIGN SYSTEM (identical to home page) ─────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem 2.5rem; max-width: 860px; }

h1 {
    font-weight: 700 !important;
    letter-spacing: -0.04em !important;
    color: #FFFFFF !important;
    font-size: 2.2rem !important;
    margin-bottom: 0.2rem !important;
    line-height: 1.15 !important;
}
p, li, span.muted {
    font-weight: 400;
    line-height: 1.55;
    color: #9EA4B0;
    font-size: 0.95rem;
}
.stButton > button {
    border-radius: 6px !important;
    border: 1px solid #31333F !important;
    background: #16181E !important;
    color: #C8CDD8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 0.55rem 1rem !important;
    width: 100% !important;
    text-align: left !important;
    transition: border-color 0.15s ease, background 0.15s ease !important;
}
.stButton > button:hover {
    border-color: #555B6E !important;
    background: #1E2029 !important;
    color: #FFFFFF !important;
}
div[data-testid="stSegmentedControl"] {
    background: #0E1015 !important;
    border: 1px solid #262730 !important;
    border-radius: 6px !important;
    padding: 3px !important;
}
div[data-testid="stSegmentedControl"] label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #686E7D !important;
    border-radius: 4px !important;
}
.stCaption, small { color: #555B6E !important; font-size: 0.78rem !important; }
hr.divider { border: 0; border-top: 1px solid #262730; margin: 1.2rem 0; }

/* Shared card / block style */
.sys-block {
    border: 1px solid #31333F;
    border-radius: 6px;
    padding: 1.1rem 1.3rem;
    background: #0E1015;
    margin-bottom: 0.5rem;
}
.block-label {
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    color: #555B6E;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.45rem;
}
.block-value {
    font-size: 1.7rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}
.block-caption {
    font-size: 0.75rem;
    color: #555B6E;
    font-weight: 400;
}
.section-label {
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    color: #555B6E;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.75rem;
    margin-top: 1.6rem;
}

/* Ledger */
.ledger-wrap {
    border: 1px solid #31333F;
    border-radius: 6px;
    background: #0E1015;
    overflow: hidden;
}
.ledger-head {
    display: grid;
    grid-template-columns: 80px 1fr 80px 75px 110px;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #16181E;
    border-bottom: 1px solid #262730;
}
.ledger-col { font-size: 0.65rem; letter-spacing: 0.08em; color: #555B6E; text-transform: uppercase; font-weight: 600; }
.ledger-row {
    display: grid;
    grid-template-columns: 80px 1fr 80px 75px 110px;
    gap: 0.5rem;
    padding: 0.65rem 1rem;
    border-bottom: 1px solid #1A1C24;
    align-items: center;
}
.ledger-row:last-child { border-bottom: none; }
.ledger-row:hover { background: #13151C; }
.l-date  { font-size: 0.77rem; color: #686E7D; }
.l-desc  { font-size: 0.82rem; color: #C8CDD8; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.l-cat   { font-size: 0.71rem; background: #1E2029; border: 1px solid #31333F; border-radius: 4px; padding: 0.12rem 0.4rem; color: #9EA4B0; font-family: 'SF Mono','Fira Code',monospace; display: inline-block; }
.l-amt   { font-size: 0.88rem; color: #FFFFFF; font-weight: 700; letter-spacing: -0.02em; }
.l-mood  { font-size: 0.75rem; color: #686E7D; }
</style>
""", unsafe_allow_html=True)

# ── SHARED NAV (identical to home page) ───────────────────────
nav = st.segmented_control(
    label="nav",
    options=["Home", "Dashboard", "Log Expense", "Coach", "Challenges"],
    default="Dashboard",
    label_visibility="collapsed",
)
if nav == "Home":
    st.switch_page("app.py")
elif nav == "Log Expense":
    st.switch_page("pages/2_add_expense.py")
elif nav == "Coach":
    st.switch_page("pages/3_ai_coach.py")
elif nav == "Challenges":
    st.switch_page("pages/4_challenges.py")

# ── FILTERS ────────────────────────────────────────────────────
now   = datetime.now()
col_y, col_m, _ = st.columns([1, 1, 4])
year  = col_y.selectbox("Year",  [2024, 2025, 2026], index=2, label_visibility="collapsed")
month = col_m.selectbox("Month", list(range(1, 13)), index=now.month - 1,
                         format_func=lambda m: datetime(2000, m, 1).strftime("%b"),
                         label_visibility="collapsed")

df = get_expenses_by_month(year, month)

# ── HEADER ─────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
st.markdown("<h1>Spending Console</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='margin-top:0.3rem;'>Real-time analysis of transaction velocities and emotional purchase baselines.</p>",
    unsafe_allow_html=True,
)
st.markdown('<hr style="border:0;border-top:1px solid #262730;margin:1.2rem 0;">', unsafe_allow_html=True)

# ── DERIVED METRICS ────────────────────────────────────────────
total   = df["amount"].sum() if not df.empty else 0
count   = len(df)
avg     = total / count if count > 0 else 0
top_cat = df.groupby("category")["amount"].sum().idxmax() if not df.empty else "—"
top_amt = df.groupby("category")["amount"].sum().max()    if not df.empty else 0

# ── KPI CARDS ─────────────────────────────────────────────────
st.markdown('<div class="section-label">Executive Metrics</div>', unsafe_allow_html=True)
k1, k2, k3 = st.columns(3, gap="medium")

with k1:
    st.markdown(f"""
    <div class="sys-block">
        <div class="block-label">Total Spent</div>
        <div class="block-value">₹{total:,.0f}</div>
        <div class="block-caption">Across {count} logged transactions</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="sys-block">
        <div class="block-label">Volume</div>
        <div class="block-value">{count} Entries</div>
        <div class="block-caption">Averaging ₹{avg:,.0f} per allocation</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="sys-block">
        <div class="block-label">Primary Category</div>
        <div class="block-value">{top_cat}</div>
        <div class="block-caption">₹{top_amt:,.0f} allocated this cycle</div>
    </div>""", unsafe_allow_html=True)

# ── SYSTEM CONTEXT ─────────────────────────────────────────────
if not df.empty and "mood" in df.columns:
    positive_moods = ["Happy 😊", "Celebratory 🎉", "Happy", "Celebratory"]
    positive = df[df["mood"].isin(positive_moods)].shape[0]
    pct      = int((positive / count) * 100) if count > 0 else 0
    largest  = df.loc[df["amount"].idxmax()]
    lmood    = str(largest.get("mood", "an untagged state")).replace("😊","").replace("😰","").replace("😑","").replace("🎉","").replace("😐","").strip()
    lamt     = largest["amount"]
    context  = (
        f"{pct}% of transaction volume this period occurred during positive behavioral states. "
        f"The largest single outflow (₹{lamt:,.0f}) correlated with a {lmood} state. "
        f"Baseline discretionary spending remains stable across the logged window."
    )
else:
    context = (
        "Insufficient data to generate behavioral correlation analysis for this period. "
        "Log expenses with mood tags to unlock contextual intelligence."
    )

st.markdown(f"""
<div class="sys-block" style="margin-top:1rem;">
    <div class="block-label">System Context</div>
    <p style="margin:0;font-size:0.88rem;color:#9EA4B0;line-height:1.65;">{context}</p>
</div>
""", unsafe_allow_html=True)

# ── CHART PALETTE ──────────────────────────────────────────────
PALETTE = ["#4C6EF5","#38BDF8","#34D399","#A78BFA","#F59E0B","#94A3B8","#E879A0"]
BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#686E7D", size=10),
    margin=dict(t=16, b=16, l=8, r=8),
    height=240,
)

# ── CHARTS ────────────────────────────────────────────────────
st.markdown('<div class="section-label">Visualization Grid</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns(2, gap="medium")

with ch1:
    st.markdown("<p style='font-size:0.75rem;color:#555B6E;margin-bottom:0.3rem;letter-spacing:0.04em;'>ALLOCATION BY CATEGORY</p>", unsafe_allow_html=True)
    if not df.empty:
        cat_df = df.groupby("category")["amount"].sum().reset_index()
        fig = go.Figure(go.Pie(
            labels=cat_df["category"],
            values=cat_df["amount"],
            hole=0.58,
            marker=dict(colors=PALETTE[:len(cat_df)], line=dict(color="#0E1015", width=2)),
            textinfo="percent",
            textfont=dict(size=10, color="#C8CDD8"),
            showlegend=True,
        ))
        fig.update_layout(
            **BASE_LAYOUT,
            legend=dict(font=dict(size=9, color="#686E7D"), bgcolor="rgba(0,0,0,0)", x=1, y=0.5),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown("<p style='color:#555B6E;font-size:0.85rem;padding:1.5rem 0;'>No data for this period.</p>", unsafe_allow_html=True)

with ch2:
    st.markdown("<p style='font-size:0.75rem;color:#555B6E;margin-bottom:0.3rem;letter-spacing:0.04em;'>BEHAVIORAL STATE VS OUTFLOW</p>", unsafe_allow_html=True)
    if not df.empty and "mood" in df.columns:
        mood_df = df.groupby("mood")["amount"].sum().reset_index().sort_values("amount", ascending=False)
        mood_df["mood_clean"] = mood_df["mood"].str.replace(r'[^\w\s]', '', regex=True).str.strip()
        fig2 = go.Figure(go.Bar(
            x=mood_df["mood_clean"],
            y=mood_df["amount"],
            marker=dict(color=PALETTE[:len(mood_df)], line=dict(width=0)),
            text=mood_df["amount"].apply(lambda x: f"₹{x:,.0f}"),
            textposition="outside",
            textfont=dict(size=9, color="#686E7D"),
        ))
        fig2.update_layout(
            **BASE_LAYOUT,
            xaxis=dict(showgrid=False, tickfont=dict(size=9), linecolor="#262730", tickcolor="#262730"),
            yaxis=dict(showgrid=True, gridcolor="#1A1C24", tickfont=dict(size=9), tickprefix="₹"),
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown("<p style='color:#555B6E;font-size:0.85rem;padding:1.5rem 0;'>No mood data for this period.</p>", unsafe_allow_html=True)

# ── TRANSACTION LEDGER ─────────────────────────────────────────
st.markdown(
    "<p style='font-size:0.68rem;letter-spacing:0.1em;color:#555B6E;text-transform:uppercase;font-weight:600;margin-top:1.6rem;margin-bottom:0.75rem;'>Recent Transactions</p>",
    unsafe_allow_html=True,
)

G  = "display:grid;grid-template-columns:80px 1fr 90px 80px 110px;gap:0.5rem;align-items:center;"
HS = "font-size:0.65rem;letter-spacing:0.08em;color:#555B6E;text-transform:uppercase;font-weight:600;"

if not df.empty:
    recent = df.head(15).copy()
    recent["date_fmt"]   = pd.to_datetime(recent["date"]).dt.strftime("%b %d")
    recent["mood_clean"] = (
        recent["mood"].str.replace(r'[^\w\s]', '', regex=True).str.strip()
        if "mood" in recent.columns else "—"
    )

    parts = []
    parts.append('<div style="border:1px solid #31333F;border-radius:6px;background:#0E1015;overflow:hidden;">')
    parts.append('<div style="' + G + 'padding:0.5rem 1rem;background:#16181E;border-bottom:1px solid #262730;">')
    for col in ["Date", "Description", "Category", "Amount", "State"]:
        parts.append('<span style="' + HS + '">' + col + '</span>')
    parts.append('</div>')
    for _, r in recent.iterrows():
        desc = str(r.get("description", "—"))[:28] or "—"
        cat  = str(r.get("category", "—"))
        mood = str(r["mood_clean"])
        dstr = str(r["date_fmt"])
        amt  = f"{r['amount']:,.0f}"
        parts.append('<div style="' + G + 'padding:0.65rem 1rem;border-bottom:1px solid #1A1C24;">')
        parts.append('<span style="font-size:0.77rem;color:#686E7D;">' + dstr + '</span>')
        parts.append('<span style="font-size:0.82rem;color:#C8CDD8;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' + desc + '</span>')
        parts.append('<span style="font-size:0.71rem;background:#1E2029;border:1px solid #31333F;border-radius:4px;padding:0.12rem 0.4rem;color:#9EA4B0;font-family:monospace;display:inline-block;">' + cat + '</span>')
        parts.append('<span style="font-size:0.88rem;color:#FFFFFF;font-weight:700;letter-spacing:-0.02em;">\u20b9' + amt + '</span>')
        parts.append('<span style="font-size:0.75rem;color:#686E7D;">' + mood + '</span>')
        parts.append('</div>')
    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)

else:
    st.markdown(
        '<div style="border:1px solid #31333F;border-radius:6px;padding:1.1rem 1.3rem;background:#0E1015;">' +
        '<p style="margin:0;color:#555B6E;font-size:0.85rem;">No transactions logged for this period.</p>' +
        '</div>',
        unsafe_allow_html=True,
    )
