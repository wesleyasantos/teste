import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    system="AC",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "A poem about the ocean"
                }
            ]
        }
    ]     
)