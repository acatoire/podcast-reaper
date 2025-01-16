"""
This script reads all files in a given directory and its subdirectories,
concatenates their content, and creates a PDF file with the content of the chosen extension files.
"""
import json
import os
import glob
import re


class OptimTool:

    DO_NOT_PRINT = ["WEBVTT"]

    def __init__(self,
                 input_path,
                 output_path,
                 model_name):

        self.hide_timestamps = True

        self.directory_input = input_path
        self.output_dir = output_path
        self.model = model_name

        self.file_dict = {}

    def execute(self,
                ext,
                folder_ep,
                with_diari=False,
                with_merge=False):

        print("\n\n----------------------------------------")
        print(f"Optimization for {folder_ep} with {ext} extension.")

        # Find all files in the given directory and its subdirectories
        files = self.find_files(folder_ep, ext)

        if len(files) != 1:
            raise ValueError(f"Only one file expected in the folder {folder_ep} with extension {ext}.")

        output_file = f"{self.output_dir}/{self.model}-{ext}/{self.model}-{folder_ep}-{ext}"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Read file content
        if ext == 'json':
            file_content = json.loads(self.read_file(files[0])) # FIXME store start and end as miliseconds
            file_content.pop('text')
            file_content = file_content['segments']
        else:
            # TODO see for others extensions
            raise ValueError(f"Extension {ext} not supported.")

        # Read diarization speaker as dict
        if with_diari:
            diarization_file = os.path.join('transcript',
                                            'diarization',
                                            f'{folder_ep}-diari.txt')
            diarization_speaker = self.get_speaker_info(diarization_file)

            if with_merge:
                for line in file_content:
                    print(f"DEBUG : line - {line}")
                    speaker = self.find_speaker(line['start'], line['end'], diarization_speaker)
                    line['speaker'] = speaker

        # store new file
        with open(output_file, 'w') as file_handler:
            json.dump(file_content, file_handler)

    def find_files(self,
                   sub_folder,
                   ext):

        print("Find all .vtt files in the given directory and its subdirectories.")
        ext_files = glob.glob(os.path.join(self.directory_input,
                                           sub_folder,
                                           '**',
                                           f'*.{ext}'),
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
            return {'start': int(float(start)*1000),
                    'stop': int(float(stop)*1000),
                    'speaker': speaker}
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
            raise FileNotFoundError(f"Speaker information file not found: {diarization_path}")

        with open(diarization_path, 'r') as f:
            speaker_def = f.readlines()

        # Parse speaker information
        speaker_info = []
        for line in speaker_def:
            info = self.parse_speaker_info(line)
            if info:
                speaker_info.append(info)
        return speaker_info


if __name__ == "__main__":


    #model = "large-v3"
    model = "turbo"
    directory_input = f"transcript/{model}"
    output_dir = "transcript/"
    
    with_diarization = True
    merge_speaker = True

    extensions = [#"vtt",
                  #"txt",
                  #'srt',
                  #'tsv',
                  'json'
                  ]

    os.makedirs(output_dir, exist_ok=True)

    optim_tool = OptimTool(directory_input,
                           output_dir,
                           model)

    # TODO separate folder with diarization addon
    # TODO separate folder with not pdf concat

    folder_list = os.listdir(directory_input)

    for folder in folder_list:
        print(f"------ Processing contains: {folder}")
        for extension in extensions:
            print(f"--- Processing extension: {extension}")
            optim_tool.execute(extension,
                               folder,
                               with_diarization,
                               merge_speaker)
