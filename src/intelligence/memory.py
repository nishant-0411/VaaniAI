from collections import deque
from typing import List, Dict

class ConversationMemory:
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.history = deque(maxlen=max_messages)

    def add_message(self, role:str, content: str):
        self.history.append({"role": role,"content": content})

    def get_context(self)-> List[Dict]:
        return list(self.history)
    
    def clear(self):
        self.history.clear()