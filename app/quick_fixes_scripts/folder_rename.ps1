# Define the target directory
$targetFolder = "../podcasts/pardon_gpt/turbo"

# Get all subfolders in the target directory
Get-ChildItem -Path $targetFolder -Directory | ForEach-Object {
    # Extract the date prefix from the folder name (first 10 characters)
    $datePrefix = $_.Name.Substring(0, 10)

    # Construct the new folder name with the date prefix
    $newFolderName = "$datePrefix"
    echo "Renaming folder: $($_.Name) to $newFolderName"

    # Check if the new name is different from the current name
    if ($_.Name -ne $newFolderName) {
        # Rename the folder
        Rename-Item -Path $_.FullName -NewName $newFolderName
    }
}