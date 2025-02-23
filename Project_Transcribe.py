import whisper
import os
import json
from pathlib import Path
import textwrap

Supported_ex = ["mp3", "mp4", "mkv"]  # supported extensions


def find_media(path):               # It Scans the folder and return the tuple of lists of media, and its roots it founds
    media = []
    roots = []
    for r, _, files in os.walk(path):
        for file in files:
            ext = file.split(".")[-1]
            if ext in Supported_ex:
                media.append(file)
                roots.append(r)
    return media, roots


def transcribe_audio(audio):        # It first loads the tiny model of whisper and then transcribe the audio into text
    model = whisper.load_model("tiny")
    text_of_audio = model.transcribe(audio)
    # remove the extra space in the text that the model return
    text_of_audio = text_of_audio["text"].strip()
    text_of_audio = textwrap.wrap(text_of_audio, width=80)
    return text_of_audio


if __name__ == "__main__":
    path_to_search = 'C:/Users/hp/PycharmProjects/practice/Songs'
    media_files, path_of_files = find_media(path_to_search)
    if not media_files:
        print("No media files found")
    for afile, path_of_file in zip(media_files, path_of_files):
        full_path = path_of_file + "/" + afile
        ext = afile.split(".")[-1]
        file_name = afile.removesuffix(ext)
        output_dir = Path("C:/Users/hp/PycharmProjects/practice/Transcribed_audio")
        output_file = output_dir / (file_name + "json")
        with open(output_file, "w") as file:
            # helps in creating json file and adding the keys and its values
            json.dump({'File name': file_name + ext, 'text' : transcribe_audio(full_path)}, file, indent=4)
            print(f'Successfully transcribed {afile}')
