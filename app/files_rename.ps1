# Define the target directory
$targetFolder = "../podcasts/pardon_gpt/turbo"

# Get all subfolders in the target directory
Get-ChildItem -Path $targetFolder -Directory | ForEach-Object {
    # Extract the date prefix from the folder name (first 10 characters)
    $datePrefix = $_.Name.Substring(0, 10)

    # Get all matching files in the current folder
    Get-ChildItem -Path $_.FullName -File | ForEach-Object {
        if ($_.Name -in "info.txt", "transcript.txt") {
            # Add the date before the name for specific files
            $newName = "$datePrefix-$($_.Name)"
        }

        # Rename the file
        Rename-Item -Path $_.FullName -NewName $newName
    }

    # Get all matching files in the current folder
    Get-ChildItem -Path $_.FullName -File | Where-Object {
        ($_.Extension -in ".json", ".srt", ".tsv", ".txt", ".vtt", ".diari") -and
                ($_.Name -notin "*info.txt", "*transcript.txt")
    } | ForEach-Object {
        # Construct the new file name with only the date and extension
        $newName = "$datePrefix$($_.Extension)"

        # Rename the file
        Rename-Item -Path $_.FullName -NewName $newName
    }
}