if ($args.count -eq 0) {
    Write-Host "Usage: hash <file>"
    exit
}

$file_name = $args[0]

$md5 = Get-FileHash -Path $file_name -Algorithm MD5
$sha1 = Get-FileHash -Path $file_name -Algorithm SHA1
$sha256 = Get-FileHash -Path $file_name -Algorithm SHA256
$sha512 = Get-FileHash -Path $file_name -Algorithm SHA512

Write-Host "MD5: $($md5.Hash)"
Write-Host "SHA1: $($sha1.Hash)"
Write-Host "SHA256: $($sha256.Hash)"
Write-Host "SHA512: $($sha512.Hash)"