import yt_dlp

# Configure inputs
from url_list import links as URLS

SEASON = 1
NUMBER_EPISODES_FROM = 1
DIRECTORY = "output"

episode = NUMBER_EPISODES_FROM
for url in URLS:
    file_name = f"{DIRECTORY}/S{SEASON:02}E{episode:02} %(title)s.%(ext)s"

    options = {"verbose": True, "outtmpl": file_name}

    ydl = yt_dlp.YoutubeDL(options)
    ydl.download(url)

    episode += 1
