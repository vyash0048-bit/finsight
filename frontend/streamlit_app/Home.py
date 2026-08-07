import streamlit as st
import requests

st.set_page_config(page_title="FinSight", page_icon="📈", layout="wide")

st.title("Welcome to FinSight")
st.write("AI Multi-Agent Stock Research Platform")

# Check API Health
try:
    # Use the docker-compose service name 'api'
    response = requests.get("http://api:8000/health")
    if response.status_code == 200:
        st.success("Connected to Backend API successfully!")
    else:
        st.warning("Backend API responded with an error.")
except Exception as e:
    st.error(f"Failed to connect to Backend API: {e}")
