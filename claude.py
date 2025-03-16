import anthropic
from dotenv import load_dotenv
import os
import sys

def main(content, prompt: str):
    if not load_dotenv('token.env'):
        print("Error: Could not load token.env file")
        sys.exit(1)
    
    client = anthropic.Anthropic()
    vystup = ''
    
    if not isinstance(content, list):
        content_array = [content]
    else:
        content_array = content
    
    try:
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=8192,
            temperature=0,
            system=prompt,
            messages=[
                {
                    "role": "user",
                    "content": content_array
                }
            ]
        )
        
        for content_item in message.content:
            if content_item.type == "text":
                vystup += content_item.text
                
    except anthropic.APIError as e:
        print(f"API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
        
    return vystup

if __name__ == "__main__":
    # Test case if launched directly
    test_content = [{"type": "text", "text": "Hello!"}]
    result = main(test_content, "Respond in a friendly manner.")
    print(result)