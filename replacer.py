import os

from utils.replacement_helper import normalize_honorifics

def honorifics(text_en, text_jp):
    text_en = honorifics_yuika(text_en, text_jp)
    text_en = honorifics_yamashiro(text_en, text_jp)
    jp_to_en_name_mapping = [
        ('蒼崎', 'Aozaki'),
        ('青子', 'Aoko'),
        ('久遠寺', 'Kuonji'),
        ('有珠', 'Alice'),
        ('静希', 'Shizuki'),
        ('草十郎', 'Soujuurou'),
        ('橙子', 'Touko'),
        ('トーコ', 'Touko'),
        ('槻司', 'Tsukiji'),
        ('鳶丸', 'Tobimaru'),
        ('木乃美', 'Kinomi'),
        ('芳助', 'Housuke'),
        ('久万梨', 'Kumari'),
        ('金鹿', 'Kojika'),
        ('ルゥ', 'Lugh'),
        ('ベオウルフ', 'Beowulf'),
        ('ベオ', 'Beo'),
        ('文柄', 'Fumizuka'),
        ('詠梨', 'Eiri'),
        ('周瀬', 'Suse'),
        ('律架', 'Ritsuka'),
        ('唯架', 'Yuika'),
        ('シスター', 'Sister'),
        ('和樹', 'Kazuki'),
        ('土桔', 'Tokitsu'),
        ('由里彦', 'Yurihiko'),
        ('メイ', 'May'),
        ('リデル', 'Riddell'),
        ('アーシェロット', 'Archelot'),
        ('吉田', 'Yoshida'),
        ('<吉田|よしだ>', 'Yoshida'),
        ('恒河', 'Kouga'),
        ('<恒河|こうが>', 'Kouga'),
        ('<魚達|うおたつ>', 'Uotatsu'),
        ('魚達', 'Uotatsu'),
        ('花澤', 'Hanazawa'),
        ('エイリ', 'Eiri'),
        ('ザキ', 'Zaki'),
        ('アリス', 'Alice'),
        ('ユイ', 'Yui'),
        ('トコ', 'Toko'),
        ('アコ', 'Ako'),
        ('<蒼崎|あおざき>', 'Aozaki'),
        ('うじゅうろう>', 'Soujuurou'),
        ('有里', 'Arisato'),
        ('城|やましろ>', 'Yamashiro'),
        ('中|さとなか>', 'Satonaka'),
        ('里中', 'Satonaka'),
        ('美濃', 'Mino'),
        ('<美|み><濃|の>', 'Mino'),
        ('キッツィー', 'Kitsy'),
        ('青山', 'Aoyama'),
    ]
    jp_to_en_honorific_mapping = [
        ('さん', '-san'),
        ('サン', '-san'),
        ('様', '-sama'),
        ('さま', '-sama'),
        ('ちゃん', '-chan'),
        ('くん', '-kun'),
        ('君', '-kun'),
        ('先生', '-sensei'),
        ('先輩', '-senpai'),
        ('氏', '-shi'),
        ('クン', '-kun'),
        ('センセ', '-sensei'),
        ('せんせい', '-sensei'),
    ]
    en_prefixes = ["Mr. ", "Ms. ", "Mister ", "Miss ", "Lady ", ""]
    replacements = []
    for jp_name, en_name in jp_to_en_name_mapping:
        for jp_honorific, en_honorific in jp_to_en_honorific_mapping:
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
