import os

from utils.replacement_helper import normalize_honorifics, load_replacements

def honorifics(text_en, text_jp):
    text_en = honorifics_yuika(text_en, text_jp)
    text_en = honorifics_yamashiro(text_en, text_jp)
    jp_to_en_name_replacements = load_replacements("json/jp_to_en_names.json")
    jp_to_en_honorific_replacements = load_replacements("json/jp_to_en_honorifics.json")
    jp_to_en_names = [(item.original, item.replacement) for item in jp_to_en_name_replacements]
    jp_to_en_honorifics = [(item.original, item.replacement) for item in jp_to_en_honorific_replacements]
    en_prefixes = ["Mr. ", "Ms. ", "Mister ", "Miss ", "Lady ", ""]
    replacements = []
    for jp_name, en_name in jp_to_en_names:
        for jp_honorific, en_honorific in jp_to_en_honorifics:
            replacements.append(
                (
                    jp_name + jp_honorific,
                    en_name + en_honorific,
                    [prefix + en_name for prefix in en_prefixes],
                )
            )
    for index, (line_en, line_jp) in enumerate(zip(text_en, text_jp)):
        for jp_honorific, en_honorific, en_prefix_variants in replacements:
            if jp_honorific not in line_jp:
                continue
            for en_prefix in en_prefix_variants:
                if en_prefix in line_en and en_honorific not in line_en:
                    line_en = line_en.replace(
                        en_prefix,
                        en_honorific
                    )
                    break
        text_en[index] = line_en
    text_en = honorifics_special(text_en, text_jp)
    return text_en

def honorifics_yuika(text_en, text_jp):
    jp_to_en= [
        ("シスター唯架", "Sister Yuika"),
        ("周瀬唯架", "Suse Yuika"),
        ("<周|す><瀬|せ><唯架|ゆいか>", "Suse Yuika"),
        ("<唯架|ゆいか>", "Yuika"),
        ("唯架さん", "Yuika-san"),
        ("周瀬さん", "Suse-san"),
        ("唯ちゃん", "Yui-chan"),
        ("唯架", "Yuika"),
        ("周瀬", "Suse"),
        ("ユイカ", "Yuika"),
        ("シスター", "Sister")
    ]
    en_aliases = [
        "Sister-san Yuika-san",
        "Yuika Yuika",
        "Suse Yuika",
        "Sister Yuika-san",
        "Sister-san Yuika",
        "Sister Yuika",
        "Sister-san",
        "Miss Yuika",
        "Ms. Yuika",
        "Ms. Suse",
        "Yuika-san",
        "Suse-san",
        "Yui-chan",
        "Sister",
        "Yuika",
        "Suse",
        "Yui"
    ]
    text_en = normalize_honorifics(text_en, text_jp, jp_to_en, en_aliases)
    return text_en

def honorifics_yamashiro(text_en, text_jp):
    jp_to_en= [
        ("山城教諭", "Mr. Yamashiro"),
        ("山城先生", "Yamashiro-sensei"),
        ("山城", "Yamashiro")
    ]
    en_aliases = ["Mr. Yamashiro"]
    text_en = normalize_honorifics(text_en, text_jp, jp_to_en, en_aliases)
    return text_en

def honorifics_special(text_en, text_jp):
    special_cases = [
        ("アッちゃん", "Allie", "Acchan"),
        ("アコちゃん", "Aoko", "Ako-chan"),
        ("ペン太くん", "Flippy", "Penta-kun"),
        ("先生", "sir", "sensei"),
        ("先生", "Sir", "Sensei"),
        ("トコちゃん", "Touko", "Toko-chan"),
        ("唯ちゃん", "Yuika", "Yui-chan"),
        ("唯ちゃん", "Yui", "Yui-chan"),
        ("土桔由里彦氏", "Mr. Tokitsu", "Tokitsu Yurihiko-shi"),
        ("土桔由里彦", "Mr. Tokitsu", "Tokitsu Yurihiko"),
    ]
    special_cases.sort(key=lambda case: len(case[0]), reverse=True)
    for jp_name, en_name, en_name_honorific in special_cases:
        for index, line_jp in enumerate(text_jp):
            if jp_name not in line_jp:
                continue
            if en_name in text_en[index] and en_name_honorific not in text_en[index]:
                text_en[index] = text_en[index].replace(en_name, en_name_honorific)
    return text_en


class Replacer:
    def __init__(self, game_dir, input_path, output_path):
        self.in_path = os.path.join(game_dir, input_path)
        self.out_path = os.path.join(game_dir, output_path)

    def get_script(self):
        with open(self.in_path, "r", encoding="utf-8") as script:
            return script.readlines()

    def set_script(self, text):
        with open(self.out_path, "w", encoding="utf-8") as fout:
            fout.writelines(text)
