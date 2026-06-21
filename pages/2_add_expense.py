import streamlit as st
from datetime import date
from utils.db import add_expense
from utils.ai import flag_impulse_buy

st.set_page_config(page_title="Log Allocation", layout="wide", initial_sidebar_state="collapsed")

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
p, li { font-weight: 400; line-height: 1.55; color: #9EA4B0; font-size: 0.95rem; }

/* Buttons */
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

/* Nav */
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

/* All form inputs unified */
div[data-testid="stDateInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-baseweb="select"] {
    background: #16181E !important;
    border: 1px solid #31333F !important;
    border-radius: 6px !important;
    color: #C8CDD8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
}
div[data-baseweb="select"] {
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

/* Field labels */
label, .stDateInput label, .stNumberInput label,
.stTextInput label, .stSelectbox label {
    font-size: 0.72rem !important;
    letter-spacing: 0.07em !important;
    color: #555B6E !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Number input buttons */
div[data-testid="stNumberInput"] button {
    border: 1px solid #31333F !important;
    background: #16181E !important;
    color: #686E7D !important;
    border-radius: 4px !important;
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
    margin-bottom: 0.4rem;
}
.preview-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 0.3rem 0;
    border-bottom: 1px solid #1A1C24;
}
.preview-row:last-child { border-bottom: none; }
.preview-key { font-size: 0.75rem; color: #555B6E; }
.preview-val { font-size: 0.82rem; color: #C8CDD8; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────
if "log_confirmed" not in st.session_state:
    st.session_state.log_confirmed = False
if "ai_nudge" not in st.session_state:
    st.session_state.ai_nudge = ""

# ── NAV ───────────────────────────────────────────────────────
nav = st.segmented_control(
    label="nav",
    options=["Home", "Dashboard", "Log Expense", "Coach", "Challenges"],
    default="Log Expense",
    label_visibility="collapsed",
)
if nav == "Home":
    st.switch_page("app.py")
elif nav == "Dashboard":
    st.switch_page("pages/1_dashboard.py")
elif nav == "Coach":
    st.switch_page("pages/3_ai_coach.py")
elif nav == "Challenges":
    st.switch_page("pages/4_challenges.py")

# ── HEADER ────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
st.markdown("<h1>Log Allocation</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='margin-top:0.3rem;'>Record a new transaction to update active velocity baselines and behavioral states.</p>",
    unsafe_allow_html=True,
)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── CONFIRMATION STATE ────────────────────────────────────────
if st.session_state.log_confirmed:
    st.markdown(f"""
    <div class="sys-block">
        <div class="block-label">Transaction Recorded</div>
        <p style="margin:0;font-size:0.88rem;color:#9EA4B0;line-height:1.65;">
            {st.session_state.ai_nudge}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    if st.button("Log another transaction"):
        st.session_state.log_confirmed = False
        st.session_state.ai_nudge = ""
        st.rerun()
    st.stop()

# ── FORM ──────────────────────────────────────────────────────
CATEGORIES   = ["Food", "Shopping", "Education", "Health", "Transport", "Entertainment", "Other"]
PAYMENT_MODES = ["UPI", "Cash", "Card", "Net Banking"]
MOODS        = ["Balanced", "Stressed", "Motivated", "Passive", "Celebratory"]

st.markdown('<div class="section-label">Transaction Fields</div>', unsafe_allow_html=True)

with st.form("log_form", border=False):
    exp_date    = st.date_input("Transaction Date", value=date.today())
    amount      = st.number_input("Numeric Value (₹)", min_value=1.0, step=10.0, value=100.0)
    category    = st.selectbox("Category Assignment", CATEGORIES)
    description = st.text_input("Ledger Line Note", placeholder="e.g., Grocery replenishment")
    payment     = st.selectbox("Settlement Mode", PAYMENT_MODES)
    mood        = st.selectbox("Behavioral Baseline State", MOODS)

    # ── MICRO-PREVIEW ─────────────────────────────────────────
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sys-block">
        <div class="block-label">Entry Preview</div>
        <div class="preview-row">
            <span class="preview-key">Date</span>
            <span class="preview-val">{exp_date.strftime('%b %d, %Y')}</span>
        </div>
        <div class="preview-row">
            <span class="preview-key">Amount</span>
            <span class="preview-val">₹{amount:,.0f}</span>
        </div>
        <div class="preview-row">
            <span class="preview-key">Category</span>
            <span class="preview-val">{category}</span>
        </div>
        <div class="preview-row">
            <span class="preview-key">Note</span>
            <span class="preview-val">{description if description else '—'}</span>
        </div>
        <div class="preview-row">
            <span class="preview-key">Settlement</span>
            <span class="preview-val">{payment}</span>
        </div>
        <div class="preview-row">
            <span class="preview-key">State</span>
            <span class="preview-val">{mood}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Commit Transaction", use_container_width=True)

# ── SUBMISSION LOGIC ──────────────────────────────────────────
if submitted:
    # Map UI mood labels back to DB format
    mood_map = {
        "Balanced":    "Neutral 😐",
        "Stressed":    "Stressed 😰",
        "Motivated":   "Happy 😊",
        "Passive":     "Neutral 😐",
        "Celebratory": "Celebratory 🎉",
    }
    add_expense(
        date=exp_date.isoformat(),
        amount=amount,
        category=category,
        description=description,
        mood=mood_map.get(mood, mood),
        payment_mode=payment,
    )

    try:
        nudge = flag_impulse_buy(description or category, amount, category)
        nudge = nudge.strip()
    except Exception:
        nudge = f"Transaction of ₹{amount:,.0f} under {category} has been committed to the ledger."

    st.session_state.log_confirmed = True
    st.session_state.ai_nudge = nudge
    st.rerun()
