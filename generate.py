import os
import pathlib
import re

# PDF Generation
from pdflatex import PDFLaTeX
import shutil

import claude as model
import process

def generate_pdf(text: str, name="output"):
    tex_filename = f'{name}.tex'
    with open(tex_filename, "a") as tex_file:
        tex_file.write(text)

    pdfl = PDFLaTeX.from_texfile(tex_filename)
    pdf, log, _ = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
    
    return pdf

def parse_test_output(output_string):
    first_line = output_string.strip().split('\n')[0]
    match = re.search(r'\{\{(\d+)\}\}', first_line)
    
    if not match:
        raise ValueError("Could not find number of test groups in the first line")
    
    num_groups = int(match.group(1))
    latex_docs = []
    txt_docs = []
    
    for i in range(1, num_groups + 1):
        latex_pattern = rf'<BEGIN_LATEX_{i}>(.*?)<END_LATEX_{i}>'
        latex_match = re.search(latex_pattern, output_string, re.DOTALL)
        if latex_match:
            latex_docs.append(latex_match.group(1).strip())
        
        txt_pattern = rf'<BEGIN_TXT_{i}>(.*?)<END_TXT_{i}>'
        txt_match = re.search(txt_pattern, output_string, re.DOTALL)
        if txt_match:
            txt_docs.append(txt_match.group(1).strip())
    
    return latex_docs, txt_docs    

if __name__ == "__main__":
    user = ''
    output_folder = input('Enter the output folder path: ').strip("'\"").strip()
    
    templates = []
    templates_folder = 'templates_gen'
    for entry in os.scandir(templates_folder):
        if entry.is_file() and pathlib.Path(entry.path).suffix == '.txt':
            templates.append(entry.path)

    if len(templates) > 0:
        yn = ''
        while True:
            yn = str(input('Do you want to use a template? y/N ')).lower()
            if yn == 'y' or yn == 'n' or yn == '':
                break
            
        if yn == 'n' or yn == '':
            pass
        else:
            print('Templates: ')
            for x in range(0, len(templates)):
                filename = pathlib.Path(templates[x]).stem
                print(f'{x + 1}. {filename}')
            
            choice = int(input('Enter your template choice (0 to pass): '))
            if choice == 0:
                pass
            else:
                with open(templates[choice - 1], 'r') as t:
                    user += t.read()

    with open("prompts/master.txt", 'r') as m:
        master = m.read()

    input_array = []

    add_prompt = input('Add more details to your prompt: ')
    user += add_prompt
    if user != '':
        input_array.append({"type": "text", "text": user})

    while True:
        yn = str(input('Do you want to save it as new template? y/N ')).lower()
        if yn == 'y' or yn == 'n' or yn == '':
            break

    if yn == 'y':
        new_name = input('Enter the name: ')
        
        while True:
            yn2 = str(input('Do you want to include the previous template? y/N ')).lower()
            if yn2 == 'y' or yn2 == 'n' or yn2 == '':
                break
            
        with open(f"{templates_folder}/{new_name}.txt", "a") as f:
            if yn2 == 'y':
                f.write(user)
            else:
                f.write(add_prompt)
    
    x = 1
    files = []
    while True:
        read = input(f'Drag the {x}. file to process. Press enter to exit.')
        if read == '':
            break
        else:
            files.append(read.strip("'\"").strip())
            x += 1

    for items in files:
        input_array.append(process.main(items))

    model_output = model.main(input_array, master)
    latex_docs, txt_docs = parse_test_output(model_output)

    os.chdir(output_folder)

    i = 1
    for x in latex_docs:
        generate_pdf(x, i)
        i += 1

    i = 1
    for x in txt_docs:
        with open(f'{i}.txt', "a") as txt_file:
            txt_file.write(x)
            i += 1