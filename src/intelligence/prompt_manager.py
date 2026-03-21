class PromptManager:
    @staticmethod
    def get_system_prompt() -> str:
        return (
            "You are VaaniAI, a smart voice assistant.\n\n"
            "Rules:\n"
            "- Keep responses short and conversational.\n"
            "- Do NOT use markdown, bullet points, or special formatting.\n"
            "- Speak like a human, not like a document.\n"
            "- Avoid long explanations unless explicitly asked.\n"
            "- Prefer simple sentences.\n"
        )

    @staticmethod
    def build_messages(user_input: str, memory_context: list) -> list:
        """System Behaviour + History + User Input"""

        messages = [{"role": "system", "content": PromptManager.get_system_prompt()}]

        messages.extend(memory_context)

        messages.append({"role": "user","content": user_input})

        return messages