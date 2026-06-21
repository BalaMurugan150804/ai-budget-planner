# 💰 Personal AI Budget Planner

> A Streamlit app with Gemini-powered spending psychology analysis, mood-expense correlation, and gamified no-spend challenges.

## Features
- ➕ Log expenses with mood tagging
- 📊 Visual dashboard (pie, bar, heatmap)
- 🤖 Gemini AI coach with personalised weekly tips
- 🔍 Overspend explainer — AI tells you *why* you overspent
- 🏆 No-spend challenge mode with AI motivation
- 😬 Regret score system to learn from impulse buys

## Setup

### 1. Clone and install
```bash
pip install -r requirements.txt
```

### 2. Add your Gemini API key
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```
Get a free key at: https://aistudio.google.com/app/apikey

### 3. Run
```bash
streamlit run app.py
```

## Project structure
```
ai_budget_planner/
├── app.py                  # Entry point
├── pages/
│   ├── 1_dashboard.py      # Charts & KPIs
│   ├── 2_add_expense.py    # Log expenses + AI impulse check
│   ├── 3_ai_coach.py       # Weekly Gemini coaching
│   └── 4_challenges.py     # No-spend challenges + regret check
├── utils/
│   ├── db.py               # SQLite helpers
│   ├── ai.py               # Gemini API calls
│   └── charts.py           # Plotly chart builders
├── data/                   # SQLite DB lives here
└── requirements.txt
```

## Tech stack
- **Streamlit** — UI
- **Gemini 1.5 Flash** — AI coaching & analysis
- **SQLite + Pandas** — Data storage & processing
- **Plotly** — Interactive charts
