import os

# https://github.com/argosopentech/argos-translate


# To enable GPU support, set the ARGOS_DEVICE_TYPE env variable to cuda
os.environ["ARGOS_DEVICE_TYPE"] = "cuda"  # or "cpu" for CPU support

import argostranslate.package
import argostranslate.translate

input_folder = (input("Enter the path to the folder containing transcripts folder: "))

transcript_folder = os.path.join(input_folder, "turbo")

if not os.path.exists(transcript_folder):
    print(f"Error: The folder {transcript_folder} does not exist.")
    exit(1)

from_code = "fr"
to_code = "en"

print(f"Translate from {from_code} to {to_code}")

# Download and install Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

# Translate
translatedText = argostranslate.translate.translate(
    "Bien venue dans le traducteur de vtt, c'est un test avant de commencer.", from_code, to_code)
print(translatedText)

# For each folder in the input folder, open the vtt file and translate it lien per lines
# List all folders in the input folder
folders = [folder for folder in os.listdir(input_folder) if
           os.path.isdir(os.path.join(input_folder, folder))]

print(f"Found {folders.__len__()} Folders:")

initial_files = []
final_list_to_process = []

for folder in folders:
    # List all files in the folder
    files = [os.path.join(input_folder, folder, filename) for filename in os.listdir(os.path.join(input_folder, folder))
             if (filename.endswith(".vtt") and
                 not filename.startswith("translated_"))]

    initial_files += files

print(f"Found {len(initial_files)} vtt files")

for filepath in initial_files:
    output_path = os.path.join(os.path.dirname(filepath),
                               "translated_" + os.path.basename(filepath))

    # Check if the file is already translated
    if not os.path.exists(output_path):
        final_list_to_process += [filepath]

print(f"Found {len(final_list_to_process)} vtt to process")

for index_file, filepath in enumerate(final_list_to_process, start=1):
    print(f"{index_file}/{len(final_list_to_process)}: {filepath}")
    output_path = os.path.join(os.path.dirname(filepath),
                               "translated_" + os.path.basename(filepath))

    # Read the file content
    with open(filepath, 'r', encoding='utf-8') as file:
        # Read the file content line by line
        translated_content = ""
        for line in file:
            if (" --> " in line or
                    line.strip() == "" or
                    'WEBVTT' in line):
                # Write the line as is
                translated_content += line  # Write the line as is
            else:
                # remove last return if present
                line = line.rstrip()
                # Write the input line as french
                translated_content += "<c.fr>" + line + "</c>\n"
                # Translate the content
                translated_content += "<c.en>" + argostranslate.translate.translate(line, from_code,
                                                                                    to_code) + "</c>\n"

        # Save the translated content to a new file
        with open(output_path, 'w', encoding='utf-8') as translated_file:
            translated_file.write(translated_content)
