# Define the target directory
$targetFolder = "./turbo"

# Get all .txt files in the target directory and its subdirectories
Get-ChildItem -Path $targetFolder -Recurse -Filter "*.txt" | ForEach-Object {
    # Check if the file contains the string 'speaker_SPEAKER'
    if (Select-String -Path $_.FullName -Pattern "speaker_SPEAKER" -Quiet) {
        # Construct the new file name with the .diari extension
        $newName = "$($_.DirectoryName)\$($_.BaseName).diari"

        # Rename the file
        Rename-Item -Path $_.FullName -NewName $newName
    }
}