import pymupdf
import anthropic
import base64
import pathlib
from dotenv import load_dotenv
import sys

def main(file):
    output = str('')
    filetype = pathlib.Path(file).suffix
    
    if filetype in ['.pdf', '.xps', '.epub']:
        doc = pymupdf.open(file)
        for page in doc:
            output += page.get_text()  

    elif filetype in ['.jpg', '.jpeg', '.png']:

        # loads "ANTHROPIC_API_KEY=key" from a token.env file
        if not load_dotenv('token.env'):
            print("Error: Could not load token.env file")
            sys.exit(1)

        with open(file, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')  

        if filetype == '.jpg':
            media_type = 'image/jpeg'
        else:
            media_type = f'image/{filetype[1:]}'

        with open(f'prompts/read_img.txt', 'r') as file:
            prompt = file.read()
        
        try:
            client = anthropic.Anthropic()
            message = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )
            output += message.content[0].text
        except anthropic.APIError as e:
            print(f"API Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)        

    return output

if __name__ == "__main__":
    w = main('ab.png')
    
    with open(f'abc.txt', 'w') as file:
        file.write(w)