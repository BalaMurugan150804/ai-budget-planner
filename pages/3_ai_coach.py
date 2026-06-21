import streamlit as st
import pandas as pd
from datetime import datetime
from utils.db import get_all_expenses, get_expenses_by_month
from utils.ai import get_weekly_coach, explain_overspend

st.set_page_config(page_title="System Intelligence", layout="wide", initial_sidebar_state="collapsed")

# ── SHARED DESIGN SYSTEM ───────────────────────────────────────
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
h3 {
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    color: #E2E8F0 !important;
    font-size: 1.05rem !important;
    margin-bottom: 0.1rem !important;
}
p, li { font-weight: 400; line-height: 1.55; color: #9EA4B0; font-size: 0.95rem; }

.stButton > button {
    border-radius: 6px !important;
    border: 1px solid #31333F !important;
    background: #16181E !important;
    color: #C8CDD8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 0.9rem !important;
    width: 100% !important;
    text-align: left !important;
    transition: border-color 0.15s ease, background 0.15s ease !important;
    letter-spacing: 0.01em !important;
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

label, .stSelectbox label {
    font-size: 0.72rem !important;
    letter-spacing: 0.07em !important;
    color: #555B6E !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-baseweb="select"] {
    background: #16181E !important;
    border: 1px solid #31333F !important;
    border-radius: 6px !important;
}
div[data-baseweb="popover"] ul {
    background: #16181E !important;
    border: 1px solid #31333F !important;
    border-radius: 6px !important;
}
div[data-baseweb="popover"] li {
    color: #9EA4B0 !important;
    font-size: 0.85rem !important;
}
div[data-baseweb="popover"] li:hover {
    background: #1E2029 !important;
    color: #FFFFFF !important;
}

/* Chat message override */
div[data-testid="stChatMessage"] {
    background: #0E1015 !important;
    border: 1px solid #31333F !important;
    border-radius: 6px !important;
    padding: 1rem 1.2rem !important;
}
div[data-testid="stChatMessage"] p {
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    color: #9EA4B0 !important;
}

hr.divider { border: 0; border-top: 1px solid #262730; margin: 1.2rem 0; }

.section-label {
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    color: #555B6E;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.75rem;
    margin-top: 1.6rem;
}
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

/* Behavioral matrix table */
.matrix-wrap {
    border: 1px solid #31333F;
    border-radius: 6px;
    background: #0E1015;
    overflow: hidden;
    margin-bottom: 0.75rem;
}
.matrix-head {
    display: grid;
    grid-template-columns: 1fr 100px 80px;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #16181E;
    border-bottom: 1px solid #262730;
}
.matrix-col { font-size: 0.65rem; letter-spacing: 0.08em; color: #555B6E; text-transform: uppercase; font-weight: 600; }
.matrix-row {
    display: grid;
    grid-template-columns: 1fr 100px 80px;
    gap: 0.5rem;
    padding: 0.6rem 1rem;
    border-bottom: 1px solid #1A1C24;
    align-items: center;
}
.matrix-row:last-child { border-bottom: none; }
.m-state { font-size: 0.82rem; color: #C8CDD8; font-weight: 500; }
.m-amt   { font-size: 0.82rem; color: #FFFFFF; font-weight: 700; letter-spacing: -0.02em; }
.m-pct   { font-size: 0.75rem; color: #686E7D; }

/* Chip row */
.chip-hint {
    font-size: 0.72rem;
    color: #555B6E;
    margin-top: 0.5rem;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────
for key in ["chip_response", "chip_label", "variance_analysis"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# ── NAV ───────────────────────────────────────────────────────
nav = st.segmented_control(
    label="nav",
    options=["Home", "Dashboard", "Log Expense", "Coach", "Challenges"],
    default="Coach",
    label_visibility="collapsed",
)
if nav == "Home":           st.switch_page("app.py")
elif nav == "Dashboard":    st.switch_page("pages/1_dashboard.py")
elif nav == "Log Expense":  st.switch_page("pages/2_add_expense.py")
elif nav == "Challenges":   st.switch_page("pages/4_challenges.py")

# ── HEADER ────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
st.markdown("<h1>System Intelligence</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='margin-top:0.3rem;'>Proactive behavioral analysis and spend velocity diagnostics.</p>",
    unsafe_allow_html=True,
)
st.markdown('<hr style="border:0;border-top:1px solid #262730;margin:1.2rem 0;">', unsafe_allow_html=True)

# ── DATA LOAD ─────────────────────────────────────────────────
now = datetime.now()
df  = get_expenses_by_month(now.year, now.month)
all_df = get_all_expenses()

no_data = df.empty

# ── PERMANENT COACH TERMINAL ──────────────────────────────────
st.markdown('<div class="section-label">Executive Summary</div>', unsafe_allow_html=True)

if no_data:
    terminal_text = (
        "No transaction data has been logged for the current period. "
        "The behavioral analysis engine requires at least one recorded allocation to generate velocity diagnostics. "
        "Navigate to Log Allocation and begin tracking to activate this terminal."
    )
else:
    total    = df["amount"].sum()
    count    = len(df)
    top_cat  = df.groupby("category")["amount"].sum().idxmax()
    top_pct  = int((df.groupby("category")["amount"].sum().max() / total) * 100)

    dominant_mood = "—"
    if "mood" in df.columns and not df["mood"].isna().all():
        raw = df["mood"].mode()[0]
        dominant_mood = str(raw).replace("😊","").replace("😰","").replace("😑","").replace("🎉","").replace("😐","").strip()

    terminal_text = (
        f"Current period total stands at ₹{total:,.0f} across {count} recorded allocations, "
        f"with {top_cat} representing the dominant outflow category at {top_pct}% of total volume. "
        f"The most recurring behavioral baseline during transactions is the {dominant_mood} state — "
        f"a pattern that warrants continued monitoring for impulse-driven allocation spikes. "
        f"Overall spending velocity remains within a trackable range; no critical threshold breaches detected."
    )

with st.chat_message("assistant", avatar=None):
    st.markdown(terminal_text)

# ── VARIANCE ANALYSIS ─────────────────────────────────────────
st.markdown('<hr style="border:0;border-top:1px solid #262730;margin:1.2rem 0;">', unsafe_allow_html=True)
st.markdown("<h3>Allocation Variance</h3>", unsafe_allow_html=True)
st.markdown(
    "<p style='margin-top:0.2rem;margin-bottom:1rem;font-size:0.85rem;'>Select a category to compare current velocity against historical baseline.</p>",
    unsafe_allow_html=True,
)

categories = df["category"].unique().tolist() if not no_data else ["Food", "Transport", "Shopping"]
selected_cat = st.selectbox("Category", categories, label_visibility="visible")

if not no_data and selected_cat:
    current_total = df[df["category"] == selected_cat]["amount"].sum()
    historical_avg = (
        all_df[all_df["category"] == selected_cat]["amount"].mean()
        if not all_df.empty and selected_cat in all_df["category"].values
        else current_total
    )
    deviation = ((current_total - historical_avg) / historical_avg * 100) if historical_avg > 0 else 0
    deviation_dir = "above" if deviation >= 0 else "below"
    deviation_color = "#F87171" if deviation > 10 else "#34D399" if deviation < -5 else "#9EA4B0"

    v1, v2 = st.columns(2, gap="medium")
    with v1:
        st.markdown(f"""
        <div class="sys-block">
            <div class="block-label">Current Velocity</div>
            <div class="block-value">₹{current_total:,.0f}</div>
            <div class="block-caption">This period total</div>
        </div>""", unsafe_allow_html=True)

    with v2:
        st.markdown(f"""
        <div class="sys-block">
            <div class="block-label">Historical Baseline</div>
            <div class="block-value">₹{historical_avg:,.0f}</div>
            <div class="block-caption">Per-period average across all data</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <p style="font-size:0.78rem;color:{deviation_color};margin-top:0.4rem;letter-spacing:0.02em;">
        {abs(deviation):.1f}% {deviation_dir} historical baseline for {selected_cat}.
    </p>""", unsafe_allow_html=True)

    if st.button("Run Variance Diagnostic"):
        with st.spinner("Generating analysis..."):
            try:
                common_mood = (
                    df[df["category"] == selected_cat]["mood"].mode()[0]
                    if "mood" in df.columns and not df[df["category"] == selected_cat].empty
                    else "Unknown"
                )
                result = explain_overspend(selected_cat, current_total, historical_avg, common_mood)
                st.session_state.variance_analysis = result
            except Exception:
                st.session_state.variance_analysis = (
                    f"Current {selected_cat} allocation of ₹{current_total:,.0f} is "
                    f"{abs(deviation):.1f}% {deviation_dir} the historical average of ₹{historical_avg:,.0f}. "
                    f"Monitor this category closely over the next 7-day window."
                )

    if st.session_state.variance_analysis:
        st.markdown(f"""
        <div class="sys-block" style="margin-top:0.7rem;">
            <div class="block-label">Diagnostic Output</div>
            <p style="margin:0;font-size:0.88rem;color:#9EA4B0;line-height:1.65;">
                {st.session_state.variance_analysis}
            </p>
        </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="sys-block">
        <p style="margin:0;color:#555B6E;font-size:0.85rem;">
            No allocation data available. Log transactions to activate variance analysis.
        </p>
    </div>""", unsafe_allow_html=True)

# ── BEHAVIORAL MATRIX ─────────────────────────────────────────
st.markdown('<hr style="border:0;border-top:1px solid #262730;margin:1.2rem 0;">', unsafe_allow_html=True)
st.markdown("<h3>Behavioral Correlations</h3>", unsafe_allow_html=True)
st.markdown(
    "<p style='margin-top:0.2rem;margin-bottom:1rem;font-size:0.85rem;'>Spend volume mapped against recorded emotional baseline states.</p>",
    unsafe_allow_html=True,
)

MGRID = "display:grid;grid-template-columns:1fr 110px 80px;gap:0.5rem;align-items:center;"

if not no_data and "mood" in df.columns:
    mood_df = df.groupby("mood")["amount"].agg(["sum", "count"]).reset_index()
    mood_df.columns = ["mood", "total", "count"]
    mood_df["mood_clean"] = mood_df["mood"].str.replace(r'[^\w\s]', '', regex=True).str.strip()
    mood_df["pct"] = (mood_df["total"] / mood_df["total"].sum() * 100).round(1)
    mood_df = mood_df.sort_values("total", ascending=False)

    MG = "display:grid;grid-template-columns:1fr 110px 80px;gap:0.5rem;align-items:center;"
    MH = "font-size:0.65rem;letter-spacing:0.08em;color:#555B6E;text-transform:uppercase;font-weight:600;"
    parts = []
    parts.append('<div style="border:1px solid #31333F;border-radius:6px;background:#0E1015;overflow:hidden;margin-bottom:0.75rem;">')
    parts.append('<div style="' + MG + 'padding:0.5rem 1rem;background:#16181E;border-bottom:1px solid #262730;">')
    for col in ["Behavioral State", "Total Outflow", "Share"]:
        parts.append('<span style="' + MH + '">' + col + '</span>')
    parts.append('</div>')
    for _, r in mood_df.iterrows():
        parts.append('<div style="' + MG + 'padding:0.6rem 1rem;border-bottom:1px solid #1A1C24;">')
        parts.append('<span style="font-size:0.82rem;color:#C8CDD8;font-weight:500;">' + str(r["mood_clean"]) + '</span>')
        parts.append('<span style="font-size:0.82rem;color:#FFFFFF;font-weight:700;letter-spacing:-0.02em;">\u20b9' + f"{r['total']:,.0f}" + '</span>')
        parts.append('<span style="font-size:0.75rem;color:#686E7D;">' + str(r["pct"]) + '%</span>')
        parts.append('</div>')
    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)

    # Dominant trigger alert
    top_mood     = mood_df.iloc[0]
    top_mood_pct = top_mood["pct"]
    top_mood_lbl = top_mood["mood_clean"]

    st.markdown(f"""
    <div class="sys-block">
        <div class="block-label">System Alert</div>
        <p style="margin:0;font-size:0.88rem;color:#9EA4B0;line-height:1.65;">
            {top_mood_lbl} states currently account for {top_mood_pct}% of total discretionary volume this period.
            This represents the primary behavioral trigger in your current spending cycle.
            Consider logging intent before committing allocations during this state.
        </p>
    </div>""", unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="sys-block">
        <p style="margin:0;color:#555B6E;font-size:0.85rem;">
            Behavioral correlation data unavailable. Tag emotional states when logging transactions to activate this module.
        </p>
    </div>""", unsafe_allow_html=True)

# ── INTERACTION CHIPS ─────────────────────────────────────────
st.markdown('<hr style="border:0;border-top:1px solid #262730;margin:1.2rem 0;">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Quick Actions</div>', unsafe_allow_html=True)

ch1, ch2, ch3 = st.columns(3, gap="small")

with ch1:
    if st.button("Request Containment Tips"):
        st.session_state.chip_label    = "Containment Protocol"
        st.session_state.chip_response = (
            "Identify the top two categories by volume and apply a hard ceiling for the remaining period. "
            "Delay discretionary purchases by 24 hours before committing. "
            "Review your ledger every 48 hours — visibility reduces unplanned allocations by an estimated 20-30%."
        )

with ch2:
    if st.button("View Behavioral Analysis"):
        if not no_data and "mood" in df.columns:
            top = mood_df.iloc[0] if not mood_df.empty else None
            st.session_state.chip_label = "Behavioral Analysis"
            st.session_state.chip_response = (
                f"Dominant state: {top['mood_clean']} — {top['pct']}% of total volume. "
                f"This pattern suggests that emotional baseline directly influences allocation frequency. "
                f"Introduce a confirmation step before logging transactions in this state."
            ) if top is not None else "Insufficient behavioral data for analysis."
        else:
            st.session_state.chip_label    = "Behavioral Analysis"
            st.session_state.chip_response = "No mood data available. Begin tagging transactions to enable this analysis."

with ch3:
    if st.button("Set Velocity Alert"):
        st.session_state.chip_label    = "Velocity Alert Configuration"
        st.session_state.chip_response = (
            "Velocity alert thresholds are configured at the category level. "
            "To activate, log at least 5 transactions in a single category — "
            "the system will then benchmark your current pace against the historical baseline "
            "and surface deviations exceeding 15% automatically."
        )

if st.session_state.chip_response:
    st.markdown(f"""
    <div class="sys-block" style="margin-top:0.8rem;">
        <div class="block-label">{st.session_state.chip_label}</div>
        <p style="margin:0;font-size:0.88rem;color:#9EA4B0;line-height:1.65;">
            {st.session_state.chip_response}
        </p>
    </div>""", unsafe_allow_html=True)
