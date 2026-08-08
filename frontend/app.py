from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Render public URL format
    api_host = os.environ.get("API_HOST", "")
    api_url = f"https://{api_host}.onrender.com" if api_host else "http://localhost:8000"
    return render_template('index.html', api_url=api_url)

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8501))
    app.run(host='0.0.0.0', port=port, debug=True)
