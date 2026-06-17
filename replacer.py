import os

from utils.replacement_helper import normalize_honorifics

def honorifics(text_en, text_jp):
    text_en = honorifics_yuika(text_en, text_jp)
    text_en = honorifics_yamashiro(text_en, text_jp)
    text_en = honorifics_special(text_en, text_jp)
    en_names = ["Aozaki", "Aoko", "Kuonji", "Alice", "Shizuki", "Soujuurou", "Touko", "Touko", "Tsukiji",
                      "Tobimaru", "Kinomi", "Housuke", "Kumari", "Kojika", "Lugh", "Beowulf", "Beo", "Fumizuka", "Eiri",
                      "Suse", "Ritsuka", "Yuika", "Sister", "Kazuki", "Tokitsu", "Yurihiko",
                      "May", "Riddell", "Archelot", "Yoshida", "Yoshida", "Kouga", "Kouga", "Uotatsu", "Uotatsu",
                      "Hanazawa", "Eiri", "Zaki", "Alice", "Yui", "Toko", "Ako", "Aozaki", "Soujuurou",
                      "Arisato", "Yamashiro", "Satonaka", "Satonaka", "Mino", "Mino", "Kitsy", "Aoyama"]
    en_prefixes = ["Mr. ", "Ms. ", "Mister ", "Miss ", "Lady ", ""]
    en_honorifics = ["-san", "-san", "-sama", "-sama", "-chan", "-kun", "-kun", "-sensei", "-senpai", "-shi", "-kun", "-sensei", "-sensei"]
    jp_names = ["蒼崎", "青子", "久遠寺", "有珠", "静希", "草十郎", "橙子", "トーコ", "槻司",
                      "鳶丸", "木乃美", "芳助", "久万梨", "金鹿", "ルゥ", "ベオウルフ", "ベオ", "文柄", "詠梨",
                      "周瀬", "律架", "唯架", "シスター", "和樹", "土桔", "由里彦",
                      "メイ", "リデル", "アーシェロット", "吉田", "<吉田|よしだ>", "恒河", "<恒河|こうが>", "<魚達|うおたつ>", "魚達",
                      "花澤", "エイリ", "ザキ", "アリス", "ユイ", "トコ", "アコ", "<蒼崎|あおざき>", "うじゅうろう>",
                      "有里", "城|やましろ>", "中|さとなか>", "里中", "美濃", "<美|み><濃|の>", "キッツィー", "青山"]
    jp_honorifics = ["さん", "サン", "様", "さま", "ちゃん", "くん", "君", "先生", "先輩", "氏", "クン", "センセ", "せんせい"]
    replacements = []
    for en_name, jp_name in zip(en_names, jp_names):
        en_prefix_variants = [
            prefix + en_name for prefix in en_prefixes
        ]
        en_honorific_variants = [
            en_name + honorific for honorific in en_honorifics
        ]
        jp_honorific_variants = [
            jp_name + honorific for honorific in jp_honorifics
        ]

        replacements.append((
            en_prefix_variants,
            en_honorific_variants,
            jp_honorific_variants
        ))

    for index, (line_en, line_jp) in enumerate(zip(text_en, text_jp)):
        for en_prefix_variants, en_honorific_variants, jp_honorific_variants in replacements:
            for jp_honorific, en_honorific in zip(jp_honorific_variants, en_honorific_variants):
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

    # Edge Cases
    # Aozaki introduction => <蒼崎|あおざき><青子|あおこ>くん
    text_en[380] = text_en[380].replace("Aoko", "Aoko-kun")
    # Drop the honorific, an honorific mentioned without a name...
    text_en[463] = text_en[463].replace("Miss", "-san")
    # But should I use an honorific with you?
    text_en[466] = text_en[466].replace("What do you mean, what do I mean?", "How I'm gonna call you. Is it fine if I use '-kun'?")
    # Yamashirooo -> Mr. Yamashirooo
    text_en[1756] = text_en[1756].replace("Mr. Yamashirooo!", "Yamashirooo!")
    # Yuika introduction
    text_en[1799] = text_en[1799].replace("Yuika", "Yuika-san")
    # Hanazawa-sa-
    text_en[1985] = text_en[1985].replace("Ms. Hanazawa", "Hanazawa-san")
    # Hanazawa-san takes her leave
    #text_en[1987] = text_en[1987].replace("Catch you later", "Hanazawa-san takes her leave")
    # Tsukiji introduction
    text_en[2238] = text_en[2238].replace("Tsukiji", "Tsukiji-kun")
    # Caps Lock
    text_en[2683] = text_en[2683].replace("AOKO AOZAKI", "AOZAKI AOKO")
    # Kitsy-chan and Kitsy Land in the same line. Basing on the mess I create since this will run after
    text_en[3973] = text_en[3973].replace("mascot Kitsy-chan, retired, and Kitsy-chan Land's", "mascot Kitsy-chan, retired, and Kitsy Land's")
    # Mr. Yamashiro -> sensei
    text_en[8590] = text_en[8590].replace("Mr. Yamashiro", "sensei")
    # sir -> sensei
    text_en[8591] = text_en[8591].replace("sir", "sensei")
    # sir -> sensei || restore the missing "Yamashiro"
    #text_en[8620] = text_en[8620].replace("sensei", "Yamashiro-sensei")
    # Yamase -> Yamase-san
    text_en[11421] = text_en[11421].replace("Yamase", "Yamase-san")
    # Fix these two broken lines
    text_en[11484] = text_en[11484].replace("Kinomi-kun", "Kinomi")
    text_en[11485] = text_en[11485].replace("Kinomi", "Kinomi-kun")
    # Mino -> Senpai
    text_en[11554] = text_en[11554].replace("Mino", "senpai")
    # Yuika-san
    text_en[12642] = text_en[12642].replace("Yuika", "Yuika-san")
    # Sister -> The Sister
    text_en[12649] = text_en[12649].replace("Sister", "The Sister")
    # Sister -> Sister Yuika ### Because of the way they rewrote this line in English
    text_en[12659] = text_en[12659].replace("Sister", "The Sister")
    # Sister -> Sister Yuika ### Because of the way they rewrote this line in English
    text_en[12681] = text_en[12681].replace("Sister", "the Sister")
    # Sister -> Sister Yuika ### Because of the way they rewrote this line in English
    text_en[12696] = text_en[12696].replace("Sister", "the Sister")
    # Sister -> Sister Yuika ### Because of the way they rewrote this line in English
    text_en[12698] = text_en[12698].replace("Sister", "the Sister")
    # Sister -> Sister Yuika ### Because of the way they rewrote this line in English
    text_en[12700] = text_en[12700].replace("Sister", "The Sister")
    # Sister -> Sister Yuika ### Because of the way they wrote this line in English
    text_en[16616] = text_en[16616].replace("Sister", "The Sister")
    # Sister -> Sister Yuika ### Because of the way they wrote this line in English
    text_en[16650] = text_en[16650].replace("Sister", "the Sister")
    # someone like Aoko -> Aoko (helps with the line break while being technically more accurate)
    text_en[19767] = text_en[19767].replace("someone like Aoko", "Aoko")
    # Miss Alice -> Alice-san - Special case where the name in JP and in EN are in different lines
    text_en[19800] = text_en[19800].replace("Miss Alice", "Alice-san")
    # Soujuurou -> Soujuurou-kun - Special case where the name in JP and in EN are in different lines
    text_en[13657] = text_en[13657].replace("Soujuurou", "Soujuurou-kun")
    # Shizuki... -> Shizuki...kun...
    text_en[15341] = text_en[15341].replace("Shizuki...", "Shizuki...kun...")
    # Ritsuka -> Ritsuka-san
    text_en[15621] = text_en[15621].replace("Ritsuka", "Ritsuka-san")
    # Shizuki -> Shizuki-kun
    text_en[23506] = text_en[23506].replace("Shizuki", "Shizuki-kun")
    # Kumari -> Kumari-kun
    text_en[23214] = text_en[23214].replace("Kumari", "Kumari-kun")
    # Mr. Yamashiro -> Yamashiro
    text_en[23241] = text_en[23241].replace("Mr. ", "")
    # Kinomi -> Kinomi-kun
    text_en[23247] = text_en[23247].replace("Kinomi", "Kinomi-kun")
    # Yui -> Yui-chan
    text_en[23881] = text_en[23881].replace("Yui", "Yui-chan")
    # Ritsuka -> Ritsuka-san
    text_en[23889] = text_en[23889].replace("Ritsuka", "Ritsuka-san")
    # May -> Riddell-san
    text_en[21952] = text_en[21952].replace("May", "Riddell-san")
    # Mr. Tokitsu -> Tokitsu-san
    text_en[21957] = text_en[21957].replace("Mr. Tokitsu", "Tokitsu-san")
    # Mr. Tokitsu -> Tokitsu
    text_en[22028] = text_en[22028].replace("Mr. Tokitsu", "Tokitsu")
    # Miss Kuonji -> Kuonji-san
    text_en[22306] = text_en[22306].replace("Kuonji", "Kuonji-san")
    # Mr. Yamashiro -> Yamashiro-sensei
    text_en[21567] = text_en[21567].replace("Mr. Yamashiro", "Yamashiro-sensei")
    # Sister -> Yuika
    text_en[21573] = text_en[21573].replace("Sister", "Yuika")
    # Sister-san Yuika-san -> Yuika-san ### Sister wasn't in the original text
    text_en[21575] = text_en[21575].replace("Sister-san ", "")
    # Mr. Yamashiro -> Yamashiro
    text_en[21581] = text_en[21581].replace("Mr. ", "")
    # Mr. Yamashiro -> Yamashiro
    text_en[21583] = text_en[21583].replace("Mr. ", "")
    # Mr. Yamashiro -> Yamashiro
    text_en[21658] = text_en[21658].replace("Mr. ", "")
    # Mr. Yamashiro -> Sensei
    text_en[22844] = text_en[22844].replace("Mr. Yamashiro", "Sensei")
    # Miss Kuonji -> Kuonji-san
    text_en[23369] = text_en[23369].replace("Miss Kuonji", "Kuonji-san")
    # Yuika -> Sister Yuika
    text_en[23896] = text_en[23896].replace("Yuika", "Sister Yuika")
    # Yuika -> Sister Yuika
    text_en[20971] = text_en[20971].replace("Yuika", "Sister Yuika")
    # Yuika Yuika -> Suse Yuika
    text_en[21083] = text_en[21083].replace("Yuika Yuika", "Suse Yuika")
    # Sister -> Sister Yuika ### Because of the way they wrote this line in English
    text_en[21090] = text_en[21090].replace("Sister", "The Sister")
    # Sister -> The Sister ### Because of the way they wrote this line in English
    text_en[21093] = text_en[21093].replace("Sister", "The Sister")
    # Sister -> The Sister ### Because of the way they wrote this line in English
    text_en[21099] = text_en[21099].replace("Sister", "the Sister")
    # Sister -> The Sister ### Because of the way they wrote this line in English
    text_en[21101] = text_en[21101].replace("Sister", "the Sister")
    # Sister -> The Sister ### Because of the way they wrote this line in English
    text_en[21113] = text_en[21113].replace("Sister", "The Sister")
    # Sister -> The Sister ### Because of the way they wrote this line in English
    text_en[21136] = text_en[21136].replace("Sister", "the Sister")
    # Sister -> The Sister ### Because of the way they wrote this line in English
    text_en[21154] = text_en[21154].replace("Sister", "the Sister")
    # Sister -> The Sister ### Because of the way they wrote this line in English
    text_en[24051] = text_en[24051].replace("Sister", "The Sister")
    # Yuika -> Suse Yuika
    text_en[24088] = text_en[24088].replace("Yuika", "Suse Yuika")
    # Yuika -> Suse Yuika
    text_en[24113] = text_en[24113].replace("Yuika", "Suse Yuika")
    # Yamashiro -> Mr. Yamashiro (thanks to the new Yamashiro function)
    text_en[166] = text_en[166].replace("Yamashiro", "Mr. Yamashiro")
    # Mr. Yamashiro -> Sensei
    text_en[22845] = text_en[22845].replace("Mr. Yamashiro", "Sensei")
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
