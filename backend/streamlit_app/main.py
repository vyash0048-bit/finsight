import os
import requests
import streamlit as st

from styles import PREMIUM_CSS

st.set_page_config(
    page_title="FinSight | Login",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

API_HOSTPORT = os.getenv("API_HOSTPORT", "localhost:8000")
API_URL = f"http://{API_HOSTPORT}".rstrip("/")

def login(email, password):
    response = requests.post(f"{API_URL}/auth/login", data={"username": email, "password": password})
    if response.status_code == 200:
        st.session_state["token"] = response.json().get("access_token")
        st.session_state["logged_in"] = True
        st.success("Login successful! Please select a page from the sidebar.")
        st.rerun()
    else:
        st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")

def signup(email, password):
    response = requests.post(f"{API_URL}/auth/signup", json={"email": email, "password": password})
    if response.status_code == 200:
        st.success("Signup successful! You can now log in.")
    else:
        st.error(f"Signup failed: {response.json().get('detail', 'Unknown error')}")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("✨ FinSight AI Swarm")
    st.markdown("### Welcome to your Autonomous Research Terminal.")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        email_login = st.text_input("Email", key="login_email")
        password_login = st.text_input("Password", type="password", key="login_password")
        if st.button("Log In"):
            login(email_login, password_login)
            
    with tab2:
        st.subheader("Create Account")
        email_signup = st.text_input("Email", key="signup_email")
        password_signup = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            signup(email_signup, password_signup)
else:
    st.title("✨ FinSight AI Swarm")
    st.success("You are logged in!")
    st.info("👈 Please select a module from the sidebar to begin.")
    
    if st.button("Log Out"):
        st.session_state["logged_in"] = False
        st.session_state["token"] = None
        st.rerun()

    # Decorative metrics
    cols = st.columns(3)
    with cols[0]:
        st.metric(label="Active Agents", value="6", delta="Online")
    with cols[1]:
        st.metric(label="Data Sources", value="Yahoo Finance", delta="Live")
    with cols[2]:
        st.metric(label="LLM Core", value="Gemini Flash Lite", delta="Active")
