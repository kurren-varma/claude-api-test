from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic()

user_input = input("Ask Claude anything: ")

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": user_input}
    ]
)

print(message.content[0].text)