import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import dropbox


PAGE_URL = "https://easyitaliannews.com"

# Temp output is a local folder where the output of the script can easily be inspected
# Archive is the main directory where data is kept for later reference
TEMP_OUTPUT_DIRECTORY = "output/"
ARCHIVE_DIRECTORY = "/private/var/mobile/Library/Mobile Documents/com~apple~CloudDocs/Italian/_Media/Easy Italian News/"

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

TEMPLATE = """<html>
<header><title>{}</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></header>
<body>{}</body>
</html>
"""

DROPBOX_FOLDER = "/EIN/"


def main():
    # Delete existing files in the output to make it easier to find current episode
    print("Clearing temp output directory")
    delete_all_files_in_directory(TEMP_OUTPUT_DIRECTORY)

    # Get main page as a parsable object
    print("Downloading html")

    page_response = requests.get(PAGE_URL)

    # Process the page with bs4
    print("Processing page")

    page = BeautifulSoup(page_response.content, "html.parser")

    # Grab date of article to use in file names and header
    date_string = page.select_one(".entry-time").get("datetime")[:10]
    file_stem = "EIN_" + date_string

    # Wrap the H4s in paragraphs to make parsing easier
    h4_tags = page.find_all("h4")

    for h4_tag in h4_tags:
        h4_tag.wrap(page.new_tag("p"))

    # Get article content
    title = page.select_one(".entry-title-link").text
    content = page.select_one(".entry-content")
    paragraphs = content.select("p")

    # Loop through paragraphs and format article content into style
    i = 0
    body = ""
    for para in paragraphs:
        # Ignore first 2 paragraphs
        i += 1
        if i <= 2:
            continue

        # Flag features to skip or parse differently
        strong_flag = para.select_one("strong")
        a_flag = para.select_one("a")
        img_flag = para.select_one("img")

        # Skip paragraphs containing the following
        if img_flag or a_flag or strong_flag:
            continue

        # Extract text from paragraph and clean
        t = para.get_text(separator="\n").strip()

        # Skip text in the filter list
        if t in FILTER_OUT:
            continue

        # Extract data to create headers and content
        body += para.prettify()

    # Write html file. Force utf-8 for iOS compatibility
    print("Writing html file")

    output = TEMPLATE.format(title, body).encode("utf-8")

    html_filename = file_stem + ".html"

    save_file(TEMP_OUTPUT_DIRECTORY + html_filename, output, True)
    save_file(ARCHIVE_DIRECTORY + html_filename, output, True)

    # Download audio
    print("Downloading audio")

    audio_filename = file_stem + ".mp3"
    audio_path = TEMP_OUTPUT_DIRECTORY + audio_filename

    audio_url = page.select_one("audio a").text
    audio_response = requests.get(audio_url)

    save_file(TEMP_OUTPUT_DIRECTORY + audio_filename, audio_response.content, True)
    save_file(ARCHIVE_DIRECTORY + audio_filename, audio_response.content, True)

    # Save to dropbox
    print("Uploading html and audio to dropbox")
    upload_to_dropbox(output, html_filename, DROPBOX_FOLDER)
    upload_to_dropbox(audio_response.content, audio_filename, DROPBOX_FOLDER + "Audio/")

    print("Done")

    return True


def upload_to_dropbox(data, filename, dropbox_path="/"):
    # Get data from .env file (or command line)
    load_dotenv()
    db_token = os.getenv("DB_TOKEN")
    db_key = os.getenv("DB_KEY")
    db_secret = os.getenv("DB_SECRET")

    # Connect and upload
    dbx = dropbox.Dropbox(
        oauth2_refresh_token=db_token, app_key=db_key, app_secret=db_secret
    )
    dbx.files_upload(data, dropbox_path + filename, dropbox.files.WriteMode.overwrite)

    return True


def delete_all_files_in_directory(directory):
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))

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
