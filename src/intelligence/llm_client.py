import requests
import json
from src.utils.logger import get_logger
from src.intelligence.prompt_manager import PromptManager
from src.intelligence.memory import ConversationMemory

logger = get_logger(__name__)

class LLMClient:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "phi3"
        self.memory = ConversationMemory(max_messages=8)

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

            self.memory.add_message("user", user_input)
            self.memory.add_message("assistant", text)

            logger.info(f"LLM Response: {text}")
            return text if text else "I didn't understand that."

        except Exception as e:
            logger.error(f"LLM Error: {e}")
            return "Something went wrong."

    def get_response_stream(self, user_input: str):
        try:
            messages = PromptManager.build_messages(
                user_input,
                self.memory.get_context()
            )

            prompt = self._format_prompt(messages)

            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True
                },
                stream=True,
                timeout=60
            )

            response.raise_for_status()

            full_response = ""

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        chunk = data.get("response", "")

                        if chunk:
                            full_response += chunk
                            yield chunk   

                        if data.get("done", False):
                            break

                    except json.JSONDecodeError:
                        continue

            self.memory.add_message("user", user_input)
            self.memory.add_message("assistant", full_response)

            logger.info(f"Full LLM Response: {full_response}")

        except Exception as e:
            logger.error(f"Streaming Error: {e}")
            yield "Sorry, something went wrong."

    def _format_prompt(self, messages):
        prompt = ""

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                prompt += f"[SYSTEM]\n{content}\n"
            elif role == "user":
                prompt += f"[USER]\n{content}\n"
            elif role == "assistant":
                prompt += f"[ASSISTANT]\n{content}\n"

        prompt += "[ASSISTANT]\n"
        return prompt