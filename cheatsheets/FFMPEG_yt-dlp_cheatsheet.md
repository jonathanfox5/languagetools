---
title: FFMPEG / yt-dlp cheat sheet
author: Jonathan Fox
---

# FFMPEG

## Extract audio without re-encoding

```bash
ffmpeg -vn -acodec copy -i video.mp4 audio.aac
```

## Extract video + audio track for a given language

```bash
ffmpeg -i source.mp4 -map 0:v -map 0:a:m:language:ita -acodec copy -vcodec copy output.mp4
```

## Combine videos without re-encoding

First, create `vidlist.txt` with each file on a separate line.

```bash
ffmpeg -f concat -safe 0 -i vidlist.txt -c copy output.mp4
```

## Trim video without re-encoding

```bash
ffmpeg -i input.mp4 -ss 00:01:19 -to 00:16:13 \
-c:v copy -c:a copy output.mp4
```

## Convert all files in a directory

Note: this specific snippet won't work on Windows unless a bash terminal is used.

```bash
for i in *.ogg; do ffmpeg -i "$i" "${i%.*}.mp3"; done
rm *.ogg
```

## Transcoding low quality content (e.g. video rips)

```bash
ffmpeg -i original.mp4 -c:v hevc_nvenc -rc vbr -cq 30 -sn -c:a libfdk_aac -vbr 3 output.mp4
```

# yt-dlp

## Extract audio from youtube video in mp3 format

```bash
yt-dlp -x --audio-format mp3 '[youtube url]'
```

## List available subtitles

```bash
yt-dlp --list-subs '[youtube_url]'

```

## Download video plus english subtitles

```bash
yt-dlp --sub-lang=en '[youtube_url]'
```

## Download all subs but not the video

```bash
yt-dlp --all-subs --write-auto-sub --skip-download '[youtube_url]'
```

## List available formats

```bash
yt-dlp -F '[youtube_url]'

```

## Variations on best quality

Note that:

1. `best` selects the best overall format
2. `bestaudio + bestvideo` downloads them separately and merges
3. `bestvideo, bestaudio` downloads them but doesn't merge.
4. `bv+ba/b` downloads them separately but will download the best combined format if video only isn't available
5. You can specify the best file of a specific type
6. `bestaudio` downloads audio only

The comma and plus notation also works with format codes.

```bash
yt-dlp -f best '[youtube_url]'

yt-dlp -f 'bestvideo+bestaudio' '[youtube_url]'
yt-dlp -f 'bestvideo,bestaudio' '[youtube_url]'
yt-dlp -f 'bv+ba/b' '[youtube_url]'

yt-dlp -f 'best[ext=mp4]' '[youtube_url]'
yt-dlp -f 'bestaudio' '[youtube_url]'

```

## List available formats

```bash
yt-dlp -F '[youtube_url]'

```

## Some flags for -o option for specifying file names

- `%(title)s` The title of the video or playlist.
- `%(uploader)s` The name of the video or playlist uploader.
- `%(upload_date)s` The date on which the video or playlist was uploaded.
- `%(playlist)s` The name of the playlist, if the video is part of a playlist.
- `%(ext)s` The file extension of the downloaded video or audio file.

# Building this pdf

```bash
pandoc --defaults=pdf.yaml FFMPEG_yt-dlp_cheatsheet.md \
-o FFMPEG_yt-dlp_cheatsheet.pdf
```
