import re, os, pathlib

DIRECTORY = "/Users/jonathan/iCloud/Italian/_Media/Immersion Videos/Easy Italian/"

FIRST_REGEX = "(?<=｜)(.*?)(?=\[)"
LAST_REGEX = ".+?(?=｜)"

FORMAT_NUMBER_IN_FIRST = True
NUMBER_OF_ZEROS = 3


def main():
    for file in os.listdir(DIRECTORY):
        print(file)

        file_path = pathlib.Path(file)
        file_ext = file_path.suffix
        file_stem = file_path.stem

        # Laziest thing ever
        try:
            first_part = re.findall(FIRST_REGEX, file_stem)[0].strip()

            if FORMAT_NUMBER_IN_FIRST:
                final_number = re.findall("\d+", first_part)[-1].rjust(
                    NUMBER_OF_ZEROS, "0"
                )
                non_number = "".join(re.findall("[^0-9]", first_part)).strip()

                first_part = non_number + " " + final_number

            last_part = re.findall(LAST_REGEX, file_stem)[0].strip()

            new_path = (
                DIRECTORY + clean_filename(first_part + " " + last_part) + file_ext
            )
            print(new_path)

            os.rename(DIRECTORY + file, new_path)
        except:
            continue


def clean_filename(filename):
    # Reference: https://en.wikipedia.org/wiki/Filename#Reserved_characters_and_words
    clean = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", filename).strip()

    return clean


if __name__ == "__main__":
    main()
