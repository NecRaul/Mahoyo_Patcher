import re
from typing import Pattern

from mahoyo_patcher.models import Replacement, load_replacements
from mahoyo_patcher.utils import get_resource_path


def apply_honorifics(script_en: list[str], script_jp: list[str]) -> list[str]:
    script_en = yuika_honorifics(script_en, script_jp)
    script_en = yamashiro_honorifics(script_en, script_jp)
    jp_to_en_name_replacements: list[Replacement] = load_replacements(
        get_resource_path("mahoyo_patcher.data", "jp_to_en_names.json")
    )
    jp_to_en_honorific_replacements: list[Replacement] = load_replacements(
        get_resource_path("mahoyo_patcher.data", "jp_to_en_honorifics.json")
    )
    jp_to_en_names: list[tuple[str, str]] = [
        (item.original, item.replacement) for item in jp_to_en_name_replacements
    ]
    jp_to_en_honorifics: list[tuple[str, str]] = [
        (item.original, item.replacement) for item in jp_to_en_honorific_replacements
    ]
    en_prefixes: list[str] = ["Mr. ", "Ms. ", "Mister ", "Miss ", "Lady ", ""]
    replacements: list[tuple[str, str, list[str]]] = []
    for jp_name, en_name in jp_to_en_names:
        for jp_honorific, en_honorific in jp_to_en_honorifics:
            replacements.append(
                (
                    jp_name + jp_honorific,
                    en_name + en_honorific,
                    [prefix + en_name for prefix in en_prefixes],
                )
            )
    for index, (line_en, line_jp) in enumerate(zip(script_en, script_jp)):
        for jp_honorific, en_honorific, en_prefix_variants in replacements:
            if jp_honorific not in line_jp:
                continue
            for en_prefix in en_prefix_variants:
                if en_prefix in line_en and en_honorific not in line_en:
                    line_en = line_en.replace(en_prefix, en_honorific)
                    break
        script_en[index] = line_en
    script_en = special_honorifics(script_en, script_jp)
    return script_en


def yuika_honorifics(script_en: list[str], script_jp: list[str]) -> list[str]:
    jp_to_en: list[tuple[str, str]] = [
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
        ("シスター", "Sister"),
    ]
    en_aliases: list[str] = [
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
        "Yui",
    ]
    script_en = normalize_honorifics(script_en, script_jp, jp_to_en, en_aliases)
    return script_en


def yamashiro_honorifics(script_en: list[str], script_jp: list[str]) -> list[str]:
    jp_to_en: list[tuple[str, str]] = [
        ("山城教諭", "Mr. Yamashiro"),
        ("山城先生", "Yamashiro-sensei"),
        ("山城", "Yamashiro"),
    ]
    en_aliases: list[str] = ["Mr. Yamashiro"]
    script_en = normalize_honorifics(script_en, script_jp, jp_to_en, en_aliases)
    return script_en


def special_honorifics(script_en: list[str], script_jp: list[str]) -> list[str]:
    special_cases: list[tuple[str, str, str]] = [
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
    special_cases.sort(key=sort_honorific_case, reverse=True)
    for jp_name, en_name, en_name_honorific in special_cases:
        for index, line_jp in enumerate(script_jp):
            if jp_name not in line_jp:
                continue
            if (
                en_name in script_en[index]
                and en_name_honorific not in script_en[index]
            ):
                script_en[index] = script_en[index].replace(en_name, en_name_honorific)
    return script_en


def sort_honorific_case(case: tuple[str, str, str]) -> int:
    return len(case[0])


def normalize_honorifics(
    script_en: list[str],
    script_jp: list[str],
    jp_to_en: list[tuple[str, str]],
    en_aliases: list[str],
) -> list[str]:
    en_aliases_sorted: list[str] = sorted(en_aliases, key=len, reverse=True)
    pattern: str = r"\b(?:" + "|".join(map(re.escape, en_aliases_sorted)) + r")\b"
    alias_regex: Pattern[str] = re.compile(pattern)
    for index, line_jp in enumerate(script_jp):
        target_en: str | None = next(
            (en for jp, en in jp_to_en if jp in line_jp),
            None,
        )
        if target_en:
            script_en[index] = alias_regex.sub(target_en, script_en[index])
    return script_en
