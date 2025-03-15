import pymupdf
import anthropic
import base64
import pathlib
from dotenv import load_dotenv
import sys

def image(file, filetype):
    # loads "ANTHROPIC_API_KEY=key" from a token.env file
    if not load_dotenv('token.env'):
        print("Error: Could not load token.env file")
        sys.exit(1)

    with open(file, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    
    if filetype == '.jpg' or filetype == '.jpeg':
        media_type = 'image/jpeg'
    else:
        media_type = f'image/{filetype[1:]}'
    
    with open('prompts/read_img.txt', 'r') as file:
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
        output = message.content[0].text
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    return output

def main(file):
    output = str('')
    filetype = pathlib.Path(file).suffix.lower()
    
    if filetype in ['.pdf', '.xps', '.epub']:
        doc = pymupdf.open(file)
        for page in doc:
            output += page.get_text()  

    elif filetype in ['.jpg', '.jpeg', '.png']:
        output += image(file, filetype)
    else:
        output = f"Unsupported file type: {filetype}"
    
    return output

if __name__ == "__main__":
    # Test case if run directly
    file_path = input('Input a file path to process: ')
    file_path = file_path.strip("'\"").strip()
    
    if not file_path:
        print("No file path provided.")
        sys.exit(1)
    
    if not pathlib.Path(file_path).exists():
        print(f"File not found: {file_path}")
        sys.exit(1)
        
    result = main(file_path)
    print(result)