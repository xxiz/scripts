# To run this script, simply open Powershell and type: .\wfetch.ps1
# Alternativley to run this script on startup, add it to your profile (https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/ise/how-to-use-profiles-in-windows-powershell-ise?view=powershell-7.3)
cimSession = New-CimSession
$m = Get-CimInstance -ClassName Win32_OperatingSystem -Property TotalVisibleMemorySize,FreePhysicalMemory -CimSession $cimSession
$total = $m.TotalVisibleMemorySize / 1mb
$used = ($m.TotalVisibleMemorySize - $m.FreePhysicalMemory) / 1mb
$usage = [math]::floor(($used / $total * 100))
$gpu = wmic path win32_VideoController get name | grep NVIDIA
Write-Host (Get-CimInstance -ClassName Win32_Processor -Property Name -CimSession $cimSession).Name
Write-Host $gpu
Write-Host "PowerShell v$($PSVersionTable.PSVersion)"
Write-Host "$usage% @ " "$($used.ToString("#.##")) GiB / $($total.ToString("#.##")) GiB"