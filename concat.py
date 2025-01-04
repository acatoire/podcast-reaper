"""
This script reads all files in a given directory and its subdirectories,
concatenates their content, and creates a PDF file with the content of the chosen extension files.
"""
import os
import glob
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def find_files(dir_path, ext):
    print("Find all .vtt files in the given directory and its subdirectories.")
    ext_files = glob.glob(os.path.join(dir_path, '**', f'*.{ext}'), recursive=True)
    print(f"Found {len(ext_files)} files in {dir_path}.")
    return sorted(ext_files)

def read_vtt_file(file_path):
    print("Read the content of a file.")
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def create_pdf(vtt_files, pdf_path):
    print("Create a PDF by concatenating the content of files.")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y_position = height - 40

    for file_path in vtt_files:
        content = read_vtt_file(file_path)
        print(f"Processing: {file_path}", end='')
        c.drawString(40,
                     y_position,
                     f"{os.path.basename(file_path.replace(f'.{extension}', ''))}")
        y_position -= 20

        for line in content.splitlines():
            print('.', end='')
            if y_position < 40:
                c.showPage()
                y_position = height - 40

            c.drawString(40, y_position, line)
            y_position -= 12

        print(' done')

    c.save()

def main(directory, output_pdf, ext):
    files = find_files(directory, ext)
    create_pdf(files, output_pdf)
    print(f"PDF created: {output_pdf}")

if __name__ == "__main__":
    directory_input = "transcript/turbo"
    output_pdf_path = "output.pdf"
    extension = "vtt"
    main(directory_input, output_pdf_path, extension)
