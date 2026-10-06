import os

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    api_host = os.environ.get("API_HOST", "localhost:8000")
    if not api_host.startswith("http"):
        if "localhost" in api_host or "127.0.0.1" in api_host:
            api_url = f"http://{api_host}"
        else:
            if "." not in api_host:
                api_host = f"{api_host}.onrender.com"
            api_url = f"https://{api_host}"
    else:
        api_url = api_host
    return render_template('index.html', api_url=api_url)

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8501'))
    app.run(host='0.0.0.0', port=port, debug=True)
