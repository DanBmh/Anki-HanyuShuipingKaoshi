import copy
import hashlib
import json
import os

# ==================================================================================================

filepath = os.path.dirname(os.path.realpath(__file__)) + "/"
vocab_file = filepath + "sourcedata/vocab_ger.json"
outfile = filepath + "sourcedata/notes.json"

note_template = {
    "__type__": "Note",
    "data": "",
    "fields": [
        "报纸",
        "<span class='tone4'>bào</span> <span class='tone3'>zhǐ</span><!--bao zhi-->",
        "Zeitung",
        "",
        "",
    ],
    "flags": 0,
    "guid": "e4ce37ce6340fa89e1d03b99375fc0e5ebb99a01501deb5c355e62fec17cbd02",
    "note_model_uuid": "09165a9e-6da5-11ec-8299-2331cedecf60",
    "tags": ["Buch_2::Kapitel_1", "Nomen"],
}

tone_template = "<span class='tone{}'>{}</span>"

tones = {
    "1": "āēīōū",
    "2": "áéíóú",
    "3": "ǎěǐǒǔ",
    "4": "àèìòù",
}

replacements = {
    "a": "āáǎà",
    "e": "ēéěè",
    "i": "īíǐì",
    "o": "ōóǒò",
    "u": "ūúǔù",
}

# ==================================================================================================


def add_note_id(note, hanzi, pinyin):
    """Create id from hashed hanzi tag"""

    text = hanzi + " " + pinyin
    note_id = hashlib.sha256(text.encode("utf-8")).hexdigest()
    note["guid"] = note_id
    return note


# ==================================================================================================


def main():
    with open(vocab_file, "r", encoding="utf-8") as file:
        vocab = json.load(file)

    notes = []
    for entry in vocab:
        note = copy.deepcopy(note_template)
        note["fields"][0] = entry["hanzi"]
        note = add_note_id(note, entry["hanzi"], entry["pinyin"])

        # Find out which tone the parts of the pinyin transcription have to colorize them
        pinyins = [p.strip() for p in entry["pinyin"].split()]
        pinyin_text = ""
        for p in pinyins:
            tone = ""
            for t in tones:
                for v in tones[t]:
                    if v in p:
                        tone = t
                        break
                if tone != "":
                    break
            pinyin_text += tone_template.format(tone, p.lower()) + " "

        # Add a comment without tones to simplify searching the finished deck file
        pinyin_comment = entry["pinyin"]
        for v in replacements:
            for t in replacements[v]:
                pinyin_comment = pinyin_comment.replace(t, v)
        pinyin_comment = "<!--{}-->".format(pinyin_comment)

        pinyin_text = pinyin_text.strip() + pinyin_comment
        note["fields"][1] = pinyin_text

        tags = []
        tags.append("hsk{}".format(entry["level"]))
        tags.extend(entry["text"].keys())
        note["tags"] = tags

        text = ""
        for k, v in entry["text"].items():
            if k == "Zählwort":
                text += "Zählwort " + v
            else:
                text += v
            text += ", <br>"
        if text.endswith(", <br>"):
            text = text[:-6]
        note["fields"][2] = text

        notes.append(note)

    with open(outfile, "w+", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2, sort_keys=True)


# ==================================================================================================

if __name__ == "__main__":
    main()
    print("FINISHED")
