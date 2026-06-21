import streamlit as st
from utils.db import init_db

st.set_page_config(
    page_title="Personal AI Financial Coach",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()

# ── GLOBAL STYLE INJECTION ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 4rem 2.5rem;
    max-width: 860px;
}

/* Headings */
h1 {
    font-weight: 700 !important;
    letter-spacing: -0.04em !important;
    color: #FFFFFF !important;
    font-size: 2.2rem !important;
    margin-bottom: 0.2rem !important;
    line-height: 1.15 !important;
}
h2, h3 { letter-spacing: -0.02em; color: #e2e8f0; }

/* Paragraphs / muted text */
p, li, .muted {
    font-weight: 400;
    line-height: 1.55;
    color: #9EA4B0;
    font-size: 0.95rem;
}

/* All buttons — sharp, flat, dark */
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
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    border-color: #555B6E !important;
    background: #1E2029 !important;
    color: #FFFFFF !important;
}
.stButton > button:active {
    background: #252830 !important;
}

/* Mood button active state via selected class */
.mood-active > button {
    border-color: #4F5668 !important;
    background: #1E2029 !important;
    color: #FFFFFF !important;
}

/* Segmented control / tab row */
div[data-testid="stSegmentedControl"] {
    background: #0E1015 !important;
    border: 1px solid #262730 !important;
    border-radius: 6px !important;
    padding: 3px !important;
}
div[data-testid="stSegmentedControl"] label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
    color: #686E7D !important;
    border-radius: 4px !important;
}

/* Progress bar */
.stProgress > div > div {
    background: #2A2D38 !important;
    border-radius: 2px !important;
    height: 3px !important;
}
.stProgress > div > div > div {
    background: #7C83FF !important;
    border-radius: 2px !important;
}

/* Caption text */
.stCaption, small {
    color: #555B6E !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.01em;
}

