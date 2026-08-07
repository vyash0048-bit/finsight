from pydantic import BaseModel

from app.services.llm_client import LLMClient


class DummySchema(BaseModel):
    sentiment: str
    score: int

def test_call_llm_success(mocker):
    # Mock the OpenAI API response
    mock_response = mocker.MagicMock()
    mock_response.choices[0].message.content = '{"sentiment": "positive", "score": 85}'
    mock_response.usage.total_tokens = 100
    mock_response.usage.prompt_tokens = 50
    mock_response.usage.completion_tokens = 50
    
    # Patch the litellm completion method
    mock_create = mocker.patch("litellm.completion", return_value=mock_response)
    
    client = LLMClient()
    result = client.call_llm("What is the sentiment of AAPL?", DummySchema)
    
    # Assertions
    assert result is not None
    assert isinstance(result, DummySchema)
    assert result.sentiment == "positive"
    assert result.score == 85
    mock_create.assert_called_once()
