import os

# https://github.com/argosopentech/argos-translate


# To enable GPU support, set the ARGOS_DEVICE_TYPE env variable to cuda
os.environ["ARGOS_DEVICE_TYPE"] = "cuda"  # or "cpu" for CPU support

import argostranslate.package
import argostranslate.translate

input_folder = (
        input("Enter the path to the folder containing transcripts (default: ./transcript/turbo): ")
        or "./transcript/turbo")

from_code = "fr"
to_code = "en"

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
translatedText = argostranslate.translate.translate("Bien venue dans le traducteur de vtt", from_code, to_code)
print(translatedText)

# For each folder in the input folder, open the vtt file and translate it lien per lines
# List all folders in the input folder
folders = [folder for folder in os.listdir(input_folder) if
           os.path.isdir(os.path.join(input_folder, folder))]

print(f"Found {folders.__len__()} Folders:")

for index_folder, folder in enumerate(folders, start=1):

    print(f"{index_folder}/{len(folders)}: {folder}")
    folder_path = os.path.join(input_folder, folder)

    # List all files in the folder
    files = [filename for filename in os.listdir(folder_path)
             if (filename.endswith(".vtt") and
                 not filename.startswith("translated_"))]

    print(f"Found {files.__len__()} vtt file:")
    for index_file, filename in enumerate(files, start=1):
        print(f"{index_file}/{len(files)}: {filename}")
        file_path = os.path.join(folder_path, filename)
        output_file = f"translated_{filename}"

        # Check if the file is already translated
        if os.path.exists(os.path.join(folder_path, output_file)):
            print(f"Translated file already exists: {output_file}, skipping.")
            continue

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the file content line by line
            translated_content = ""
            for line in file:
                if " --> " in line or line.strip() == "":
                    translated_content += line  # Write the line as is
                else:
                    # remove last return if present
                    line = line.rstrip()

                    # Translate the content
                    translated_content += "<c.fr>" + line + "</c>\n"
                    translated_content += "<c.en>" + argostranslate.translate.translate(line, from_code,
                                                                                        to_code) + "</c>\n"

        # Save the translated content to a new file
        translated_file_path = os.path.join(folder_path, output_file)
        with open(translated_file_path, 'w', encoding='utf-8') as translated_file:
            translated_file.write(translated_content)
