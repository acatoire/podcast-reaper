# Define the source and destination directories
$sourceFolder = "./diarization"
$destinationFolder = "./turbo"

# Get all files in the source folder
Get-ChildItem -Path $sourceFolder -File | ForEach-Object {
    # Extract the date prefix from the file name (first 10 characters)
    $datePrefix = $_.Name.Substring(0, 10)

    # Search for a folder that starts with the date prefix
    $targetFolder = Get-ChildItem -Path $destinationFolder -Directory | Where-Object {
        $_.Name -like "$datePrefix*"
    } | Select-Object -First 1

    # Check if a matching folder was found
    if ($targetFolder -ne $null) {
        # Move the file to the matching folder
        Move-Item -Path $_.FullName -Destination $targetFolder.FullName
    } else {
        Write-Host "Target folder does not exist: $datePrefix"
    }
}