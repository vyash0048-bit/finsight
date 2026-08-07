import streamlit as st
import time
from components.style import inject_custom_css

st.set_page_config(page_title="AI Reports", page_icon="🤖", layout="wide")
inject_custom_css()

st.title("🤖 Autonomous AI Reports")
st.write("Deploy the FinSight AI team to analyze any stock and generate a comprehensive investment thesis.")

col1, col2 = st.columns([1, 2])
with col1:
    ticker = st.text_input("Enter a Ticker Symbol", placeholder="e.g. AAPL, MSFT", max_chars=5)
    generate = st.button("Deploy Agents")

if generate:
    if ticker:
        with st.spinner(f"🚀 Deploying Fundamental, Technical, and News agents to analyze {ticker.upper()}..."):
            # Mocking the AI agent delay for the UI skeleton
            time.sleep(3)
            
        st.success(f"Analysis Complete for {ticker.upper()}")
        
        # Displaying the report in a beautiful container
        report_html = f"""
        <div style="background: rgba(15, 23, 42, 0.7); padding: 30px; border-radius: 15px; border: 1px solid rgba(139, 92, 246, 0.3); box-shadow: 0 0 20px rgba(139, 92, 246, 0.1);">
            <h2 style="text-align: center; margin-top: 0; font-size: 28px;">--- SUPERVISOR DECISION ---</h2>
            <h3 style="color: #60a5fa;">TICKER: {ticker.upper()}</h3>
            
            <h4 style="color: #c084fc; margin-bottom: 5px;">📊 FUNDAMENTALS</h4>
            <p style="color: #e2e8f0; line-height: 1.6;">Valuation looks reasonable. The trailing P/E sits at 22.4, which is favorable compared to sector averages. Profit margins remain robust at 25%.</p>
            
            <h4 style="color: #c084fc; margin-bottom: 5px;">📈 TECHNICALS</h4>
            <p style="color: #e2e8f0; line-height: 1.6;">Bullish momentum detected. RSI is currently 65.2 (not overbought). The asset is trading 5% above its 50-day moving average.</p>
            
            <h4 style="color: #c084fc; margin-bottom: 5px;">📰 NEWS & SENTIMENT</h4>
            <p style="color: #e2e8f0; line-height: 1.6;">Positive sentiment regarding upcoming product launches and strong guidance from recent earnings calls.</p>
            
            <hr style="border-color: rgba(255,255,255,0.1);">
            <h2 style="text-align: center; color: #10b981; font-size: 32px; font-weight: 800; letter-spacing: 2px;">RECOMMENDATION: STRONG BUY</h2>
        </div>
        """
        st.markdown(report_html, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a ticker symbol to deploy the agents.")
