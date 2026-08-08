import os
import requests

import streamlit as st

from styles import PREMIUM_CSS

st.set_page_config(page_title="Dashboard | FinSight", layout="wide")
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)


API_HOST = os.getenv("API_HOST")
if API_HOST:
    # Render public URL format
    API_URL = f"https://{API_HOST}.onrender.com"
else:
    # Local fallback
    API_URL = "http://localhost:8000"

st.title("📊 Real-Time Swarm Research")

if "report_cache" not in st.session_state:
    st.session_state["report_cache"] = {}

ticker = st.text_input("Enter Ticker Symbol (e.g. AAPL, TSLA)", "").upper()

if st.button("🚀 Generate AI Report"):
    if not ticker:
        st.warning("Please enter a ticker.")
    elif ticker in st.session_state["report_cache"]:
        st.success("Loaded from cache!")
    else:
        with st.spinner(f"Swarm is actively analyzing {ticker}... this usually takes 15-30 seconds."):
            try:
                response = requests.post(
                    f"{API_URL}/research/report", 
                    json={"ticker": ticker},
                    timeout=90
                )
                if response.status_code == 200:
                    st.session_state["report_cache"][ticker] = response.json()
                    st.success(f"Analysis Complete for {ticker}!")
                else:
                    st.error(f"API Error: {response.text}")
            except Exception as e:
                st.error(f"Network error: {e!s}")

# Render Report if it exists in cache
if ticker and ticker in st.session_state["report_cache"]:
    res = st.session_state["report_cache"][ticker]
    report = res["report"]
    
    st.markdown("---")
    st.header(f"🏆 Final Report: {ticker}")
    
    if report["status"] == "success":
        data = report["data"]
        
        # Recommendation Banner
        rec = data.get("final_recommendation", "UNKNOWN").upper()
        color = "green" if rec == "BUY" else "red" if rec == "SELL" else "orange"
        st.markdown(f"<h3 style='color: {color};'>Recommendation: {rec}</h3>", unsafe_allow_html=True)
        
        st.markdown("#### Executive Summary")
        st.write(data.get("executive_summary", ""))
        
        st.markdown("#### Key Drivers")
        for driver in data.get("key_drivers", []):
            st.markdown(f"- {driver}")
    else:
        st.error(f"Report Synthesis Failed: {report.get('summary', 'Unknown error')}")
        
    st.markdown("---")
    st.subheader("🤖 Swarm Agent Breakdowns")
    
    # 2 rows of 3 columns
    agents = list(res["findings"].items())
    for i in range(0, len(agents), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(agents):
                agent_name, agent_data = agents[i + j]
                with cols[j]:
                    status = "🟢" if agent_data["status"] == "success" else "🔴"
                    st.markdown(f"**{agent_name.capitalize()} Agent** {status}")
                    
                    if agent_data["status"] == "success":
                        d = agent_data["data"]
                        # Just render the top keys
                        for k, v in list(d.items())[:3]:
                            st.caption(f"{k.replace('_', ' ').capitalize()}: {v}")
                    else:
                        st.caption("Error retrieving data")
