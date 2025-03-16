import pymupdf
import base64
import pathlib
import sys
import os

def main(file):
    output = ""
    filetype = pathlib.Path(file).suffix.lower()
    
    if filetype in ['.pdf', '.xps', '.epub']:
        doc = pymupdf.open(file)
        for page in doc:
            output += page.get_text()
        return {"type": "text", "text": output}
        
    elif filetype in ['.jpg', '.jpeg', '.png']:
        with open(file, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        if filetype == '.jpg' or filetype == '.jpeg':
            media_type = 'image/jpeg'
        else:
            media_type = f'image/{filetype[1:]}'
            
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": image_data,
            }
        }
        
    elif filetype in ['.txt', '.tex']:
        with open(file, "r") as file_obj:
            output = file_obj.read()
        return {"type": "text", "text": output}
        
    else:
        return {"type": "text", "text": f"Unsupported file type: {filetype}"}

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