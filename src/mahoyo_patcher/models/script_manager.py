from pathlib import Path


class ScriptManager:
    def __init__(self, game_path: Path, input_file: str, output_file: str):
        self.input_path: Path = game_path / input_file
        self.output_path: Path = game_path / output_file

    def get_script(self) -> list[str]:
        with open(self.input_path, mode="r", encoding="utf-8") as f:
            return f.readlines()

    def set_script(self, script: list[str]) -> None:
        with open(self.output_path, mode="w", encoding="utf-8") as f:
            f.writelines(script)
