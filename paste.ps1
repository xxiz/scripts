param([string]$File)

$instance = "YOUR_HASTE_SERVER" # https://github.com/toptal/haste-server
$apiEndpoint = "$instance/documents"

$content = Get-Content $File -Raw
$response = Invoke-WebRequest -Method POST -Uri $apiEndpoint -Body $content

$jsonObject = $response.Content | ConvertFrom-Json
$extension = $File -split "\." | Select-Object -Last 1
$result = "$instance/$($jsonObject.key).$extension"

Write-Host "Visible at: $result"
Set-Clipboard -Value $result