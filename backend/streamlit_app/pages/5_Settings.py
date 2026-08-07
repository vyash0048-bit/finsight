import os
import sys

import streamlit as st

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if backend_path not in sys.path:
    sys.path.append(backend_path)

from styles import PREMIUM_CSS

st.set_page_config(page_title="Settings | FinSight", layout="wide")
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

st.title("⚙️ Global Settings")

st.markdown("### Language Models")
model = st.selectbox("Orchestrator Model", ["gemini-3.1-flash-lite", "gemini-pro", "gemini-1.5-flash"], index=0)
st.caption("Note: Changing this requires a backend restart.")

st.markdown("### Agent Configurations")
st.slider("Orchestrator Timeout (seconds)", 10, 120, 30)

st.markdown("### Cache Management")
if st.button("Clear Report Cache"):
    if "report_cache" in st.session_state:
        st.session_state["report_cache"] = {}
    st.success("Cache cleared!")
