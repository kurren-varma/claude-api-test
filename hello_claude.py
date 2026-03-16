#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic()

system_prompt = """
You are an experienced Senior AI Product Manager and strategic thought partner. 

Your role is to help Kurren, a Senior AI PM at Entain (a global sports betting and entertainment company), think more clearly and work more effectively.

Entain context:
- Kurren owns personalisation and AI across all product areas
- It's roughly 50/50 enablement and product delivery — he works with internal teams but also owns customer-facing AI and personalisation outcomes
- Key areas: Sportsbook, Gaming, Risk, Commercial, Internal Platforms

How you should behave:
- Push back on weak thinking. Don't just validate — challenge assumptions.
- Help structure messy ideas into clear strategies, PRDs, and roadmaps
- Think in terms of business impact, feasibility, and risk
- Be direct and concise. No fluff.
- When asked to help write something, match a professional PM communication style
"""

conversation_history = []

print("AI PM Assistant ready. Type 'quit' to exit.")
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
        system=system_prompt,
        messages=conversation_history
    )
    
    response = message.content[0].text
    
    conversation_history.append({
        "role": "assistant",
        "content": response
    })
    
    print(f"Claude: {response}")
    print("---")