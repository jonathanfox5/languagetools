# Note, some manual trying up required afterwards.
# Use pandoc to convert to epub
# Prettier in vscode is also handy!

import requests
from bs4 import BeautifulSoup

PAGE_URLS = [
    "https://www.podcastitaliano.com/podcast-episode/la-storia-di-italo-capitolo-1",
    "https://www.podcastitaliano.com/podcast-episode/la-storia-di-italo-capitolo-2",
    "https://www.podcastitaliano.com/podcast-episode/la-storia-di-italo-capitolo-3",
    "https://www.podcastitaliano.com/podcast-episode/la-storia-di-italo-capitolo-4",
    "https://www.podcastitaliano.com/podcast-episode/la-storia-di-italo-capitolo-5",
    "https://www.podcastitaliano.com/podcast-episode/11-lettera-da-davide",
    "https://www.podcastitaliano.com/podcast-episode/12-lettera-da-budapest",
    "https://www.podcastitaliano.com/podcast-episode/13-lettera-dal-caffe",
    "https://www.podcastitaliano.com/podcast-episode/15-lettera-dalla-mia-stanza",
    "https://www.podcastitaliano.com/podcast-episode/14-lettera-dal-pullman",
    "https://www.podcastitaliano.com/podcast-episode/16-cartolina-dalla-montagna",
    "https://www.podcastitaliano.com/podcast-episode/17-cartolina-dal-mare",
    "https://www.podcastitaliano.com/podcast-episode/18-cartolina-dal-lago",
    "https://www.podcastitaliano.com/podcast-episode/19-cartolina-dalla-campagna",
    "https://www.podcastitaliano.com/podcast-episode/20-cartolina-da-roma",
    "https://www.podcastitaliano.com/podcast-episode/21-lettera-dal-treno",
    "https://www.podcastitaliano.com/podcast-episode/22-lettera-dal-parco",
    "https://www.podcastitaliano.com/podcast-episode/23-lettera-dalla-casa-in-montagna",
    "https://www.podcastitaliano.com/podcast-episode/24-lettera-dal-fiume",
    "https://www.podcastitaliano.com/podcast-episode/25-lettera-alla-fine-dellestate",
]
SAVE_DIRECTORY = "/Users/jonathan/iCloud/Italian/_Media/Podcast Italiano/Principiante/"

FILE_NAME = "PrincipiateMerged.md"

HEADER = """---
title: Podcast Italiano - Principante
author: Davide Gemello
language: it-IT
toc: true
cover-image: principiante_cover.png
...

"""


def main():
    # File that will eventually turn into the md file, ready for conversion
    output = HEADER

    for episodes in PAGE_URLS:
        # Get main page as a parsable object
        page_response = requests.get(episodes)
        page = BeautifulSoup(page_response.content, "html.parser")

        # Get article content
        title = page.select_one("title").text.strip()
        content = page.select_one("div.espisode-trascrizione-locked")
        print(title)

        # Remove the text that tells you to log in
        content.select_one("div.episode-locked-gradient").extract()

        # Remove english translations that are in italics
        em_tags = content.find_all("em")
        for em_tag in em_tags:
            em_tag.extract()

        # Build output
        chapter_title = "# " + title[1:] + "\n"
        chapter = chapter_title
        chapter += content.get_text(separator="\n\n") + "\n\n"

        output += chapter

    # Write file
    save_file(SAVE_DIRECTORY + FILE_NAME, output, False)

    return True


def save_file(filename, data, write_binary):
    write_type = "w"
    if write_binary:
        write_type = "wb"

    with open(filename, write_type) as f:
        f.write(data)

    return True


if __name__ == "__main__":
    main()
