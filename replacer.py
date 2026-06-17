import os
import re

def metric(text):
    indices = [89, 113, 1482, 1602, 1604,
               1874, 1877, 2576, 2991, 3083,
               3101, 3156, 4012, 4059, 4419,
               4476, 4553, 4558, 4655,
               4695, 4837, 4849, 4852, 4858,
               4877, 4940, 4941, 5156, 5214,
               5565, 5613, 5688, 5866,
               5879, 5890, 5892, 5909,
               5957, 5962, 5965, 6012, 6300,
               6364, 6376, 6400, 6407,
               6449, 6478, 6491, 6826, 6838,
               6918, 6921, 7105,
               7227, 7238, 7243, 7308, 5826, 8772,
               10175, 10176, 10192, 10647,
               11009, 11047, 11727, 14791, 14988,
               15286, 15288, 15381, 15895,
               16798, 16827, 16916, 16923, 16974,
               17218, 17487,
               17515, 17549, 17880, 18038, 18070,
               18308,
               18328, 18329, 18340, 18383, 20479,
               20786, 20930, 21087, 22576, 22577, 23065,
               14811, 4486, 1485,
               11505,
               3955, 6007, 11727, 13055]
    imperial_strings = ["43 degrees Fahrenheit", "thirty-foot", "over three feet", "45 miles", "miles",
                        "yards", "15 feet", "was a good few feet in length", "6 feet", "a few feet",
                        "ten feet", "a few feet", "yards", "thirty feet", "greater than a football field",
                        "fifteen feet", "few feet", "sixty feet", "thirty or so feet",
                        "a couple hundred feet", "thirty-foot", "hundred-pound", "thirty feet", "thirty feet",
                        "thirty feet", "a hundred feet", "fifty feet", "thirty feet", "thirty feet",
                        "thirty feet", "yards", "fifty feet", "one hundred feet",
                        "One hundred and fifty feet", "fifteen feet", "foot", "a hundred and fifty feet",
                        "two hundred feet", "three hundred feet", "half-mile", "650 yards", "miles",
                        "a great height―was", "six hundred feet", "two hundred feet", "two-hundred-foot",
                        "five feet", "a hundred feet", "a few feet", "sixty-foot", "yards...!",
                        "the better part of a mile", "mile", "two hundred and fifty feet",
                        "yards", "ten feet", "three feet", "paces", "three feet", "couple of feet",
                        "sixteen inches", "sixty miles", "six miles", "three hundred feet",
                        "yards", "inches", "112 miles", "twelve feet", "eighty feet",
                        "ten miles", "Four inches", "six miles", "six feet",
                        "two miles", "a hundred feet", "yards", "yards", "a hundred feet",
                        "closed the distance between them.", "thirty feet",
                        "Fifteen feet to go", "Five feet", "twenty pounds", "feet", "twenty-foot",
                        "the beast now towered above him",
                        "thirty feet", "thirty feet", "three feet", "three feet", "seventy-pound",
                        "yards", "yards", "thirty feet", "miles", "50 miles", "eight inches",
                        "twelve hundred square foot", "a foot to his left", "a foot and a half",
                        "myself, but I think my brain had a major malfunction, and my hand just went for it!",
                        "more than eighty-five square acres", "238,900 miles", "38 miles", "ounce"]
    metric_strings = ["6 degrees Celsius", "ten-meter", "around one meter", "70 kilometers", "kilometers",
                      "meters", "five meters", "stretched out several meters", "two meters", "one meter",
                      "several meters", "one meter", "meters", "ten meters", "about a hundred meters",
                      "five meters", "two meters", "twenty meters", "ten or so meters",
                      "about sixty meters", "ten-meter", "forty-five-kilo", "ten meters", "ten meters",
                      "ten meters", "thirty meters", "fifteen meters", "ten meters", "ten meters",
                      "ten meters", "meters", "twenty meters", "forty meters",
                      "Forty-eight meters", "five meters", "meter", "fifty meters",
                      "sixty meters", "a hundred meters", "one-kilometer", "600 meters", "kilometers",
                      "sixty meters above ground―was", "two hundred meters", "sixty meters", "sixty-meter",
                      "two meters", "thirty meters", "about a meter", "18-meter", "meters...!",
                      "about a kilometer", "kilometer", "eighty meters",
                      "meters", "three meters", "a meter", "meters", "a meter", "meter",
                      "forty centimeters", "a hundred kilometers", "ten kilometers", "a hundred meters",
                      "meters", "centimeters", "180 kilometers", "six meters", "eight meters",
                      "fifteen kilometers", "Ten centimeters", "ten kilometers", "two meters",
                      "three kilometers", "thirty meters", "meters", "meters", "thirty meters",
                      "closed the distance between them to just ten meters.", "ten meters",
                      "Five meters to go", "Two meters", "ten kilos", "meters", "six-meter",
                      "the boy, who was smaller than him, had grown to a size of nearly two meters",
                      "ten meters", "ten meters", "a meter", "a meter", "thirty-kilo",
                      "meters", "meters", "ten meters", "kilometers", "80 kilometers", "twenty centimeters",
                      "four hundred square meters", "twenty centimeters", "fifty centimeters",
                      "just a centimeter before that, but I misjudged. It turns out that Aozaki's physical size was slightly greater than my visual information.",
                      "350,000 square meters", "384,400 kilometers", "60 kilometers", "gram"]

    for i in range (len(indices)):
        text[indices[i]-1] = text[indices[i]-1].replace(imperial_strings[i], metric_strings[i])

    return text

