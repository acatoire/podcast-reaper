import os
import whisper
import time
from mutagen.mp3 import MP3
from whisper.utils import get_writer

# ask the root folder to work on
root_folder = input("Enter the path to the folder containing downloads folder: ").strip()

# Specify input and output directories
input_folder = root_folder + "/downloads"  # Replace with your folder containing MP3 files
output_folder = root_folder  # Base folder for transcripts
output_format = "all"
#model_size = input("Choose Whisper model size (1 for 'turbo', 2 for 'large-v3'): ")
#model_size = "turbo" if model_size == "1" else "large-v3"
model_size = "turbo"
language = "fr"
task = "transcribe"

# Get the maximum number of available threads
max_threads = os.cpu_count()
#print(f"Maximum available threads: {max_threads}")
#threads = input(f"Enter the number of threads to use (max {max_threads}): ") or str(max_threads)


# Load the Whisper model
def load_whisper_model(model_requested):
    local_model_path = model_requested + '.pt'

    # Check if the model file exists locally
    if os.path.exists(local_model_path):
        print(f"Loading Whisper model from local file: {local_model_path}")
        model_load = whisper.load_model(local_model_path)
    else:
        print(f"Downloading Whisper model: {model_requested}")
        model_load = whisper.load_model(model_requested)
        # Save the model locally
        # print(f"Saving Whisper model to: {local_model_path}")
        # model_load.save(local_model_path) # todo
    return model_load

print(f"Loading Whisper model: {model_size}")
model = load_whisper_model(model_size)

# List all MP3 files in the input folder
mp3_files = [filename for filename in os.listdir(input_folder) if filename.endswith(".mp3")]
mp3_to_process = []

# Print the list of MP3 files
print(f"Found {len(mp3_files)} MP3 files found")

for filename in mp3_files:
    base_name = os.path.splitext(filename)[0]
    date_name = filename[0:10]
    output_dir = os.path.join(output_folder, model_size, date_name)
    transcript_path = os.path.join(output_dir, f"{date_name}-transcript.txt")

    if not os.path.exists(transcript_path):
        mp3_to_process.append(filename)

print(f"Found {len(mp3_to_process)} MP3 files to process")

for index, filename in enumerate(mp3_to_process, start=1):
    print(f"{time.strftime('%H:%M:%S')} - {index/len(mp3_to_process)*100:.2f}% - {index}/{len(mp3_to_process)}: {filename}")
    date_name = filename[0:10]
    file_path = os.path.join(input_folder, filename)

    # Create output directory structure
    base_name = os.path.splitext(filename)[0]
    output_dir = os.path.join(output_folder, model_size, date_name)
    transcript_path = os.path.join(output_dir, f"{date_name}-transcript.txt")
    info_path = os.path.join(output_dir, f"{date_name}-info.txt")


    os.makedirs(output_dir, exist_ok=True)

    file_size_mb = round(os.path.getsize(file_path) / 1024 / 1024, 0)
    file_duration_mn = round(MP3(file_path).info.length / 60, 0)

    with open(info_path, "a", encoding="utf-8") as info_file:
        info_file.write(f"File: {filename} - {file_size_mb} MB - {file_duration_mn} minutes\n")
        info_file.write(f"Model: {model_size}\n")

    # Transcribe the MP3 file
    print(f"Transcribing {filename} size: {file_size_mb:.2f} MB, duration: {file_duration_mn:.2f} minutes.")
    start_time = time.time()
    result = model.transcribe(file_path,
                              language=language)
    end_time = time.time()
    execution_time = (end_time - start_time) / 60
    print(f"Transcription complete for {filename} in {execution_time:.2f} seconds.")

    # Save the transcript
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    output_writer = get_writer(output_format, output_dir)
    output_writer(result, date_name, {})

    with open(info_path, "a", encoding="utf-8") as info_file:
        info_file.write(f"Transcript Time: {execution_time:.2f} minutes\n")

print("All files processed.")
