#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic()

conversation_history = []

print("Chat with Claude! Type 'quit' to exit.")
print("---")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print("Ending conversation.")
        break
    
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=conversation_history
    )
    
    response = message.content[0].text
    
    conversation_history.append({
        "role": "assistant",
        "content": response
    })
    
    print(f"Claude: {response}")
    print("---")