def romanization(text):
    localized_name = ["Soujyuro", "Sizuki", "Fumidsuka", "Yamasiro", "Koga"]
    hepburn_name = ["Soujuurou", "Shizuki", "Fumizuka", "Yamashiro", "Kouga"]

    for i in range (len(localized_name)):
        line_count = 0
        for line in text:
            if (localized_name[i] in line) and (hepburn_name[i] not in line):
                text[line_count] = text[line_count].replace(localized_name[i], hepburn_name[i])
            line_count += 1

    # Edge Cases
    # "The 'jyu' in your name"
    text[1917] = text[1917].replace("jyu", "juu")
    # Si -> Shi
    text[15548] = text[15548].replace("Si", "Shi")
    # Sou...jyuro... -> Sou...juurou...
    text[18757] = text[18757].replace("jyuro", "juurou")
    # Touko -> Toko ### It's how Ritsuka calls Touko
    text[20888] = text[20888].replace("Touko", "Toko")


    return text

def name_order(text):
    localized_name = ["Aoko Aozaki", "Alice Kuonji", "Soujuurou Shizuki", "Touko Aozaki", "Tobimaru Tsukiji",
                      "Housuke Kinomi", "Kojika Kumari", "Eiri Fumizuka", "Ritsuka Suse", "Yuika Suse",
                      "Kazuki Yamashiro", "Yurihiko Tokitsu", "Kimikuni Tsukiji", "Hitoyoshi Tsukiji"]
    correct_name = ["Aozaki Aoko", "Kuonji Alice", "Shizuki Soujuurou", "Aozaki Touko", "Tsukiji Tobimaru",
                    "Kinomi Housuke", "Kumari Kojika", "Fumizuka Eiri", "Suse Ritsuka", "Suse Yuika",
                    "Yamashiro Kazuki", "Tokitsu Yurihiko", "Tsukiji Kimikuni", "Tsukiji Hitoyoshi"]

    for i in range (len(localized_name)):
        line_count = 0
        for line in text:
            if (localized_name[i] in line) and (correct_name[i] not in line):
                text[line_count] = text[line_count].replace(localized_name[i], correct_name[i])
            line_count += 1

    return text

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

def honorifics_special(text_en, text_jp):
    # Special Cases:
    # アッちゃん - Allie
    # アコちゃん - Aoko
    # ペン太くん - Flippy
    # 先生 - Sir

    jp_name = ["アッちゃん", "アコちゃん", "ペン太くん", "先生", "先生", "トコちゃん", "唯ちゃん", "唯ちゃん", "土桔由里彦氏", "土桔由里彦"]
    en_name_honorific = ["Acchan", "Ako-chan", "Penta-kun", "sensei", "Sensei", "Toko-chan", "Yui-chan", "Yui-chan", "Tokitsu Yurihiko-shi", "Tokitsu Yurihiko"]
    en_name = ["Allie", "Aoko", "Flippy", "sir", "Sir", "Touko", "Yuika", "Yui", "Mr. Tokitsu", "Mr. Tokitsu"]

    for i in range(0, len(en_name)):
        line_count = 0
        for line_jp in text_jp:
            if jp_name[i] in line_jp:
                if (en_name[i] in text_en[line_count]) and (en_name_honorific[i] not in text_en[line_count]):
                    text_en[line_count] = text_en[line_count].replace(en_name[i], en_name_honorific[i])
            line_count = line_count + 1

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


