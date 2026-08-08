import os

import streamlit as st

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
