if ($args.count -lt 1) {
    Write-Host "Not enough arguments supplied"
    exit
}

$lang = $args[0]
$question = $args[1..$args.Length] -join "+"
curl cht.sh/$lang/$question