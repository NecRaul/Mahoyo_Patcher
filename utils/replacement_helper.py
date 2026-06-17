import json

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
