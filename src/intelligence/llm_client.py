import requests
from src.utils.logger import get_logger

logger = get_logger(__name__)

class LLMClient:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "phi3"

    def get_response(self, user_input: str) -> str:
        try:
            prompt = self._build_prompt(user_input)
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            text = data.get("response", "").strip()

            logger.info(f"LLM Response: {text}")
            return text if text else "I didn't understand that."
        
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            return "Something went wrong."
        
    def _build_prompt(self,user_input: str) -> str:
        return f"""
            You are VaaniAI, a smart voice assistant.
            Keep responses:
            - Short
            - Natural
                - Speakable (no long paragraphs)

                User: {user_input}
                Assistant:
                """