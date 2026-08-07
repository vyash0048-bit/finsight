import os
import sys

import streamlit as st

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if backend_path not in sys.path:
    sys.path.append(backend_path)

from styles import PREMIUM_CSS

st.set_page_config(page_title="Watchlist | FinSight", layout="wide")
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

st.title("⭐ Watchlist")

if "watchlist" not in st.session_state:
    st.session_state["watchlist"] = ["AAPL", "MSFT", "TSLA"]

new_ticker = st.text_input("Add Ticker")
if st.button("Add"):
    if new_ticker and new_ticker.upper() not in st.session_state["watchlist"]:
        st.session_state["watchlist"].append(new_ticker.upper())

for t in st.session_state["watchlist"]:
    st.markdown(f"### {t}")
    if st.button(f"Analyze {t}", key=f"analyze_{t}"):
        st.info(f"Go to the Dashboard to run a full Swarm analysis on {t}.")
