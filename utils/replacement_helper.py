import json
import re

from replacement import Replacement


def load_replacements(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [
        Replacement(
            item.get("line"),
            item.get("original"),
            item.get("replacement"),
            item.get("comment", None),
        )
        for item in data
    ]


def apply_replacements(text, replacements):
    for replacement in replacements:
        original_txt = replacement.original
        replacement_txt = replacement.replacement
        line = int(replacement.line) if replacement.line != "all" else "all"
        if line == "all":
            text = [
                line_text.replace(original_txt, replacement_txt) for line_text in text
            ]
        else:
            text[line - 1] = text[line - 1].replace(original_txt, replacement_txt)
    return text


def normalize_honorifics(text_en, text_jp, jp_to_en, en_aliases):
    en_aliases_sorted = sorted(en_aliases, key=len, reverse=True)
    pattern = r"\b(?:" + "|".join(map(re.escape, en_aliases_sorted)) + r")\b"  # ty:ignore[no-matching-overload]
    alias_regex = re.compile(pattern)
    for index, line_jp in enumerate(text_jp):
        target_en = next(
            (en for jp, en in jp_to_en if jp in line_jp),
            None,
        )
        if target_en:
            text_en[index] = alias_regex.sub(target_en, text_en[index])
    return text_en
