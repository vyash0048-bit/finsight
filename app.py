import sys
import os
import uvicorn

# Add the backend folder to Python's path so imports work correctly
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

if __name__ == "__main__":
    # Hugging Face Spaces expects the app to run on port 7860
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=7860)
