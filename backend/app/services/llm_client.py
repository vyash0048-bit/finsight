import json
import logging
import os
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel, ValidationError
import litellm

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class LLMClient:
    def __init__(self):
        self.model = "gemini/gemini-3.1-flash-lite"
        
    def call_llm(self, prompt: str, schema: Type[T], max_retries: int = 1, system_prompt: Optional[str] = None) -> Optional[T]:
        """
        Calls the LLM and enforces output to match the provided Pydantic schema using JSON mode.
        Includes a retry-with-repair mechanism for malformed JSON or validation errors.
        """
        base_role = system_prompt if system_prompt else "You are a helpful financial AI."
        system_msg = (
            f"{base_role}\n"
            f"Respond ONLY with a valid JSON object matching this schema: {schema.model_json_schema()}"
        )
        
        attempt = 0
        last_error = ""
        
        while attempt <= max_retries:
            try:
                messages = [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]
                
                # If it's a retry, pass the error back to the LLM to 'repair' it
                if attempt > 0:
                    messages.append({"role": "user", "content": f"Your previous response failed validation: {last_error}. Please fix the JSON output."})

                # litellm drop-in replacement
                response = litellm.completion(
                    model=self.model,
                    messages=messages,
                    response_format={"type": "json_object"}
                )
                
                content = response.choices[0].message.content
                
                # Log usage and costs (critical for Phase 7)
                usage = response.usage
                if usage:
                    logger.info(f"LLM Call - Tokens: {usage.total_tokens} (Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens})")
                
                # Parse and validate against the Pydantic schema
                parsed_data = json.loads(content)
                validated_model = schema(**parsed_data)
                
                return validated_model
                
            except ValidationError as ve:
                logger.warning(f"Attempt {attempt + 1}: Pydantic validation error: {ve}")
                last_error = str(ve)
            except json.JSONDecodeError as je:
                logger.warning(f"Attempt {attempt + 1}: JSON decode error: {je}")
                last_error = str(je)
            except Exception as e:
                logger.error(f"LLM API Error: {e}")
                break
                
            attempt += 1
            
        logger.error(f"Failed to generate valid response after {max_retries + 1} attempts.")
        return None
