PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}

/* Make it look like a sleek dashboard */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #f8fafc;
}

/* Glassmorphism containers */
div[data-testid="stMetric"], div[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 15px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

/* Inputs */
.stTextInput>div>div>input {
    background: rgba(0,0,0,0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
}
</style>
"""
