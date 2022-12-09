if ($args.count -eq 0) {
    Write-Host "Usage: mp3 <url>"
    exit
}

$song_link = $args[0]

$domain = $song_link -replace "https://", "" -replace "http://", "" -replace "www.", "" -replace "/.*", ""

if ($domain -eq "youtube.com") {
    yt-dlp --newline -i -o "C:\Users\Ashwi\Documents\Spotify\RAW\%(title)s.%(ext)s" -x --audio-format mp3 --ignore-config --hls-prefer-native "https://www.youtube.com/watch?v=JLOVIDUQpM4" --verbose 
}

if ($domain -eq "soundcloud.com") {
    scdl -l $song_link --path "C:\Users\Ashwi\Documents\Spotify\RAW"
}