def honorifics_yuika(text_en, text_jp):
    # 1. Map JP text directly to the exact desired EN output.
    # Order matters: we put the longest/most specific names first
    # so "シスター唯架" is caught before just "シスター" or "唯架".
    jp_target_mapping = [
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

    # 2. List all the inconsistent ways the English text refers to her.
    # We include your bugged outputs too, so this script cleans them up if they exist!
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

    # Sort the English aliases by length (longest first) so regex checks "Sister Yuika" before "Sister"
    en_aliases_sorted = sorted(en_aliases, key=len, reverse=True)

    # Build a regex pattern to match these exactly as whole words.
    # This is case-sensitive by default, which safely ignores common nouns like "my sister".
    pattern = r'\b(?:' + '|'.join(map(re.escape, en_aliases_sorted)) + r')\b'
    alias_regex = re.compile(pattern)

    for i in range(len(text_jp)):
        line_jp = text_jp[i]

        # Figure out the true intended name from the Japanese text
        target_en = None
        for jp_term, expected_en in jp_target_mapping:
            if jp_term in line_jp:
                target_en = expected_en
                break

        if target_en:
            # Find any of the recognized English aliases in the line and swap them for the correct target
            text_en[i] = alias_regex.sub(target_en, text_en[i])

    return text_en

def honorifics_yamashiro(text_en, text_jp):
    # 1. Map JP text directly to the exact desired EN output.
    # Order matters: we put the longest/most specific names first
    # so "シスター唯架" is caught before just "シスター" or "唯架".
    jp_target_mapping = [
        ("山城教諭", "Mr. Yamashiro"),
        ("山城先生", "Yamashiro-sensei"),
        ("山城", "Yamashiro")
    ]

    # 2. List all the inconsistent ways the English text refers to her.
    # We include your bugged outputs too, so this script cleans them up if they exist!
    en_aliases = [
        "Mr. Yamashiro"
    ]

    # Sort the English aliases by length (longest first) so regex checks "Sister Yuika" before "Sister"
    en_aliases_sorted = sorted(en_aliases, key=len, reverse=True)

    # Build a regex pattern to match these exactly as whole words.
    # This is case-sensitive by default, which safely ignores common nouns like "my sister".
    pattern = r'\b(?:' + '|'.join(map(re.escape, en_aliases_sorted)) + r')\b'
    alias_regex = re.compile(pattern)

    for i in range(len(text_jp)):
        line_jp = text_jp[i]

        # Figure out the true intended name from the Japanese text
        target_en = None
        for jp_term, expected_en in jp_target_mapping:
            if jp_term in line_jp:
                target_en = expected_en
                break

        if target_en:
            # Find any of the recognized English aliases in the line and swap them for the correct target
            text_en[i] = alias_regex.sub(target_en, text_en[i])

    return text_en

def americanisms(text):

    # It's weird, in these two instances they use an americanised school grade system, but in all other instances so
    # far they stick to the Japanese one
    # There is one more instance, but I don't think I'll really add this to the patch. This function is never called, btw

    # 11th Grade => 2nd Year
    text[559] = text[559].replace("11th grade", "2nd year")
    # Freshman -> 1st Year
    text[2387] = text[2387].replace("freshman", "first-year")

    return text

def translation_mistakes(text):

    # No reason not to fix these

    # Get him out of his head
    text[964] = text[964].replace("get him out of his head", "get him out of her head")
    # Missing "to"
    text[2792] = text[2792].replace("use them", "use them to")
    # To look of pity -> the look of pity
    text[3395] = text[3395].replace("to look", "the look")
    # missing "the"
    text[3437] = text[3437].replace("unassuming", "the unassuming")
    # missing "the"
    text[3471] = text[3471].replace("keeper", "the keeper")
    # You're weren't
    text[3747] = text[3747].replace("You're", "You")
    # missing "to"
    text[3898] = text[3898].replace("seemed", "seemed to")
    # Alice -> Aoko ### How do you make an error like this? Don't they have proofreaders? And they never fixed this?!
    text[14419] = text[14419].replace("Alice", "Aoko")
    # missing "m"
    text[15170] = text[15170].replace("with y mouth", "with my mouth")
    # missing "throw"
    text[16504] = text[16504].replace("to those", "to throw those")
    # missing "what"
    text[18823] = text[18823].replace("people", "what people")
    # missing "Aozaki". Not really an error, but I would consider a mistake since the contrast was intended,
    text[19515] = text[19515].replace("so mad", "so mad, Aozaki")
    # he -> she
    text[21765] = text[21765].replace("then he'd", "then she'd")
    # missing "be"
    text[21768] = text[21768].replace("had to unlucky", "had to be unlucky")

    return text


class Replacer:
    def __init__(self, game_dir, input_path, output_path):
        self.in_path = os.path.join(game_dir, input_path)
        self.out_path = os.path.join(game_dir, output_path)

    def get_script(self):
        script = open(self.in_path, "r", encoding='utf-8')
        text = script.readlines()
        script.close()
        return text

    def set_script(self, text):
        fout = open(self.out_path, 'w', encoding='utf-8')
        fout.writelines(text)
        fout.close()
