# Prompt the user for the target directory
$targetDirectory = Read-Host "Enter the target directory path"

# Get all .vtt files in the target directory and its subdirectories
Get-ChildItem -Path $targetDirectory -Recurse -Filter translated_*.vtt | ForEach-Object {
    # Read the file content
    $content = Get-Content -Path $_.FullName -Raw

    # Replace > followed by any type of newline and <c.fr> with > followed by the same newline and <c.en>
    # $updatedContent = $content -replace "</c><c.en>", "</c>\r\n<c.en>"
    $updatedContent = $content -replace ">\r\n<", ">`r`n<"
    # $updatedContent = $content -replace ">(\r?\n)<c.fr>", ">$1<c.en>"

    # Write the updated content back to the file
    Set-Content -Path $_.FullName -Value $updatedContent

    Write-Host "Processed: $($_.FullName)"
}

Write-Host "Replacement completed."