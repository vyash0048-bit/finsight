from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    content = response.text
    # Check that our custom metrics exist in the exposition format
    assert "llm_cost_dollars_total" in content
    assert "agent_run_total" in content
    assert "llm_token_count_total" in content
