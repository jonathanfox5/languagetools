import re, pathlib

import requests
from bs4 import BeautifulSoup


RSS_URL = "https://feeds.blubrry.com/feeds/podcastitaliano.xml"

FILTER_FOR = ["Principiante"]
FILTER_OUT = []

SAVE_DIRECTORY = "/Users/jonathan/iCloud/Italian/_Media/Podcast Italiano/Principiante/"

# For podcasts that have the episode number at the end, tries to find the final number and add to start of filename
GRAB_FINAL_NUMBER = True


def main():
    # Get main page as a parsable object and extract episode data
    rss_response = requests.get(RSS_URL)
    rss = BeautifulSoup(rss_response.content, "html.parser")
    episodes = rss.select("item")

    # Download episodes if they pass the filtering stage
    for episode in episodes:
        # Extract data
        title = episode.select_one("title").text.strip()
        link = episode.select_one("enclosure").get("url").strip()
        file_type = get_file_extension(link)

        # Check if we want want the episode, otherwise move on to the next one
        if not passes_filter(title, FILTER_FOR, FILTER_OUT):
            continue

        # For podcasts that have the episode number at the end, tries to find the final number and add to start of filename
        final_no = ""
        if GRAB_FINAL_NUMBER:
            final_no = get_final_number(title)

            if final_no:
                final_no = final_no.rjust(3, "0")

        file_name = SAVE_DIRECTORY + clean_filename(final_no + " " + title + file_type)

        # Download episode
        print(title)
        print(link)
        print(file_name)
        print("\n")

        save_episode(link, file_name)


def save_episode(link, file_name):
    audio_response = requests.get(link).content

    save_file(file_name, audio_response, True)


def get_final_number(input):
    final_no = ""

    try:
        final_no = re.findall(r"\d+", input)[-1]
    except:
        pass

    return final_no


def get_file_extension(file_name):
    ext = pathlib.Path(file_name).suffix

    return ext


def clean_filename(filename):
    # Reference: https://en.wikipedia.org/wiki/Filename#Reserved_characters_and_words
    clean = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", filename).strip()

    return clean


def passes_filter(input, filter_in, filter_out):
    # Capitalise to make case insensitive
    input = input.upper()

    # First, check that there is nothing that we want to filter out
    for filter in filter_out:
        filter = filter.upper()

        if filter in input:
            return False

    # Return true if in filter_in, otherwise return false
    for filter in filter_in:
        filter = filter.upper()

        if filter in input:
            return True

    return False


def save_file(filename, data, write_binary):
    write_type = "w"
    if write_binary:
        write_type = "wb"

    with open(filename, write_type) as f:
        f.write(data)

    return True


if __name__ == "__main__":
    main()
