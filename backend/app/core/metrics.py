from prometheus_client import Counter, Histogram

# HTTP Metrics (Standard)
http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

# LLM & Agent Metrics (Custom)
llm_token_count_total = Counter(
    "llm_token_count_total",
    "Total number of tokens consumed by the LLM",
    ["model", "token_type"] # token_type: prompt or completion
)

llm_cost_dollars_total = Counter(
    "llm_cost_dollars_total",
    "Estimated cost of LLM calls in USD",
    ["model"]
)

agent_run_total = Counter(
    "agent_run_total",
    "Total number of agent executions",
    ["agent_name", "status"] # status: success or error
)

agent_run_duration_seconds = Histogram(
    "agent_run_duration_seconds",
    "Duration of agent execution in seconds",
    ["agent_name"]
)
