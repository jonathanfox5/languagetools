import subprocess

import requests
from bs4 import BeautifulSoup


PAGE_URL = "https://easyitaliannews.com"
SAVE_DIRECTORY = "/Users/Jonathan/iCloud/Italian/_Media/Easy Italian News/"

FILTER_OUT = [
    "Click the link below to listen to a recording of the text as you read it.",
    "Subscribe to receive each bulletin via email (free!)",
    "Know others who’d enjoy EasyItalianNews.com? Forward this email!",
    "Donations pay our writers and editorial staff. You could help, too!",
    "Ti chiediamo il tuo aiuto!",
    "We need your help!",
    "Cerchiamo sostenitori di Easy Italian News!",
    "Easy Italian News is looking for supporters!",
    "We’ll be grateful!",
]

HEADER = """---
title: {}
author: EasyItalianNews.com
language: it-IT
date: {}
toc: true
cover-image: /Users/Jonathan/iCloud/Italian/_Media/Easy Italian News/ein_cover.png
...

"""


def main():
    # Get main page as a parsable object
    page_response = requests.get(PAGE_URL)
    page = BeautifulSoup(page_response.content, "html.parser")

    # Grab date of article to use in file names and header
    date_string = page.select_one(".entry-time").get("datetime")[:10]
    file_stem = "EIN_" + date_string

    # Download audio
    # audio_url = page.select_one("audio a").text
    # audio_response = requests.get(audio_url)
    # save_file(SAVE_DIRECTORY + file_stem + ".mp3", audio_response.content, True)

    # Wrap the H4s in paragraphs to make parsing easier
    h4_tags = page.find_all("h4")

    for h4_tag in h4_tags:
        h4_tag.wrap(page.new_tag("p"))

    # Get article content
    title = page.select_one(".entry-title-link").text
    content = page.select_one(".entry-content")
    paragraphs = content.select("p")

    # Build output, starting with header
    title = (
        "Easy Italian News "
        + date_string
        + " - "
        + title.replace("EasyItalianNews.com ", "")
    )
    header = HEADER.format(title, date_string)

    # Loop through paragraphs and format article content into style
    i = 0
    last_strong = ""
    body = ""
    for para in paragraphs:
        # Ignore first 2 paragraphs
        i += 1
        if i <= 2:
            continue

        # Flag features to skip or parse differently
        strong_flag = para.select_one("strong")
        h4_flag = para.select_one("h4")
        a_flag = para.select_one("a")
        img_flag = para.select_one("img")

        # Skip paragraphs containing the following
        if img_flag or a_flag:
            continue

        # Extract text from paragraph and clean
        t = para.get_text(separator="\n").strip()

        # Skip text in the filter list
        if t in FILTER_OUT:
            continue

        # Extract data to create headers and content
        # Merge strong and h4 paragraphs to create headers
        if strong_flag:
            last_strong = t
        elif h4_flag:
            next_line = "\n\n# " + last_strong + ": " + t + "\n\n"

            body += next_line
            last_strong = ""
        else:
            next_line = t + "\n\n\n"
            body += next_line

    # Write md file and convert to epub
    markdown = SAVE_DIRECTORY + file_stem + ".md"
    epub = SAVE_DIRECTORY + file_stem + ".epub"

    output = header + body

    save_file(markdown, output, False)
    subprocess.run(["pandoc", markdown, "-o", epub])

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
