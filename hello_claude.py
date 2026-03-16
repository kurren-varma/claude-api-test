#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()

import anthropic
import sys

client = anthropic.Anthropic()

system_prompt = """
You are an experienced Senior AI Product Manager and strategic thought partner.

Your role is to help Kurren, a Senior AI PM at Entain (a global sports betting and entertainment company), think more clearly and work more effectively.

Entain context:
- Kurren owns personalisation and AI across all product areas
- It's roughly 50/50 enablement and product delivery
- Key areas: Sportsbook, Gaming, Risk, Commercial, Internal Platforms

How you should behave:
- Push back on weak thinking. Don't just validate — challenge assumptions.
- Help structure messy ideas into clear strategies, PRDs, and roadmaps
- Think in terms of business impact, feasibility, and risk
- Be direct and concise. No fluff.
- When asked to help write something, match a professional PM communication style

When the user pastes a large block of text or document:
- Acknowledge what type of document it appears to be
- Ask what they want done with it (summarise, critique, improve, extract actions, etc.)
- Wait for their instruction before doing anything with it
"""

conversation_history = []

# Check if a file was passed in
def read_file(filename):
    if filename.endswith('.txt') or filename.endswith('.md'):
        with open(filename, 'r') as f:
            return f.read()
    elif filename.endswith('.pdf'):
        from pypdf import PdfReader
        reader = PdfReader(filename)
        return "\n".join([page.extract_text() for page in reader.pages])
    elif filename.endswith('.docx'):
        from docx import Document
        doc = Document(filename)
        return "\n".join([para.text for para in doc.paragraphs])
    elif filename.endswith('.pptx'):
        from pptx import Presentation
        prs = Presentation(filename)
        text = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text.append(shape.text)
        return "\n".join(text)
    else:
        print(f"Unsupported file type: {filename}")
        sys.exit(1)

if len(sys.argv) > 1:
    all_contents = []
    for filename in sys.argv[1:]:
        try:
            file_contents = read_file(filename)
            print(f"📄 Loaded: {filename}")
            all_contents.append(f"--- {filename} ---\n{file_contents}")
        except FileNotFoundError:
            print(f"File not found: {filename}")
            sys.exit(1)
    
    conversation_history.append({
        "role": "user",
        "content": f"I'm sharing these documents with you:\n\n" + "\n\n".join(all_contents)
    })

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
        max_tokens=4096,
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
    
    # Save response to file
    with open("responses.md", "a") as f:
        f.write(f"## You:\n{user_input}\n\n## Claude:\n{response}\n\n---\n\n")