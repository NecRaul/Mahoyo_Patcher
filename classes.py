import os

from mahoyo_tools import hfa


class Extractor:
    def __init__(self, game_dir, hfa_path):
        self.GAME_DIR = game_dir
        self.hfa_path = os.path.join(self.GAME_DIR, hfa_path)
        self.archive = hfa.HfaArchive(self.hfa_path, "rw")

    def extract(self, script, filepath):
        full_path = os.path.normpath(os.path.join(self.GAME_DIR, filepath))
        directory = os.path.dirname(full_path)
        os.makedirs(directory, exist_ok=True)
        self.archive.open()
        entry = self.archive[script]
        entry.extract(full_path)
        self.archive.close()

    def inject(self, script, filepath):
        self.archive.open()
        entry = self.archive[script]
        entry.inject(os.path.join(self.GAME_DIR, filepath))
        self.archive.close()


class Replacer:
    def __init__(self, game_dir, input_path, output_path):
        self.in_path = os.path.join(game_dir, input_path)
        self.out_path = os.path.join(game_dir, output_path)

    def get_script(self):
        with open(self.in_path, "r", encoding="utf-8") as f:
            return f.readlines()

    def set_script(self, text):
        with open(self.out_path, "w", encoding="utf-8") as f:
            f.writelines(text)


class Replacement:
    def __init__(self, line, original, replacement, comment=""):
        self.line = line
        self.original = original
        self.replacement = replacement
        self.comment = comment
