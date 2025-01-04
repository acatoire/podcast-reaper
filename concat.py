"""
This script reads all files in a given directory and its subdirectories,
concatenates their content, and creates a PDF file with the content of the chosen extension files.
"""
import os
import glob
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DO_NOT_PRINT = ["WEBVTT"]

def find_files(dir_path, ext, start_txt):
    print("Find all .vtt files in the given directory and its subdirectories.")
    ext_files = glob.glob(os.path.join(dir_path, '**', f'{start_txt}*.{ext}'), recursive=True)
    print(f"Found {len(ext_files)} files in {dir_path}.")
    return sorted(ext_files)

def read_vtt_file(file_path):
    print("Read the content of a file.")
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def add_footer(c, page_number):
    c.saveState()
    c.setFont("Helvetica", 9)
    c.drawString(c._pagesize[0] / 2, 20, f"Page {page_number}")
    c.restoreState()

def create_pdf(files_list, pdf_path):
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

def main(directory, output_pdf, ext, start_txt):
    files = find_files(directory, ext, start_txt)
    create_pdf(files, output_pdf)
    print(f"PDF created: {output_pdf}")

if __name__ == "__main__":
    directory_input = "transcript/turbo"
    extension = "vtt"
    start = '2020'
    output_pdf_path = f"output_{start}.pdf"
    main(directory_input, output_pdf_path, extension, start)
