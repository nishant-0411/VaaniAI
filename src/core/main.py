from src.intelligence.memory import ConversationMemory
from src.intelligence.llm_client import LLMClient

memory = ConversationMemory(max_messages=8)
llm = LLMClient(memory)

while True:
    user_input = input("You: ")

    print("AI: ", end="", flush=True)

    for token in llm.get_streaming_response(user_input):
        print(token, end="", flush=True)

    print()