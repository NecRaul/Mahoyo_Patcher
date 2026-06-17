import json
import os
import platform
import re
import sys

from classes import Replacement


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


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # ty:ignore[unresolved-attribute]
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def autodetect_game_path():
    """Attempts to find the game installation path via Windows Registry."""
    if platform.system() != "Windows":
        return None

    import winreg

    STEAM_APP_ID = "2052410"

    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App "
        + STEAM_APP_ID,
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Steam App "
        + STEAM_APP_ID,
    ]

    for reg_path in reg_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:  # ty:ignore[unresolved-attribute]
                install_loc, _ = winreg.QueryValueEx(key, "InstallLocation")  # ty:ignore[unresolved-attribute]
                if os.path.isdir(install_loc):
                    return install_loc
        except Exception:
            continue

    return None
