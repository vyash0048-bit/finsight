import os
import sys

import streamlit as st

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if backend_path not in sys.path:
    sys.path.append(backend_path)

from styles import PREMIUM_CSS

st.set_page_config(page_title="Portfolio | FinSight", layout="wide")
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

st.title("💼 Portfolio Optimizer")
st.markdown("Enter your desired basket of stocks to compute the mathematically optimal allocation (Max Sharpe Ratio).")

tickers_input = st.text_input("Tickers (comma-separated)", "AAPL, MSFT, GOOGL")

if st.button("⚖️ Optimize Allocation"):
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    if len(tickers) < 2:
        st.warning("Please enter at least 2 tickers to optimize.")
    else:
        with st.spinner("Crunching covariance matrices and historical returns..."):
            from app.agents.portfolio_agent import PortfolioAgent
            
            agent = PortfolioAgent()
            out = agent.execute(tickers)
            
            if out.status == "success":
                st.success("Optimization Complete!")
                
                cols = st.columns([1, 2])
                with cols[0]:
                    st.markdown("### Weights")
                    # To render chart, get weights directly or parse from output
                    from app.services.portfolio_service import optimize_portfolio
                    weights = optimize_portfolio(tickers)
                    st.bar_chart(weights)
                    
                with cols[1]:
                    st.markdown("### Agent Analysis")
                    st.write(out.data.get("explanation", ""))
                    st.warning(out.data.get("warning", ""))
            else:
                st.error(f"Optimization Failed: {out.summary}")
