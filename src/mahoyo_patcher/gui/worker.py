from pathlib import Path

from PySide6.QtCore import QThread, Signal

from mahoyo_patcher.core import Patcher


class Worker(QThread):
    progress_signal = Signal(int)
    status_signal = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(
        self, game_path: Path, hfa_path: Path, options: dict[str, bool]
    ) -> None:
        super().__init__()
        self.game_path: Path = game_path
        self.hfa_path: Path = hfa_path
        self.options: dict[str, bool] = options

    def run(self) -> None:
        try:
            patcher: Patcher = Patcher(
                self.game_path,
                self.hfa_path,
                self.options,
                progress_callback=self.patcher_progress,
            )
            patcher.backup_hfa()
            patcher.extract_scripts()
            patcher.load_scripts()
            patcher.apply_patches()
            patcher.save_script()
            patcher.inject_script()
            patcher.cleanup()
            self.finished_signal.emit(
                True,
                "Patch applied successfully!",
            )
        except Exception as e:
            self.finished_signal.emit(False, str(e))

    def patcher_progress(self, progress: int, status: str) -> None:
        self.progress_signal.emit(progress)
        self.status_signal.emit(status)
