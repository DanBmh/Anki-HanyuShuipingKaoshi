import json
import os

import tqdm

import audio_tools

# ==================================================================================================

filepath = os.path.dirname(os.path.realpath(__file__)) + "/"
notes_file = filepath + "sourcedata/notes.json"
audios_file = filepath + "sourcedata/audios.json"
override_existing_audio_files = False

# In rare cases audio is not correct, mostly because there are different pronunciations of the same
# word. Conversion to mp3 has to be done manually then. You can use this websites:
# https://ttsmp3.com/text-to-speech/Chinese%20Mandarin/
# https://www.eguidedog.net/ekho.php
extra_audio = [
    "93e537413b72bc12b1200ff18cec7a3ff81b8bc025d8ffadb6c1802e94dfc242",
    "3f2fec438176b35b808724c06f9cb2548147fdfca206602a68319f126d14c528",
]

# ==================================================================================================


def get_audio_file(note):
    """Download the audiofile and return audio text and path"""

    hanzi = note["fields"][0]
    guid = note["guid"]
    audio_name = guid + ".mp3"
    audio_path = filepath + "media/" + audio_name

    if not guid in extra_audio:
        if not os.path.exists(audio_path) or override_existing_audio_files:
            # Skip only the audio download if the file is already existing but not the rest,
            # the audio_name is used later to add the files to the decks media field
            audio_tools.download(hanzi, audio_path)

    text = "[sound:{}]".format(audio_name)
    return text, audio_name


# ==================================================================================================


def main():

    audio_tools.init_client()
    added_audios = []

    with open(notes_file, "r", encoding="utf-8") as file:
        notes = json.load(file)

    for note in tqdm.tqdm(notes):
        text, audio_name = get_audio_file(note)
        added_audios.append(audio_name)
        note["fields"][4] = text

    with open(notes_file, "w+", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2, sort_keys=True)

    added_audios = sorted(list(set(added_audios)))
    with open(audios_file, "w+", encoding="utf-8") as file:
        json.dump(added_audios, file, indent=2, sort_keys=True)


# ==================================================================================================

if __name__ == "__main__":
    main()
    print("FINISHED")
