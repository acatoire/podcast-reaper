"""
This script reads all files in a given directory and its subdirectories,
concatenates their content, and creates a PDF file with the content of the chosen extension files.
"""
import locale
import os
import glob
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re

DO_NOT_PRINT = ["WEBVTT"]

def find_files(dir_path, ext, contains_txt):
    print("Find all .vtt files in the given directory and its subdirectories.")
    ext_files = glob.glob(os.path.join(dir_path, '**', f'*{contains_txt}*.{ext}'), recursive=True)
    print(f"Found {len(ext_files)} files in {dir_path}:")
    for file_path in ext_files:
        print(f" - {file_path}")
    return sorted(ext_files)

def read_vtt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def add_footer(c, page_number):
    c.saveState()
    c.setFont("Helvetica", 9)
    c.drawString(c._pagesize[0] / 2, 20, f"Page {page_number}")
    c.restoreState()

def parse_timestamp(timestamp):
    """Parse a timestamp to seconds
        00:00:03,800 - vtt format
        00:03.800 - srt format
    """
    try:
        if timestamp.count(':') == 1 and '.' in timestamp:
            m, s, mm = map(int, re.split('[:|.]', timestamp))
            return m * 60 + s

        if timestamp.count(':') == 2 and '.' in timestamp:
            h, m, s, mm = map(int, re.split('[:|.]', timestamp))
            return h * 3600 + m * 60 + s

        if timestamp.count(':') == 2 and ',' in timestamp:
            h, m, s, mm = map(float, re.split('[:|,]', timestamp))
            return h * 3600 + m * 60 + s
    except:
        raise ValueError(f"Invalid timestamp format: {timestamp}")

    raise ValueError(f"Invalid timestamp format: {timestamp}")

def parse_speaker_info(line):
    """Parse a line of speaker information."""
    match = re.match(r'start=(\d+\.\d+)s stop=(\d+\.\d+)s speaker_(.+)', line)
    if match:
        start, stop, speaker = match.groups()
        return float(start), float(stop), speaker
    return None

def find_speaker(seconds, speaker_info):
    """Find the speaker for a given seconds."""
    for start, stop, speaker in speaker_info:
        if start <= seconds <= stop:
            return speaker

    print (f"Speaker at second not found ( {seconds}s).")
    return None

def match_timestamps_to_speakers(timestamps, speaker_info):
    """Match timestamps to speaker information and print the results."""

    start_timestamp, end_timestamp = timestamps.strip().split(' --> ')
    start_seconds = parse_timestamp(start_timestamp)
    end_seconds = parse_timestamp(end_timestamp)
    speak_center = start_seconds + ((end_seconds - start_seconds) // 2)

    speaker = find_speaker(speak_center, speaker_info)

    return f"{start_timestamp} --> {end_timestamp} : {speaker}"


def process_line(line, speaker_info=None):

    if speaker_info is None:
        return line

    if line.__contains__('-->'):
        return match_timestamps_to_speakers(line, speaker_info)
    else:
        return line


def create_pdf(files_list, pdf_path, ext):
    print("\n\n----------------------------------------")
    print("Create a PDF by concatenating the transcript_content of files.")

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    y_position = height - 30
    page_number = 1

    # first page with list of files
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y_position, "Lists des épisodes")
    y_position -= 20

    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

    print("Processing files list as first page")

    c.setFont("Helvetica", 10)
    for index, file_path in enumerate(files_list):
        file_name = os.path.basename(file_path)
        name_split = file_name.split('-')
        date_obj = datetime(int(name_split[0]), int(name_split[1]), int(name_split[2]))
        full_date = date_obj.strftime('%A %d %B')
        episode_name = ' '.join(name_split[3:]).replace(ext, '')
        line_content = f"{index}] Episode du {full_date} : {episode_name}"
        print(line_content)

        if y_position < 40:
            add_footer(c, page_number)
            c.showPage()
            page_number += 1
            y_position = height - 40

        # Write the file name and details
        c.drawString(40, y_position,
                     line_content)
        y_position -= 12

    # write the total number of episodes

    y_position -= 20
    c.drawString(40, y_position,
                 f"Nombres d'épisodes : {len(files_list)}")

    add_footer(c, page_number)
    c.showPage()
    page_number += 1
    y_position = height - 30


    for file_path in files_list:
        transcript_file_name = os.path.basename(file_path)
        diarization_file_name = transcript_file_name.replace(f'.{ext}', '-diari.txt')
        diarization_path = os.path.join('transcript', 'diarization', diarization_file_name)

        transcript_content = read_vtt_file(file_path)
        speaker_info = get_speaker_info(diarization_path)

        print(f"Processing: {file_path}", end='')
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y_position, f"{os.path.basename(file_path.replace(f'.{ext}', ''))}")
        c.setFont("Helvetica", 10)

        y_position -= 8
        c.drawString(40, y_position, '-' * 150)
        y_position -= 6

        for line in transcript_content.splitlines():

            # print('.', end='')
            if y_position < 40:
                add_footer(c, page_number)
                c.showPage()
                page_number += 1
                y_position = height - 40

            if line in DO_NOT_PRINT:
                continue

            if line == '':
                continue

            if '-->' in line:
                c.setFont("Helvetica", 5)
            else:
                c.setFont("Helvetica", 10)
                
            #line_to_write = process_line(line)
            line_to_write = process_line(line, speaker_info)

            c.drawString(40, y_position, line_to_write)
            y_position -= 12

        print(' done')

    add_footer(c, page_number)
    c.save()


def get_speaker_info(diarization_path):

    if not os.path.exists(diarization_path):
        print(f"Speaker information file not found: {diarization_path}")
        return None

    with open(diarization_path, 'r') as f:
        speaker_def = f.readlines()
    # Parse speaker information
    speaker_info = []
    for line in speaker_def:
        info = parse_speaker_info(line)
        if info:
            speaker_info.append(info)
    return speaker_info


def main(directory, output_pdf, ext, contains_txt):

    files = find_files(directory, ext, contains_txt)
    create_pdf(files, output_pdf, ext)
    print(f"PDF created: {output_pdf}")

if __name__ == "__main__":
    model = "large-v3"
    #model = "turbo"
    directory_input = f"transcript/{model}"
    extensions = ["vtt"]
    #contains_list = ['Plutôt_Confinés_']

    extensions = ["vtt",
                  "txt",
                  #'srt',
                  #'tsv',
                  #'json'
                  ]
    contains_list = [
        'Plutôt_Confinés',
        'Plutôt_Déconfinés',
        'Plutôt_reConfinés',
        'Plutôt_MiConfinés',
        '2018',
        '2019',
        '2020',
        '2021',
        '2022',
        '2023',
        '2024',
        'Passion'
        ]

    # output_pdf_path = f"output_{contains}.pdf"
    # main(directory_input, output_pdf_path, extension, contains)

    output_dir = f"transcript/pdf-{model}"
    #if os.path.exists(output_dir):
    #    import shutil
    #    shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # TODO separate folder with diarization addon
    # TODO separate folder with not pdf concat

    for contains in contains_list:
        print(f"------ Processing contains: {contains}")
        for extension in extensions:
            print(f"--- Processing extension: {extension}")
            output_pdf_path = f"{output_dir}/{contains}_{extension}.pdf"
            main(directory_input, output_pdf_path, extension, contains)
