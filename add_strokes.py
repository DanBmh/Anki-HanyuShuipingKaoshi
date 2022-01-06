import json
import os
import shutil

import pandas as pd
import requests

# ==================================================================================================

filepath = os.path.dirname(os.path.realpath(__file__)) + "/"
notes_file = filepath + "sourcedata/notes.json"
strokes_file = filepath + "sourcedata/strokes.json"

mch_path = filepath + "../Most Common 3000 Chinese - ANKI with Traditional.csv"
mch_data = None
src_path_1 = filepath + "../Domino_Chinese_Level_1-20_Complete_Vocabulary/media/"
src_path_2 = filepath + "../Chinese__Most_Common_3000_Hanzi/media/"
src_path_3 = filepath + "../Anki-ChinaEntdecken/media/"

# Search them at: https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb=勺拔梨
extra_gifs = {
    "勺": ["21242.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21242.gif"],
    "拔": ["25300.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25300.gif"],
    "梨": ["26792.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26792.gif"],
    "橙": ["27225.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/27225.gif"],
    "醋": ["37259.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/37259.gif"],
    "乒": ["20050.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/20050.gif"],
    "乓": ["20051.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/20051.gif"],
    "侈": ["20360.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/20360.gif"],
    "俐": ["20432.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/20432.gif"],
    "兢": ["20834.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/20834.gif"],
    "剔": ["21076.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21076.gif"],
    "叼": ["21500.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21500.gif"],
    "吝": ["21533.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21533.gif"],
    "咀": ["21632.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21632.gif"],
    "咙": ["21657.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21657.gif"],
    "哆": ["21702.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21702.gif"],
    "唆": ["21766.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21766.gif"],
    "唠": ["21792.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21792.gif"],
    "唾": ["21822.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21822.gif"],
    "啃": ["21827.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21827.gif"],
    "啬": ["21868.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21868.gif"],
    "啰": ["21872.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21872.gif"],
    "嗦": ["21990.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21990.gif"],
    "嗨": ["21992.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/21992.gif"],
    "嘈": ["22024.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/22024.gif"],
    "嚏": ["22159.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/22159.gif"],
    "婪": ["23146.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/23146.gif"],
    "宵": ["23477.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/23477.gif"],
    "屉": ["23625.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/23625.gif"],
    "岔": ["23700.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/23700.gif"],
    "崭": ["23853.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/23853.gif"],
    "徊": ["24458.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/24458.gif"],
    "徘": ["24472.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/24472.gif"],
    "徙": ["24473.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/24473.gif"],
    "怠": ["24608.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/24608.gif"],
    "惋": ["24779.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/24779.gif"],
    "惦": ["24806.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/24806.gif"],
    "惫": ["24811.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/24811.gif"],
    "惮": ["24814.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/24814.gif"],
    "惰": ["24816.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/24816.gif"],
    "憋": ["24971.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/24971.gif"],
    "扒": ["25170.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25170.gif"],
    "抒": ["25234.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25234.gif"],
    "拄": ["25284.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25284.gif"],
    "拌": ["25292.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25292.gif"],
    "拧": ["25319.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25319.gif"],
    "拽": ["25341.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25341.gif"],
    "挎": ["25358.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25358.gif"],
    "挚": ["25370.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25370.gif"],
    "捍": ["25421.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25421.gif"],
    "捎": ["25422.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25422.gif"],
    "掐": ["25488.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25488.gif"],
    "掰": ["25520.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25520.gif"],
    "揍": ["25549.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25549.gif"],
    "搀": ["25600.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25600.gif"],
    "搓": ["25619.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25619.gif"],
    "擎": ["25806.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25806.gif"],
    "攒": ["25874.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/25874.gif"],
    "斟": ["26015.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26015.gif"],
    "晾": ["26238.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26238.gif"],
    "暄": ["26244.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26244.gif"],
    "暧": ["26279.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26279.gif"],
    "曝": ["26333.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26333.gif"],
    "杠": ["26464.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26464.gif"],
    "柬": ["26604.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26604.gif"],
    "柿": ["26623.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26623.gif"],
    "桔": ["26708.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26708.gif"],
    "椒": ["26898.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26898.gif"],
    "椭": ["26925.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/26925.gif"],
    "榨": ["27048.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/27048.gif"],
    "殃": ["27523.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/27523.gif"],
    "殴": ["27572.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/27572.gif"],
    "氓": ["27667.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/27667.gif"],
    "沐": ["27792.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/27792.gif"],
    "沛": ["27803.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/27803.gif"],
    "沧": ["27815.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/27815.gif"],
    "洽": ["27965.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/27965.gif"],
    "涕": ["28053.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28053.gif"],
    "涮": ["28078.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28078.gif"],
    "淀": ["28096.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28096.gif"],
    "淆": ["28102.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28102.gif"],
    "渣": ["28195.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28195.gif"],
    "溉": ["28297.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28297.gif"],
    "滤": ["28388.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28388.gif"],
    "澈": ["28552.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28552.gif"],
    "濒": ["28626.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28626.gif"],
    "瀑": ["28689.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28689.gif"],
    "烘": ["28888.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28888.gif"],
    "烹": ["28921.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/28921.gif"],
    "熨": ["29096.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/29096.gif"],
    "狈": ["29384.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/29384.gif"],
    "猖": ["29462.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/29462.gif"],
    "猾": ["29502.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/29502.gif"],
    "甭": ["29997.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/29997.gif"],
    "疙": ["30105.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30105.gif"],
    "疤": ["30116.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30116.gif"],
    "痪": ["30186.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30186.gif"],
    "痹": ["30201.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30201.gif"],
    "瘩": ["30249.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30249.gif"],
    "瘸": ["30264.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30264.gif"],
    "瘾": ["30270.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30270.gif"],
    "皂": ["30338.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30338.gif"],
    "眶": ["30518.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30518.gif"],
    "睦": ["30566.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30566.gif"],
    "睬": ["30572.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30572.gif"],
    "瞩": ["30633.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30633.gif"],
    "磋": ["30923.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/30923.gif"],
    "秤": ["31204.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/31204.gif"],
    "稠": ["31264.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/31264.gif"],
    "筐": ["31568.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/31568.gif"],
    "筛": ["31579.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/31579.gif"],
    "筷": ["31607.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/31607.gif"],
    "簸": ["31800.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/31800.gif"],
    "粥": ["31909.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/31909.gif"],
    "紊": ["32010.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/32010.gif"],
    "绎": ["32462.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/32462.gif"],
    "缀": ["32512.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/32512.gif"],
    "肪": ["32938.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/32938.gif"],
    "肴": ["32948.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/32948.gif"],
    "腮": ["33134.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/33134.gif"],
    "舔": ["33300.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/33300.gif"],
    "荧": ["33639.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/33639.gif"],
    "葫": ["33899.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/33899.gif"],
    "蔼": ["34108.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/34108.gif"],
    "蕉": ["34121.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/34121.gif"],
    "衅": ["34885.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/34885.gif"],
    "袜": ["34972.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/34972.gif"],
    "袱": ["34993.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/34993.gif"],
    "诬": ["35820.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/35820.gif"],
    "诽": ["35837.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/35837.gif"],
    "谤": ["35876.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/35876.gif"],
    "赁": ["36161.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/36161.gif"],
    "赂": ["36162.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/36162.gif"],
    "踊": ["36362.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/36362.gif"],
    "踌": ["36364.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/36364.gif"],
    "蹋": ["36427.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/36427.gif"],
    "蹬": ["36460.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/36460.gif"],
    "躇": ["36487.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/36487.gif"],
    "辙": ["36761.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/36761.gif"],
    "辫": ["36779.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/36779.gif"],
    "迸": ["36856.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/36856.gif"],
    "酗": ["37207.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/37207.gif"],
    "酝": ["37213.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/37213.gif"],
    "酱": ["37233.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/37233.gif"],
    "锈": ["38152.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/38152.gif"],
    "锲": ["38194.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/38194.gif"],
    "阂": ["38402.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/38402.gif"],
    "隘": ["38552.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/38552.gif"],
    "隧": ["38567.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/38567.gif"],
    "雹": ["38649.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/38649.gif"],
    "鞠": ["38816.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/38816.gif"],
    "韧": ["38887.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/38887.gif"],
    "飙": ["39129.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/39129.gif"],
    "饪": ["39274.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/39274.gif"],
    "饺": ["39290.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/39290.gif"],
    "馅": ["39301.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/39301.gif"],
    "馋": ["39307.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/39307.gif"],
    "馒": ["39314.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/39314.gif"],
    "髦": ["39654.gif", "https://www.mdbg.net/chinese/rsc/img/stroke_anim/39654.gif"],
}
webgifs = {v[0]: v[1] for v in extra_gifs.values()}

