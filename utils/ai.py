import google.generativeai as genai
import streamlit as st
import os

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

def get_weekly_coach(df_summary: str, mood_pattern: str) -> str:
    """Generate a personalised weekly budget coaching message."""
    prompt = f"""
You are a friendly, empathetic personal finance coach for an Indian user.

Here is their spending summary for this week:
{df_summary}

Their mood pattern while spending:
{mood_pattern}

Give a short, warm, actionable coaching message (4-5 lines max). 
- Start with one positive observation.
- Point out one spending pattern to watch.
- End with one specific, easy tip they can act on today.
- Use Indian context (₹, Swiggy, Zomato, UPI, etc.) where relevant.
- Do NOT use bullet points. Write naturally like a mentor texting them.
"""
    response = model.generate_content(prompt)
    return response.text

def explain_overspend(category: str, amount: float, avg: float, mood: str) -> str:
    """Explain why a category overspend happened and what to do."""
    prompt = f"""
You are a personal finance coach. A user overspent on {category} this month.
- They spent: ₹{amount:.0f}
- Their usual average: ₹{avg:.0f}
- Their common mood while spending on this: {mood}

In 3 short sentences:
1. Acknowledge the overspend without judgment.
2. Connect it to their mood pattern if relevant.
3. Give one practical fix for next month.
Keep it conversational and Indian-context aware.
"""
    response = model.generate_content(prompt)
    return response.text

def flag_impulse_buy(description: str, amount: float, category: str) -> str:
    """Check if a purchase looks like an impulse buy and return a gentle warning."""
    prompt = f"""
A user just logged this expense:
- Item: {description}
- Amount: ₹{amount:.0f}
- Category: {category}

In ONE short sentence, gently ask if this was planned or an impulse purchase.
If the amount seems high for the category or the description sounds impulsive 
(food delivery late night, gaming, entertainment on weekday), add a soft nudge.
Otherwise just say "Logged! Good job tracking." Keep it under 20 words.
"""
    response = model.generate_content(prompt)
    return response.text

def generate_challenge_motivation(category: str, streak_days: int, target_days: int) -> str:
    """Generate a motivational message for an active challenge."""
    prompt = f"""
A user is on a no-spend challenge for {category}.
- Current streak: {streak_days} days
- Target: {target_days} days

Write one short, punchy motivational line (max 15 words). 
Make it fun, energetic, and specific to their streak progress.
"""
    response = model.generate_content(prompt)
    return response.text
