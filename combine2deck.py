import json
import os

# ==================================================================================================

filepath = os.path.dirname(os.path.realpath(__file__)) + "/"
notes_file = filepath + "sourcedata/notes.json"
strokes_file = filepath + "sourcedata/strokes.json"
audios_file = filepath + "sourcedata/audios.json"
deck_template = filepath + "deck.template.json"
outfile = filepath + "Anki-HanyuShuipingKaoshi.json"

# ==================================================================================================


def main():

    with open(notes_file, "r", encoding="utf-8") as file:
        notes = json.load(file)

    with open(strokes_file, "r", encoding="utf-8") as file:
        strokes = json.load(file)

    with open(audios_file, "r", encoding="utf-8") as file:
        audios = json.load(file)

    with open(deck_template, "r", encoding="utf-8") as file:
        deck = json.load(file)

    media = list(strokes)
    media.extend(audios)
    deck["media_files"] = media
    deck["notes"] = notes

    with open(outfile, "w+", encoding="utf-8") as file:
        json.dump(deck, file, ensure_ascii=False, indent=2, sort_keys=True)


# ==================================================================================================

if __name__ == "__main__":
    main()
    print("FINISHED")
