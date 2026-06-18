from pathlib import Path

from mahoyo_patcher.models.language import Language
from mahoyo_tools.hfa import HfaArchive


class HfaManager:
    def __init__(self, game_path: Path, hfa_path: Path) -> None:
        self.game_path: Path = game_path
        self.hfa_path: Path = hfa_path

    def extract(self, language: Language, output_file: str) -> None:
        output_path: Path = self.game_path / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with HfaArchive(self.hfa_path.as_posix(), mode="r") as archive:
            archive[language].extract(output_path.as_posix())

    def inject(self, language: Language, output_file: str) -> None:
        output_path: Path = self.game_path / output_file
        with HfaArchive(self.hfa_path.as_posix(), mode="rw") as archive:
            archive[language].inject(output_path.as_posix())
