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


class OptimTool:

    DO_NOT_PRINT = ["WEBVTT"]

    def __init__(self,
                 input_path,
                 output_path,
                 model_name):

        # Pdf settings and variables
        self.pdf_canvas = None
        self.width, self.height = letter
        self.y_position = self.height - 30
        self.page_number = 1


        self.hide_timestamps = True

        self.directory_input = input_path
        self.output_dir = output_path
        self.model = model_name

    def execute(self,
                ext,
                folder,
                with_diari=False,
                with_merge=False):

        self.reset_canvas()

        print("\n\n----------------------------------------")

        # Create the PDF file handler
        output_pdf = f"{self.output_dir}/{self.model}-{ext}/{self.model}-{folder}-{ext}.txt"

        print(f"Optimization for {folder} with {ext} extension.")
        os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
        self.pdf_canvas = canvas.Canvas(output_pdf, pagesize=letter)

        # Find all files in the given directory and its subdirectories
        # TODO add exclude list
        files = self.find_files(ext,
                                contains_txt)


        # Create the PDF file
        self.create_pdf(files,
                        with_diari)
        print(f"PDF created: {output_pdf}")

    def find_files(self,
                   ext,
                   contains_txt):

        print("Find all .vtt files in the given directory and its subdirectories.")
        ext_files = glob.glob(os.path.join(self.directory_input, '**',
                                           f'*{contains_txt}*.{ext}'),
                              recursive=True)

        print(f"Found {len(ext_files)} files in {self.directory_input}:")
        for file_path in ext_files:
            print(f" - {file_path}")

        return sorted(ext_files)

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            # TODO add a check for the file content and a cleaning (remove empty lines, silent hallucinations...)
            return file_content

    @staticmethod
    def parse_timestamp(timestamp):
        """Parse a timestamp to seconds
            00:00:03,800 - vtt format
            (00:)00:03.800 - srt format
        """
        try:
            if timestamp.count(':') == 1 and '.' in timestamp:
                m, s, _ = map(int, re.split('[:|.]', timestamp))
                return m * 60 + s

            if timestamp.count(':') == 2 and '.' in timestamp:
                h, m, s, _ = map(int, re.split('[:|.]', timestamp))
                return h * 3600 + m * 60 + s

            if timestamp.count(':') == 2 and ',' in timestamp:
                h, m, s, _ = map(float, re.split('[:|,]', timestamp))
                return h * 3600 + m * 60 + s
        except:
            raise ValueError(f"Invalid timestamp format: {timestamp}")

        raise ValueError(f"Invalid timestamp format: {timestamp}")

    @staticmethod
    def parse_speaker_info(line):
        """Parse a line of speaker information."""
        match = re.match(r'start=(\d+\.\d+)s stop=(\d+\.\d+)s speaker_(.+)', line)
        if match:
            start, stop, speaker = match.groups()
            return float(start), float(stop), speaker
        return None

    @staticmethod
    def find_speaker(start, end, speaker_info):
        """Find the speaker for a given seconds."""

        speak_center = start + ((end - start) // 2)

        # improve with a better search
        for start, stop, speaker in speaker_info:
            if start <= speak_center <= stop:
                return speaker

        # print (f"Speaker not found ( {speak_center}s).")
        return 'SPEAKER_NOT_FOUND'

    def match_timestamps_to_speakers(self, timestamps, speaker_info):
        """Match timestamps to speaker information and print the results."""

        start_timestamp, end_timestamp = timestamps.strip().split(' --> ')
        start_seconds = self.parse_timestamp(start_timestamp)
        end_seconds = self.parse_timestamp(end_timestamp)

        speaker = self.find_speaker(start_seconds, end_seconds, speaker_info)

        if self.hide_timestamps:
            new_line = speaker
        else:
            new_line = f"{start_timestamp} --> {end_timestamp} : {speaker}"

        return new_line

    def process_line(self, line,
                     speaker_info=None):

        if speaker_info is None:
            return line

        if line.__contains__(' --> '):
            new_line = self.match_timestamps_to_speakers(line, speaker_info)

            return new_line

        else:
            return line

    def get_speaker_info(self, diarization_path):

        if not os.path.exists(diarization_path):
            print(f"Speaker information file not found: {diarization_path}")
            return None

        with open(diarization_path, 'r') as f:
            speaker_def = f.readlines()

        # Parse speaker information
        speaker_info = []
        for line in speaker_def:
            info = self.parse_speaker_info(line)
            if info:
                speaker_info.append(info)
        return speaker_info

    # Pages creation elements
    def reset_canvas(self):
        self.pdf_canvas = None
        self.y_position = self.height - 30
        self.page_number = 1

    def add_footer(self):
        self.pdf_canvas.saveState()
        self.pdf_canvas.setFont("Helvetica", 9)

        self.pdf_canvas.drawString(self.pdf_canvas._pagesize[0] / 2, 20,
                                   f"Page {self.page_number}")

        self.pdf_canvas.restoreState()

    def add_page_title(self, title):
        self.pdf_canvas.saveState()

        self.pdf_canvas.setFont("Helvetica-Bold", 12)
        self.pdf_canvas.drawString(40,
                                   self.y_position,
                                   title)

        self.pdf_canvas.restoreState()

    def first_page(self, title, files_list):

        # first page with list of files
        self.pdf_canvas.setFont("Helvetica-Bold", 14)
        self.pdf_canvas.drawString(40, self.y_position, title)
        self.y_position -= 20

        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

        print("Processing files list for the table of content.")

        self.pdf_canvas.setFont("Helvetica", 10)
        for index, file_path in enumerate(files_list):
            file_name = os.path.basename(file_path)
            name_split = file_name.split('-')
            date_obj = datetime(int(name_split[0]), int(name_split[1]), int(name_split[2]))
            full_date = date_obj.strftime('%A %d %B')

            episode_name = ' '.join(name_split[3:]).replace(extension, '')
            line_content = f"{index}] Episode du {full_date} : {episode_name}"

            print(line_content)

            # manage page jump
            if self.y_position < 40:
                self.add_footer()
                self.pdf_canvas.showPage()
                self.page_number += 1
                self.y_position = self.height - 40


            # Write the file name and details
            self.pdf_canvas.drawString(40,
                                       self.y_position,
                                       line_content)

            self.y_position -= 12

    def create_pdf(self,
                   files_list,
                   with_diari = False):

        self.first_page("Lists des épisodes",
                        files_list)

        # write the total number of episodes

        self.y_position -= 20
        self.pdf_canvas.drawString(40, self.y_position,
                     f"Nombres d'épisodes : {len(files_list)}")

        self.add_footer()
        self.pdf_canvas.showPage()
        self.page_number += 1
        self.y_position = self.height - 30


        for file_path in files_list:
            transcript_file_name = os.path.splitext(os.path.basename(file_path))[0]
            diarization_file_name = f"{transcript_file_name}-diari.txt"
            diarization_path = os.path.join('transcript', 'diarization', diarization_file_name)

            transcript_content = self.read_file(file_path)
            if with_diari:
                speaker_info = self.get_speaker_info(diarization_path)
            else:
                speaker_info = None

            print(f"Processing: {file_path}", end='')
            self.add_page_title(transcript_file_name)

            self.y_position -= 8
            self.pdf_canvas.drawString(40,
                                       self.y_position,
                                       '-' * 150)
            self.y_position -= 6

            for line in transcript_content.splitlines():

                # print('.', end='')
                if self.y_position < 40:
                    self.add_footer()
                    self.pdf_canvas.showPage()
                    self.page_number += 1
                    self.y_position = self.height - 40

                if line in self.DO_NOT_PRINT:
                    continue

                if line == '':
                    continue

                if '-->' in line:
                    self.pdf_canvas.setFont("Helvetica", 5)
                else:
                    self.pdf_canvas.setFont("Helvetica", 10)

                #line_to_write = process_line(line)
                line_to_write = self.process_line(line,
                                                  speaker_info)

                self.pdf_canvas.drawString(40,
                                           self.y_position,
                                           line_to_write)
                self.y_position -= 12

            print(' done')

        self.add_footer()
        self.pdf_canvas.save()


if __name__ == "__main__":


    #model = "large-v3"
    model = "turbo"
    directory_input = f"transcript/{model}"
    #contains_list = ['Plutôt_Confinés_']
    with_diarization = True
    merge_speaker = True

    extensions = ["vtt",
                  #"txt",
                  #'srt',
                  #'tsv',
                  #'json'
                  ]

    # output_pdf_path = f"output_{contains}.pdf"
    # main(directory_input, output_pdf_path, extension, contains)

    output_dir = "transcript/"
    #if os.path.exists(output_dir):
    #    import shutil
    #    shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    optim_tool = OptimTool(directory_input,
                           output_dir,
                           model)

    # TODO separate folder with diarization addon
    # TODO separate folder with not pdf concat

    file_list = os.listdir(directory_input)

    for folder in file_list:
        print(f"------ Processing contains: {folder}")
        for extension in extensions:
            print(f"--- Processing extension: {extension}")
            optim_tool.execute(extension,
                               folder,
                               with_diarization,
                               merge_speaker)
