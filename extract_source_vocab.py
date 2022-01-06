import json
import os

from bs4 import BeautifulSoup

# ==================================================================================================

filepath = os.path.dirname(os.path.realpath(__file__)) + "/"
datafile = filepath + "sourcedata/hsk_{}_{}.txt"
levels = [1, 2, 3, 4, 5, 6]
language = "ger"
outfile = filepath + "sourcedata/vocab_{}.json".format(language)


# ==================================================================================================


def main():
    vocabulary = []
    for level in levels:

        sfile = datafile.format(level, language)
        with open(sfile, "r", encoding="utf-8-sig", errors="ignore") as file:
            content = file.read()
            soup = BeautifulSoup(content, "lxml")

        cbox = soup.find("div", attrs={"class": "content_txt"})

        vboxes = cbox.findAll("tr")
        for vbox in vboxes:
            items = vbox.findAll("td")

            entry = {
                "level": level,
                "hanzi": items[0].text.strip(),
                "pinyin": items[1].text.strip(),
            }

            # Some words can have multiple meanings depending on their type
            trans = {}
            for child in items[2].children:
                if child.name == "span":
                    key = child.text.strip()
                    key = key.replace(":", "")
                elif child.name == "br":
                    continue
                else:
                    trans[key] = child.text.strip()
            entry["text"] = trans

            vocabulary.append(entry)

    with open(outfile, "w+", encoding="utf-8") as file:
        json.dump(vocabulary, file, ensure_ascii=False, indent=2, sort_keys=True)


# ==================================================================================================

if __name__ == "__main__":
    main()
    print("FINISHED")
