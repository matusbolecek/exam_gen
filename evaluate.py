import pathlib
import os

import claude as model
import process

if __name__ == "__main__":
    user = ''
    output_folder = input('Enter the output folder path: ').strip("'\"").strip()
    
    templates = []
    templates_folder = 'templates_eval'
    for entry in os.scandir(templates_folder):
        if entry.is_file() and pathlib.Path(entry.path).suffix == '.txt':
            templates.append(entry.path)
    print(templates)

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

    with open("prompts/check.txt", 'r') as m:
        master = m.read()

    input_array = []
    user += input('Add more details to your prompt: ')
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
    title = model_output.partition('\n')[0]

    os.chdir(output_folder)

    with open(f'{title}.txt', "a") as txt_file:
        txt_file.write(model_output)