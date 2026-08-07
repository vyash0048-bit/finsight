import os
import sys

import streamlit as st

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if backend_path not in sys.path:
    sys.path.append(backend_path)

from styles import PREMIUM_CSS

st.set_page_config(page_title="Reports | FinSight", layout="wide")
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

st.title("📁 Historical Reports")
st.write("Browse cached reports from this session.")

if "report_cache" not in st.session_state or not st.session_state["report_cache"]:
    st.info("No reports generated yet. Head over to the Dashboard to run an analysis.")
else:
    for ticker, res in st.session_state["report_cache"].items():
        with st.expander(f"Report: {ticker}"):
            if res["report"]["status"] == "success":
                st.markdown(res["report"]["data"].get("executive_summary", ""))
            else:
                st.error("Report generation had failed.")