# ==================================================================================================


def get_gifs(note):
    """Generate the gif text and collect the gif paths"""

    simp = note["fields"][0]
    text = ""
    gifs = []
    missing = []

    for s in simp:
        if s in " .":
            # Skip some of the keys
            continue

        t = None
        if s in extra_gifs:
            # Handle gifs added by hand
            t = "<img src='{}' />".format(extra_gifs[s][0])
        else:
            try:
                # Search for the matching gif
                t = mch_data[mch_data.iloc[:, 0] == s].iloc[0, 2]
            except IndexError:
                missing.append(s)

        if not t is None:
            t = t.replace(" />", "/>")
            t = t.replace("img src", "img class='animated-gif' src")
            text = text + t

            g = t.partition("src='")[2].partition(".gif")[0] + ".gif"
            gifs.append(g)

    return text, gifs, missing


# ==================================================================================================


def main():
    global mch_data

    with open(notes_file, "r", encoding="utf-8") as file:
        notes = json.load(file)

    mch_data = pd.read_csv(mch_path, header=None, keep_default_na=False)
    added_gifs = []
    missing_gifs = []

    for note in notes:
        text, gifs, missing = get_gifs(note)
        added_gifs.extend(gifs)
        missing_gifs.extend(missing)
        if text != "":
            note["fields"][3] = text

    missing_gifs = sorted(set(missing_gifs))
    print("Missing gifs:", len(missing_gifs), "".join(missing_gifs))

    dest_path = filepath + "media/"
    for g in added_gifs:
        if not os.path.isfile(dest_path + g):
            if os.path.isfile(src_path_1 + g):
                shutil.copy(src_path_1 + g, dest_path)
            elif os.path.isfile(src_path_2 + g):
                shutil.copy(src_path_2 + g, dest_path)
            elif os.path.isfile(src_path_3 + g):
                shutil.copy(src_path_3 + g, dest_path)
            elif g in webgifs:
                r = requests.get(webgifs[g], allow_redirects=True)
                open(dest_path + g, "wb+").write(r.content)
            else:
                print("No file to copy gif:", g)

    with open(notes_file, "w+", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2, sort_keys=True)

    added_gifs = sorted(list(set(added_gifs)))
    with open(strokes_file, "w+", encoding="utf-8") as file:
        json.dump(added_gifs, file, indent=2, sort_keys=True)


# ==================================================================================================

if __name__ == "__main__":
    main()
    print("FINISHED")
