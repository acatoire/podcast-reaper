"""
This script reads all files in a given directory and its subdirectories,
concatenates their content, and creates a PDF file with the content of the chosen extension files.
"""
import os
import glob
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DO_NOT_PRINT = ["WEBVTT"]

def find_files(dir_path, ext, contains_txt):
    print("Find all .vtt files in the given directory and its subdirectories.")
    ext_files = glob.glob(os.path.join(dir_path, '**', f'*{contains_txt}*.{ext}'), recursive=True)
    print(f"Found {len(ext_files)} files in {dir_path}.")
    return sorted(ext_files)

def read_vtt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def add_footer(c, page_number):
    c.saveState()
    c.setFont("Helvetica", 9)
    c.drawString(c._pagesize[0] / 2, 20, f"Page {page_number}")
    c.restoreState()

def create_pdf(files_list, pdf_path):
    print("\n\n----------------------------------------")
    print("Create a PDF by concatenating the content of files.")

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    y_position = height - 30
    page_number = 1

    for file_path in files_list:
        content = read_vtt_file(file_path)
        print(f"Processing: {file_path}", end='')
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y_position, f"{os.path.basename(file_path.replace(f'.{extension}', ''))}")
        c.setFont("Helvetica", 10)

        y_position -= 8
        c.drawString(40, y_position, '-' * 150)
        y_position -= 6

        for line in content.splitlines():

            print('.', end='')
            if y_position < 40:
                add_footer(c, page_number)
                c.showPage()
                page_number += 1
                y_position = height - 40

            if line in DO_NOT_PRINT:
                continue

            if line == '':
                continue

            if line.__contains__('-->'):
                c.setFont("Helvetica", 5)
            else:
                c.setFont("Helvetica", 10)

            c.drawString(40, y_position, line)
            y_position -= 12

        print(' done')

    add_footer(c, page_number)
    c.save()

def main(directory, output_pdf, ext, contains_txt):
    files = find_files(directory, ext, contains_txt)
    create_pdf(files, output_pdf)
    print(f"PDF created: {output_pdf}")

if __name__ == "__main__":
    model = "turbo"
    directory_input = f"transcript/{model}"
    extensions = ["vtt", "txt", 'srt', 'tsv', 'json']
    contains = 'Confinés'
    contains_list = ['Plutôt_Confinés_',
                     'Plutôt_Déconfinés-',
                     'Plutôt_reConfinés-',
                     'Plutôt_MiConfinés_',
                     '2020',
                     '2021',
                     '2022',
                     '2023',
                     '2024',]

    # output_pdf_path = f"output_{contains}.pdf"
    # main(directory_input, output_pdf_path, extension, contains)

    output_dir = f"transcript/pdf-{model}"
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    for extension in extensions:
        print(f"--- Processing extension: {extension}")
        for contains in contains_list:
            print(f"------ Processing contains: {contains}")
            output_pdf_path = f"{output_dir}/{contains}_{extension}.pdf"
            main(directory_input, output_pdf_path, extension, contains)

