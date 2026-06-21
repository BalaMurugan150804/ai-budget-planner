import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

CATEGORY_COLORS = {
    "Food": "#EF9F27",
    "Transport": "#5DCAA5",
    "Entertainment": "#AFA9EC",
    "Shopping": "#F0997B",
    "Health": "#85B7EB",
    "Rent": "#D4537E",
    "Education": "#97C459",
    "Other": "#B4B2A9",
}

def pie_chart(df):
    if df.empty:
        return None
    grouped = df.groupby("category")["amount"].sum().reset_index()
    fig = px.pie(
        grouped, values="amount", names="category",
        color="category", color_discrete_map=CATEGORY_COLORS,
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        showlegend=False, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig

def bar_trend(df_summary):
    if df_summary.empty:
        return None
    fig = px.bar(
        df_summary, x="month", y="total",
        color_discrete_sequence=["#534AB7"],
        labels={"month": "Month", "total": "Total Spent (₹)"},
    )
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#E5E5E5"),
    )
    return fig

def mood_spend_bar(df):
    if df.empty or "mood" not in df.columns:
        return None
    mood_df = df.groupby("mood")["amount"].sum().reset_index()
    mood_colors = {
        "Happy 😊": "#5DCAA5", "Stressed 😰": "#E24B4A",
        "Bored 😑": "#EF9F27", "Celebratory 🎉": "#AFA9EC",
        "Neutral 😐": "#B4B2A9",
    }
    fig = px.bar(
        mood_df, x="mood", y="amount",
        color="mood", color_discrete_map=mood_colors,
        labels={"mood": "Mood", "amount": "Total Spent (₹)"},
    )
    fig.update_layout(
        showlegend=False, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig

def spend_heatmap(df):
    """Calendar-style daily spend heatmap."""
    if df.empty:
        return None
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    daily = df.groupby("date")["amount"].sum().reset_index()
    daily["day"] = daily["date"].dt.day_name()
    daily["week"] = daily["date"].dt.isocalendar().week.astype(str)
    fig = px.density_heatmap(
        daily, x="week", y="day", z="amount",
        color_continuous_scale=["#E1F5EE", "#0F6E56"],
        labels={"week": "Week", "day": "Day", "amount": "Spent (₹)"},
    )
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
