import os, subprocess, pathlib

import pysrt


INPUT_DIRECTORY = (
    "/Users/jonathan/iCloud/Italian/_Media/Immersion Videos/Pokemon S01/Netflix subs/"
)
SAVE_DIRECTORY = INPUT_DIRECTORY
FILE_NAME_STEM = "Pokemon Season 1 Transcripts"

HEADER = """---
title: Pokémon Season 1 Transcripts
author: Subtitles
language: it-IT
toc: true
cover-image: /Users/jonathan/iCloud/Italian/_Media/Immersion Videos/Pokemon S01/pokemon_s01_cover.png
...

"""


def main():
    # Get list of subtitle files
    files = sorted(os.listdir(INPUT_DIRECTORY))

    # Process all subtitle files
    body = ""
    for file in files:
        print(file)

        # Ignore non-srt files
        if not pathlib.Path(file).suffix.upper() == ".SRT":
            print("Ignored")
            continue

        chapter = ""

        title = pathlib.Path(file).stem
        title = title[12 : (len(title) - 27)]
        chapter += "# " + title + "\n\n"

        chapter += srt_to_txt(INPUT_DIRECTORY + file)

        body += chapter

    # Tidy up the markdown
    body = body.replace("-", "–")
    body = body.replace("[", "*[")
    body = body.replace("]", "]*")

    # Put final md together
    output = HEADER + body

    # Write md file and convert to epub
    print("Saving md and epub")
    markdown_filename = SAVE_DIRECTORY + FILE_NAME_STEM + ".md"
    epub_filename = SAVE_DIRECTORY + FILE_NAME_STEM + ".epub"

    save_file(markdown_filename, output, False)
    convert_to_epub(markdown_filename, epub_filename)

    return True


def convert_to_epub(markdown_filename, epub_filename):
    subprocess.run(["pandoc", markdown_filename, "-o", epub_filename])

    return True


def srt_to_txt(srt_filename):
    subs = pysrt.open(srt_filename)

    text = ""
    for sub in subs:
        text += sub.text + "\n\n"

    return text


def save_file(filename, data, write_binary):
    write_type = "w"
    if write_binary:
        write_type = "wb"

    with open(filename, write_type) as f:
        f.write(data)

    return True


if __name__ == "__main__":
    main()
