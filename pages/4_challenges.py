import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from utils.db import add_challenge, get_active_challenges, get_expenses_by_month
from utils.ai import generate_challenge_motivation

st.set_page_config(page_title="Active Objectives", layout="wide", initial_sidebar_state="collapsed")

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

label, .stSelectbox label, .stNumberInput label, .stSlider label {
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
div[data-baseweb="popover"] li { color: #9EA4B0 !important; font-size: 0.85rem !important; }
div[data-baseweb="popover"] li:hover { background: #1E2029 !important; color: #FFFFFF !important; }

div[data-testid="stNumberInput"] input {
    background: #16181E !important;
    border: 1px solid #31333F !important;
    border-radius: 6px !important;
    color: #C8CDD8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
}
div[data-testid="stNumberInput"] button {
    border: 1px solid #31333F !important;
    background: #16181E !important;
    color: #686E7D !important;
    border-radius: 4px !important;
}

/* Progress bar */
.stProgress > div > div {
    background: #1E2029 !important;
    border-radius: 2px !important;
    height: 3px !important;
}
.stProgress > div > div > div {
    background: #4C6EF5 !important;
    border-radius: 2px !important;
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
    font-size: 1.35rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.03em;
    line-height: 1.2;
    margin-bottom: 0.25rem;
}
.block-caption { font-size: 0.75rem; color: #555B6E; font-weight: 400; }

/* Challenge card */
.challenge-name {
    font-size: 0.92rem;
    font-weight: 600;
    color: #E2E8F0;
    margin-bottom: 0.55rem;
    letter-spacing: -0.01em;
}
.challenge-status {
    font-size: 0.75rem;
    color: #686E7D;
    margin-top: 0.4rem;
    letter-spacing: 0.01em;
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
    grid-template-columns: 1fr 75px 95px 75px;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #16181E;
    border-bottom: 1px solid #262730;
}
.ledger-col { font-size: 0.65rem; letter-spacing: 0.08em; color: #555B6E; text-transform: uppercase; font-weight: 600; }
.ledger-row {
    display: grid;
    grid-template-columns: 1fr 75px 95px 75px;
    gap: 0.5rem;
    padding: 0.6rem 1rem;
    border-bottom: 1px solid #1A1C24;
    align-items: center;
}
.ledger-row:last-child { border-bottom: none; }
.l-desc { font-size: 0.82rem; color: #C8CDD8; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.l-amt  { font-size: 0.82rem; color: #FFFFFF; font-weight: 700; letter-spacing: -0.02em; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────
if "obj_confirmed"   not in st.session_state: st.session_state.obj_confirmed   = False
if "obj_name"        not in st.session_state: st.session_state.obj_name        = ""
if "regret_flags"    not in st.session_state: st.session_state.regret_flags    = {}
if "motivation_msgs" not in st.session_state: st.session_state.motivation_msgs = {}
if "suggestion_activated" not in st.session_state: st.session_state.suggestion_activated = False

# ── NAV ───────────────────────────────────────────────────────
nav = st.segmented_control(
    label="nav",
    options=["Home", "Dashboard", "Log Expense", "Coach", "Challenges"],
    default="Challenges",
    label_visibility="collapsed",
)
if nav == "Home":          st.switch_page("app.py")
elif nav == "Dashboard":   st.switch_page("pages/1_dashboard.py")
elif nav == "Log Expense": st.switch_page("pages/2_add_expense.py")
elif nav == "Coach":       st.switch_page("pages/3_ai_coach.py")

# ── HEADER ────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
st.markdown("<h1>Active Objectives</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='margin-top:0.3rem;'>Targeted containment phases and behavioral accountability reviews.</p>",
    unsafe_allow_html=True,
)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────
now = datetime.now()
df  = get_expenses_by_month(now.year, now.month)

CATEGORIES = ["Food", "Shopping", "Education", "Health", "Transport", "Entertainment", "Other"]

# Derive AI suggestion from top spend + mood
suggested_cat    = "Food"
suggested_days   = 7
suggested_reason = "No significant spend data detected yet."

if not df.empty:
    top_cat = df.groupby("category")["amount"].sum().idxmax()
    suggested_cat  = top_cat
    suggested_days = 7
    if "mood" in df.columns:
        top_mood_raw = df["mood"].mode()[0] if not df["mood"].isna().all() else "Unknown"
        top_mood     = str(top_mood_raw).replace("😊","").replace("😰","").replace("😑","").replace("🎉","").replace("😐","").strip()
        suggested_reason = (
            f"{top_cat} is your highest-spend category this period. "
            f"Dominant behavioral state during {top_cat} allocations: {top_mood}. "
            f"A 7-day containment phase on {top_cat} is recommended."
        )
    else:
        suggested_reason = (
            f"{top_cat} is your highest outflow category this period. "
            f"A 7-day containment phase is recommended to establish a new baseline."
        )

# ── OBJECTIVE ENGINE ──────────────────────────────────────────
st.markdown('<div class="section-label">Objective Configuration</div>', unsafe_allow_html=True)

left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown("""
    <div class="sys-block">
        <div class="block-label">New Objective</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.obj_confirmed:
        st.markdown(f"""
        <div class="sys-block">
            <div class="block-label">Objective Activated</div>
            <p style="margin:0;font-size:0.88rem;color:#9EA4B0;line-height:1.65;">
                Containment phase for <strong style="color:#C8CDD8;">{st.session_state.obj_name}</strong> is now active.
                The system will track daily allocations against this objective and surface deviations automatically.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Configure another objective"):
            st.session_state.obj_confirmed = False
            st.rerun()
    else:
        with st.form("obj_form", border=False):
            cat      = st.selectbox("Category", CATEGORIES)
            target   = st.number_input("Target ceiling (₹)", min_value=100.0, step=100.0, value=1000.0)
            duration = st.number_input("Duration (days)", min_value=1, max_value=30, step=1, value=7)
            title    = st.text_input("Objective label", placeholder=f"e.g., {cat} containment — {int(duration)} days")
            submit   = st.form_submit_button("Activate Objective", use_container_width=True)

        if submit:
            label = title.strip() or f"{cat} containment — {int(duration)} days"
            add_challenge(cat, label, int(duration))
            st.session_state.obj_confirmed = True
            st.session_state.obj_name      = label
            st.rerun()

with right:
    st.markdown(f"""
    <div class="sys-block">
        <div class="block-label">Coach Suggested</div>
        <div class="block-value">{suggested_cat} — {suggested_days}d</div>
        <p style="margin:0.4rem 0 0.8rem 0;font-size:0.82rem;color:#686E7D;line-height:1.6;">
            {suggested_reason}
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.suggestion_activated:
        st.markdown("""
        <div class="sys-block">
            <p style="margin:0;font-size:0.82rem;color:#555B6E;">
                Suggestion committed to active objectives.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.button("Activate Suggestion"):
            label = f"{suggested_cat} containment — {suggested_days} days"
            add_challenge(suggested_cat, label, suggested_days)
            st.session_state.suggestion_activated = True
            st.rerun()

# ── PROGRESS HUB ──────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("<h3>Progress Tracking</h3>", unsafe_allow_html=True)
st.markdown(
    "<p style='margin-top:0.2rem;margin-bottom:1rem;font-size:0.85rem;'>Live progress against all active containment objectives.</p>",
    unsafe_allow_html=True,
)

challenges = get_active_challenges()

if challenges.empty:
    st.markdown("""
    <div class="sys-block">
        <p style="margin:0;color:#555B6E;font-size:0.85rem;">
            No active objectives. Configure one above to begin tracking.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    for _, ch in challenges.iterrows():
        start    = date.fromisoformat(ch["start_date"])
        streak   = (date.today() - start).days
        target   = int(ch["target_days"])
        progress = min(streak / target, 1.0)
        cat      = ch["category"]
        ch_id    = int(ch["id"])

        # Check spend in this category this month
        slipped = (
            not df.empty
            and cat in df["category"].values
            and df[df["category"] == cat]["amount"].sum() > 0
        )

        status_text = "Breach detected — spend recorded in this category." if slipped else "Within baseline — no allocations detected."

        with st.container():
            st.markdown(f'<div class="challenge-name">{ch["title"]}</div>', unsafe_allow_html=True)
            st.progress(progress)
            st.markdown(
                f'<div class="challenge-status">Day {streak} of {target}  &nbsp;·&nbsp;  {status_text}</div>',
                unsafe_allow_html=True,
            )

            if st.button("Request Motivation Signal", key=f"mot_{ch_id}"):
                try:
                    msg = generate_challenge_motivation(cat, streak, target)
                    msg = str(msg).strip()
                except Exception:
                    msg = f"Day {streak} of {target} — maintain the discipline. Consistency compounds."
                st.session_state.motivation_msgs[ch_id] = msg

            if ch_id in st.session_state.motivation_msgs:
                st.markdown(f"""
                <div class="sys-block" style="margin-top:0.5rem;">
                    <div class="block-label">Motivation Signal</div>
                    <p style="margin:0;font-size:0.88rem;color:#9EA4B0;line-height:1.65;">
                        {st.session_state.motivation_msgs[ch_id]}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<hr class="divider" style="margin:0.8rem 0;">', unsafe_allow_html=True)

# ── ACCOUNTABILITY REVIEW (REGRET MATRIX) ─────────────────────
st.markdown("<h3>Accountability Review</h3>", unsafe_allow_html=True)
st.markdown(
    "<p style='margin-top:0.2rem;margin-bottom:1rem;font-size:0.85rem;'>Seven-day transaction audit — assess allocation decisions against behavioral intent.</p>",
    unsafe_allow_html=True,
)

if not df.empty:
    cutoff = date.today() - timedelta(days=7)
    recent = df.copy()
    recent["date_parsed"] = pd.to_datetime(recent["date"]).dt.date
    recent = recent[recent["date_parsed"] >= cutoff].head(12).reset_index(drop=True)

    if recent.empty:
        st.markdown("""
        <div class="sys-block">
            <p style="margin:0;color:#555B6E;font-size:0.85rem;">
                No transactions in the last 7 days.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="ledger-wrap">
            <div class="ledger-head">
                <span class="ledger-col">Description</span>
                <span class="ledger-col">Amount</span>
                <span class="ledger-col">Value Added</span>
                <span class="ledger-col">Regret</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for i, row in recent.iterrows():
            desc   = str(row.get("description", "—"))[:28] or "—"
            amount = row.get("amount", 0)
            row_id = f"row_{i}_{row.get('id', i)}"

            col_desc, col_amt, col_val, col_reg = st.columns([3, 1.2, 1.5, 1.2], gap="small")

            with col_desc:
                st.markdown(
                    f"<p style='font-size:0.82rem;color:#C8CDD8;font-weight:500;margin:0.55rem 0;'>{desc}</p>",
                    unsafe_allow_html=True,
                )
            with col_amt:
                st.markdown(
                    f"<p style='font-size:0.82rem;color:#FFFFFF;font-weight:700;letter-spacing:-0.02em;margin:0.55rem 0;'>₹{amount:,.0f}</p>",
                    unsafe_allow_html=True,
                )
            with col_val:
                if st.button("Value Added", key=f"val_{row_id}"):
                    st.session_state.regret_flags[row_id] = "value"
            with col_reg:
                if st.button("Regret", key=f"reg_{row_id}"):
                    st.session_state.regret_flags[row_id] = "regret"

            if st.session_state.regret_flags.get(row_id) == "regret":
                st.markdown(f"""
                <div class="sys-block" style="margin:0.3rem 0 0.6rem 0;">
                    <p style="margin:0;font-size:0.82rem;color:#9EA4B0;line-height:1.6;">
                        System noted. The allocation of ₹{amount:,.0f} on <em>{desc}</em> has been flagged.
                        This pattern will be referenced in future behavioral state analysis to reduce recurrence.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state.regret_flags.get(row_id) == "value":
                st.markdown(f"""
                <div class="sys-block" style="margin:0.3rem 0 0.6rem 0;">
                    <p style="margin:0;font-size:0.82rem;color:#9EA4B0;line-height:1.6;">
                        Acknowledged. ₹{amount:,.0f} on <em>{desc}</em> recorded as intentional and value-positive.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<hr class="divider" style="margin:0.2rem 0;">', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="sys-block">
        <p style="margin:0;color:#555B6E;font-size:0.85rem;">
            No transaction history available. Log allocations to activate the accountability review module.
        </p>
    </div>
    """, unsafe_allow_html=True)
