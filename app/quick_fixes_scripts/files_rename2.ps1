# Define the folder path
$targetFolder = "C:\git\podcast-reaper\podcasts\plutot_caustique\turbo"

# Get all subfolders in the target directory
Get-ChildItem -Path $targetFolder -Directory | ForEach-Object {

    Write-Host "Processing folder: $( $_.FullName )"

    Get-ChildItem -Path $_.FullName -File -Filter *.vtt | ForEach-Object {
        $file = $_
        # Read the file content
        $content = Get-Content -Path $file.FullName -Raw

        # Check if the content contains the specific string
        if ($content -like "*File: *")
        {
            Write-Host "$( $_.FullName ) is a info file"

            # Delete this file as it is not needed
            Remove-Item -Path $file.FullName -Force
            Write-Host "Deleted: $( $file.Name )"
        }

        # Check if the content contains the specific string
        if ($content -like "*speaker_SPEAKER_0*")
        {
            Write-Host "$( $_.FullName ) is a diari file"

            # Delete this file as it is not needed
            Remove-Item -Path $file.FullName -Force
        }
    }
}
