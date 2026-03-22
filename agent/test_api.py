import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

try:
    message = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("Success, this is the right model!.")
    print(message.content[0].text)
except Exception as e:
    print(f"Error: {e}")