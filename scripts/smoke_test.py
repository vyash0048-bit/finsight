import requests
import sys
import time

def run_smoke_test(base_url: str):
    print(f"Starting smoke tests against {base_url}...")
    
    # Test 1: Healthcheck
    try:
        res = requests.get(f"{base_url}/health", timeout=5)
        res.raise_for_status()
        assert res.json().get("status") == "ok"
        print("✅ [PASS] /health endpoint is alive and well.")
    except Exception as e:
        print(f"❌ [FAIL] /health endpoint failed: {e}")
        sys.exit(1)

    # Test 2: Unauthenticated Auth route
    try:
        res = requests.get(f"{base_url}/auth/me", timeout=5)
        # We expect a 401 Unauthorized for a protected route without a token
        assert res.status_code == 401, f"Expected 401, got {res.status_code}"
        print("✅ [PASS] /auth/me correctly rejected unauthenticated access.")
    except Exception as e:
        print(f"❌ [FAIL] /auth/me rejection test failed: {e}")
        sys.exit(1)
        
    print("\n🎉 All smoke tests passed! The deployment is ready for traffic.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python smoke_test.py <API_URL>")
        sys.exit(1)
    
    target_url = sys.argv[1].rstrip('/')
    run_smoke_test(target_url)
