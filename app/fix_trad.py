import os
import re

# Prompt the user for the target directory
target_directory = input("Enter the target directory path: ")

# Walk through the directory and process all translated_*.vtt files
for root, _, files in os.walk(target_directory):
    for file in files:
        if file.startswith("translated_") and file.endswith(".vtt"):
            file_path = os.path.join(root, file)

            # Read the file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace > followed by any type of newline and <c.fr> with >\r\n<c.en>
            updated_content = re.sub(r">\s<c\.fr>", r">\n<c.en>", content, flags=re.DOTALL)
            # updated_content = re.sub(r">\s\s<c\.en>", r">\n<c.en>", content, flags=re.DOTALL)
            updated_content = re.sub(r">\s<c\.en>", r">\n<c.en>", updated_content, flags=re.DOTALL)

            # Write the updated content back to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)

            print(f"Processed: {file_path}")

print("Replacement completed.")
