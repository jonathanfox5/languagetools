import datetime, os, pathlib

from faster_whisper import WhisperModel


INPUT_DIRECTORY = "media\\"
OUTPUT_DIRECTORY = "output\\"
MODEL_SIZE = "medium"
LANGUAGE = "it"

# Set to "cuda" for an nvidia graphics card. Otherwise set to "cpu"
DEVICE = "cuda"

def main():
    # Additional settings
    beam_size = 1
    vad_filter = False
    word_level_timestamps = True

    # Run on all files in directory
    for file in os.listdir(INPUT_DIRECTORY):
        print(file)

        # Run on GPU with FP16
        model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type="float16")

        segments, info = model.transcribe(
            INPUT_DIRECTORY + file,
            beam_size=beam_size,
            language=LANGUAGE,
            vad_filter=vad_filter,
            word_timestamps=word_level_timestamps,
        )

        # Build SRT
        output = ""
        i = 1
        for segment in segments:
            line = "{}\n{} --> {}\n{}\n\n".format(
                i,
                srt_time_format(segment.start),
                srt_time_format(segment.end),
                segment.text.strip(),
            )

            print(line)

            output += line
            i += 1

        # Save file
        file_stem = pathlib.Path(file).stem

        save_file(OUTPUT_DIRECTORY + file_stem + ".srt", output.encode("utf-8"), True)


def srt_time_format(seconds):
    time = datetime.datetime.fromtimestamp(seconds)

    output = "{d.hour:02}:{d.minute:02}:{d.second:02},{d.microsecond:06}".format(
        d=time
    )[:-3]

    return output


def save_file(filename, data, write_binary):
    write_type = "w"
    if write_binary:
        write_type = "wb"

    with open(filename, write_type) as f:
        f.write(data)

    return True


if __name__ == "__main__":
    main()
