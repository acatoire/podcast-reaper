
#
# https://github.com/pyannote/pyannote-audio?tab=readme-ov-file


import os
import torch
import torchaudio
from pyannote.audio import Pipeline

USE_AUTH_TOKEN=os.getenv("HUGGINGFACE_ACCESS_TOKEN")
print(USE_AUTH_TOKEN)

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=USE_AUTH_TOKEN)

input_folder = "downloads"
output_folder = os.path.join("transcript", "diarization")


# List all MP3 files in the input folder
mp3_files = [filename for filename in os.listdir(input_folder) if filename.endswith(".mp3")]

for file_name in os.listdir(input_folder):
    if not file_name.endswith(".mp3"):
        continue

    file_path = os.path.join(input_folder, file_name)
    diarization_output = os.path.join(output_folder, file_name.replace('.mp3', '-diari.txt'))

    if os.path.exists(diarization_output):
        print(f"Diarization already exists for {file_name}, skipping.")
        continue

    # send pipeline to GPU (when available)
    if torch.cuda.is_available():
        print("GPU available. Sending pipeline to GPU.")
        pipeline.to(torch.device("cuda"))

    print(f"Diarization started for {file_name}...", end="")

    # apply pretrained pipeline
    waveform, sample_rate = torchaudio.load(file_path)
    diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})

    print(f"... completed. Saving in file{diarization_output}")

    # print the result
    with open(diarization_output, "a") as f:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
                output = f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}"
                print('.', end='')
                f.write(output + "\n")
    print(" done.")
