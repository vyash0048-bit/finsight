import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        /* Modern Gradient Background for the main container */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        
        /* Stylish glowing headers */
        h1, h2, h3 {
            background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Inter', sans-serif;
            font-weight: 800;
        }
        
        /* Glassmorphism for metrics */
        div[data-testid="stMetricValue"] {
            color: #ffffff;
            font-weight: 800;
        }
        div[data-testid="stMetricLabel"] {
            color: #94a3b8;
            font-weight: 600;
        }
        div[data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Stylish buttons */
        .stButton>button {
            background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.5);
            color: white;
            border: none;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.95);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Input fields */
        .stTextInput>div>div>input {
            background: rgba(255, 255, 255, 0.05);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
        }
        .stTextInput>div>div>input:focus {
            border-color: #8b5cf6;
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)