/* AI message container */
.coach-block {
    border: 1px solid #31333F;
    border-radius: 8px;
    padding: 1.1rem 1.3rem;
    background: #0E1015;
    margin-top: 0.8rem;
}
.coach-block p {
    color: #9EA4B0;
    font-size: 0.9rem;
    line-height: 1.65;
    margin: 0;
}
.coach-block .coach-label {
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    color: #555B6E;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

/* Section label */
.section-label {
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    color: #555B6E;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.75rem;
    margin-top: 1.6rem;
}

/* Stat chip */
.stat-chip {
    display: inline-block;
    background: #16181E;
    border: 1px solid #262730;
    border-radius: 6px;
    padding: 0.55rem 0.9rem;
    margin-bottom: 0.5rem;
    width: 100%;
}
.stat-chip .val {
    font-size: 1.35rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.03em;
    display: block;
}
.stat-chip .lbl {
    font-size: 0.72rem;
    color: #555B6E;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-top: 0.1rem;
    display: block;
}

hr.divider {
    border: 0;
    border-top: 1px solid #262730;
    margin: 1.2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────
if "mood" not in st.session_state:
    st.session_state.mood = None
if "ask_coach" not in st.session_state:
    st.session_state.ask_coach = False

# ── TOP NAVIGATION ─────────────────────────────────────────────
nav = st.segmented_control(
    label="nav",
    options=["Home", "Dashboard", "Log Expense", "Coach", "Challenges"],
    default="Home",
    label_visibility="collapsed",
)

if nav == "Dashboard":
    st.switch_page("pages/1_dashboard.py")
elif nav == "Log Expense":
    st.switch_page("pages/2_add_expense.py")
elif nav == "Coach":
    st.switch_page("pages/3_ai_coach.py")
elif nav == "Challenges":
    st.switch_page("pages/4_challenges.py")

# ── HEADLINE ───────────────────────────────────────────────────
st.markdown("<div style='margin-top:1.6rem'></div>", unsafe_allow_html=True)
st.markdown("<h1>Personal AI Budget Planner</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='margin-top:0.3rem;'>An intelligent, behavior-focused monetary engine tracking spending velocity and emotional states.</p>",
    unsafe_allow_html=True,
)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── MOOD MATRIX ────────────────────────────────────────────────
st.markdown('<div class="section-label">Current State</div>', unsafe_allow_html=True)

MOODS = ["Balanced", "Anxious", "Motivated", "Passive"]

MOOD_RESPONSES = {
    "Balanced": (
        "System stable. Your recent spending patterns reflect a controlled allocation across primary categories. "
        "No anomalies detected in the last 7-day window. Maintain current behavior — you are tracking well against your monthly target."
    ),
    "Anxious": (
        "Acknowledged. Financial anxiety often correlates with information gaps rather than actual deficit. "
        "Your current logged data does not indicate a critical shortfall. "
        "Consider reviewing your dashboard once — clarity tends to reduce perceived risk significantly. "
        "You are in a manageable position."
    ),
    "Motivated": (
        "High-intent state detected. This is an optimal window to configure a new savings target or initiate a no-spend challenge. "
        "Behavioral momentum compounds — actions taken now have outsized impact on your end-of-month outcome. "
        "Navigate to Challenges to activate a new constraint."
    ),
    "Passive": (
        "Passive mode noted. No immediate action required. "
        "Your most recent auto-logged entries are categorized and stored. "
        "When ready, your Coach summary is available on demand. "
        "No data has been lost — your financial state remains tracked in the background."
    ),
}

m1, m2, m3, m4 = st.columns(4, gap="small")
mood_cols = {MOODS[0]: m1, MOODS[1]: m2, MOODS[2]: m3, MOODS[3]: m4}

for label, col in mood_cols.items():
    with col:
        if st.button(label, key=f"mood_{label}"):
            st.session_state.mood = label

if st.session_state.mood:
    st.markdown(f"""
    <div class="coach-block">
        <div class="coach-label">Coach — {st.session_state.mood} Mode</div>
        <p>{MOOD_RESPONSES[st.session_state.mood]}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="coach-block">
        <div class="coach-label">Daily Briefing</div>
        <p>
            You are currently <strong style="color:#c8cdd8;">₹620 under budget</strong> for the week.<br>
            Active challenge <strong style="color:#c8cdd8;">'No Takeout Week'</strong> is at day 4 — no violations detected.<br>
            A recurring subscription of <strong style="color:#c8cdd8;">₹449</strong> is scheduled for tomorrow.
            Account balance is within a safe operating range. No intervention required.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── MICRO-TRACKING ─────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)

left, right = st.columns([1.5, 1], gap="large")

with left:
    st.markdown('<div class="section-label">Interface Controls</div>', unsafe_allow_html=True)

    if st.button("Log Daily Transaction", key="log_btn"):
        st.switch_page("pages/2_add_expense.py")

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    if st.button("Open Coach Terminal", key="coach_btn"):
        st.session_state.ask_coach = not st.session_state.ask_coach

    if st.session_state.ask_coach:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        query = st.text_input(
            label="query",
            placeholder="Enter query for Coach...",
            label_visibility="collapsed",
            key="coach_query",
        )
        if query and query != st.session_state.get("last_query", ""):
            st.session_state.last_query = query
            with st.spinner("Coach is thinking..."):
                try:
                    from utils.ai import ask_coach_question
                    from utils.db import get_expenses_by_month
                    from datetime import datetime
                    now = datetime.now()
                    df = get_expenses_by_month(now.year, now.month)
                    summary = df.groupby("category")["amount"].sum().to_string() if not df.empty else "No spend data yet"
                    st.session_state.coach_response = ask_coach_question(query, summary)
                except Exception as e:
                    st.session_state.coach_response = f"Error: {str(e)}"

        if st.session_state.get("coach_response") and st.session_state.get("last_query"):
            st.markdown(
                '<div class="coach-block" style="margin-top:0.6rem;">'
                '<div class="coach-label">Coach Response</div>'
                '<p>' + str(st.session_state.get("coach_response", "")) + '</p>'
                '</div>',
                unsafe_allow_html=True,
            )

with right:
    st.markdown('<div class="section-label">Active Target</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.82rem; color:#9EA4B0; margin-bottom:0.6rem; font-weight:500;">
        Weekend Spending Freeze
    </div>
    """, unsafe_allow_html=True)

    st.progress(0.70)
    st.caption("70% complete — 6 hours remaining in active evaluation window.")

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="stat-chip">
        <span class="val">₹1,240</span>
        <span class="lbl">Saved this session</span>
    </div>
    """, unsafe_allow_html=True)

