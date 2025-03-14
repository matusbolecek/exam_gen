import anthropic
from dotenv import load_dotenv
import os
import sys

# loads "ANTHROPIC_API_KEY=key" from a token.env file
if not load_dotenv('token.env'):
    print("Error: Could not load token.env file")
    sys.exit(1)

def main(user: str, prompt: str):

    client = anthropic.Anthropic()
    vystup = ''

    try:
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=8192,
            temperature=0,
            system=prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user
                        }
                    ]
                }
            ]
        )
        
        for content in message.content:
            if content.type == "text":
                vystup += content.text
                    
    except anthropic.APIError as e:
        print(f"API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

    return vystup