import streamlit as st
import requests
from components.style import inject_custom_css

st.set_page_config(page_title="FinSight AI", page_icon="✨", layout="wide")
inject_custom_css()

st.title("✨ Welcome to FinSight AI")
st.markdown("""
### Your Personal Autonomous Financial Analyst.
FinSight uses a team of specialized AI agents to gather market data, read the latest news, analyze the fundamentals, and deliver institutional-grade investment reports directly to you.

Select a page from the sidebar to view your dashboard, manage your portfolio, or generate AI investment reports.
""")

st.markdown("---")

# Check Backend Health
st.subheader("System Status")
try:
    # Use api:8000 since we're inside the docker network
    response = requests.get("http://api:8000/api/v1/health", timeout=5)
    if response.status_code == 200:
        st.success("✅ **FinSight API** is online and agents are standing by.")
    else:
        st.warning("⚠️ Backend API responded with an error.")
except requests.exceptions.ConnectionError:
    st.error("❌ Could not connect to the Backend API. Ensure the 'api' service is running.")
