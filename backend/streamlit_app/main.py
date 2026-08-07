import streamlit as st
import os

# Load env variables globally before importing backend modules
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, val = line.split("=", 1)
                os.environ[key.strip().upper()] = val.strip().strip('"').strip("'")

from styles import PREMIUM_CSS

st.set_page_config(
    page_title="FinSight | AI Swarm",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

st.title("✨ FinSight AI Swarm")
st.markdown("### Welcome to your Autonomous Research Terminal.")
st.write("FinSight deploys a decentralized swarm of AI Agents (News, Technical, Fundamental, Macro, Risk, and Debate) to synthesize real-time market data into actionable insights.")

st.info("👈 Please select a module from the sidebar to begin.")

# We can render some nice decorative metrics on the home page
cols = st.columns(3)
with cols[0]:
    st.metric(label="Active Agents", value="6", delta="Online")
with cols[1]:
    st.metric(label="Data Sources", value="Yahoo Finance", delta="Live")
with cols[2]:
    st.metric(label="LLM Core", value="Gemini Flash Lite", delta="Active")
