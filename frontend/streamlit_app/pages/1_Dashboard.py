import streamlit as st
from components.style import inject_custom_css

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
inject_custom_css()

st.title("📊 Market Dashboard")

# Mock market data for the skeleton UI phase
st.markdown("### Major Indices")
col1, col2, col3 = st.columns(3)
col1.metric("S&P 500", "5,100.25", "+1.2%")
col2.metric("NASDAQ", "16,200.50", "+1.5%")
col3.metric("10-Yr Treasury", "4.25%", "-0.05%")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Top Market News")

news_html = """
<div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;">
    <h4 style="margin: 0; color: #60a5fa;">Federal Reserve Holds Rates Steady</h4>
    <p style="margin: 5px 0 0 0; font-size: 14px; color: #cbd5e1;">The Federal Reserve announced it will maintain current interest rates, signaling confidence in the current economic trajectory.</p>
</div>
<div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #8b5cf6;">
    <h4 style="margin: 0; color: #c084fc;">Tech Sector Surges on AI Demand</h4>
    <p style="margin: 5px 0 0 0; font-size: 14px; color: #cbd5e1;">Major semiconductor and software companies reported better than expected earnings this quarter driven by enterprise AI spending.</p>
</div>
"""
st.markdown(news_html, unsafe_allow_html=True)
