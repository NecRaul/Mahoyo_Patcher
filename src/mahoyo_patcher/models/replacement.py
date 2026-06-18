import json
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, cast


class ReplacementJSON(TypedDict, total=False):
    line: int | str
    original: str
    replacement: str
    comment: str


@dataclass
class Replacement:
    line: int | str
    original: str
    replacement: str
    comment: str = ""

    @classmethod
    def from_dict(cls, data: ReplacementJSON) -> "Replacement":
        return cls(**data)


def load_replacements(input_path: Path) -> list[Replacement]:
    with open(input_path, mode="r", encoding="utf-8") as f:
        data_list: list[ReplacementJSON] = cast(list[ReplacementJSON], json.load(f))
    return [Replacement.from_dict(data) for data in data_list]


def apply_replacements(
    script_en: list[str], replacements: list[Replacement]
) -> list[str]:
    for replacement in replacements:
        original_txt: str = replacement.original
        replacement_txt: str = replacement.replacement
        line: int | str = int(replacement.line) if replacement.line != "all" else "all"
        if line == "all":
            script_en = [
                line_en.replace(original_txt, replacement_txt) for line_en in script_en
            ]
        elif isinstance(line, int):
            script_en[line - 1] = script_en[line - 1].replace(
                original_txt, replacement_txt
            )
    return script_en
