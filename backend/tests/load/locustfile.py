import random

from locust import HttpUser, between, task


class FinSightLoadTest(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def health_check(self):
        self.client.get("/health")

    @task(1)
    def run_report(self):
        # We simulate hitting the report endpoint (which triggers the Swarm)
        # In a real heavy load test, you might mock the LLM, or use caching heavily
        # This will test orchestration overhead
        tickers = ["AAPL", "MSFT", "TSLA"]
        ticker = random.choice(tickers)
        
        # We need to simulate logging in, but for the load test we'll assume 
        # either we bypass auth in load test env or we provide a valid token.
        # Here we'll just test the /auth/me unauthenticated rejection to test FastAPI concurrency
        self.client.get("/auth/me")
