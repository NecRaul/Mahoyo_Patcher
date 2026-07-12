import shutil
from collections.abc import Callable
from pathlib import Path

from mahoyo_patcher.constants import (
    PATCHED_SCRIPT,
    SCRIPT_EN,
    SCRIPT_JP,
)
from mahoyo_patcher.core.honorifics import apply_honorifics
from mahoyo_patcher.models import (
    HfaManager,
    Language,
    ScriptManager,
    apply_replacements,
    load_replacements,
)
from mahoyo_patcher.utils import get_resource_path

ProgressCallback = Callable[[int, str], None]


class Patcher:
    def __init__(
        self,
        game_path: Path,
        hfa_path: Path,
        options: dict[str, bool],
        progress_callback: ProgressCallback | None = None,
    ) -> None:
        self.game_path: Path = game_path
        self.hfa_path: Path = hfa_path
        self.options: dict[str, bool] = options
        self.progress_callback = progress_callback
        self.report(5, "Initializing patcher...")

        self.hfa_manager: HfaManager = HfaManager(
            self.game_path,
            self.hfa_path,
        )

        self.script_manager_en: ScriptManager = ScriptManager(
            self.game_path,
            SCRIPT_EN,
            PATCHED_SCRIPT,
        )

        self.script_manager_jp: ScriptManager = ScriptManager(
            game_path,
            SCRIPT_JP,
            SCRIPT_JP,
        )

    def backup_hfa(self) -> None:
        self.report(10, "Backing up HFA file...")
        backup_path: Path = self.hfa_path.with_suffix(self.hfa_path.suffix + ".bak")
        if not backup_path.exists():
            shutil.copy2(self.hfa_path, backup_path)

    def extract_scripts(self) -> None:
        self.report(15, "Extracting scripts...")
        self.hfa_manager.extract(Language.EN, SCRIPT_EN)
        self.hfa_manager.extract(Language.JP, SCRIPT_JP)

    def load_scripts(self) -> None:
        self.report(45, "Loading scripts...")
        self.script_en: list[str] = self.script_manager_en.get_script()
        self.script_jp: list[str] = self.script_manager_jp.get_script()

    def apply_patches(self) -> None:
        self.report(50, "Fixing translation mistakes...")
        self.script_en = apply_replacements(
            self.script_en,
            load_replacements(
                get_resource_path("mahoyo_patcher.data", "translation_mistakes.json")
            ),
        )
        self.report(55, "Fixing americanisms...")
        self.script_en = apply_replacements(
            self.script_en,
            load_replacements(
                get_resource_path("mahoyo_patcher.data", "americanisms.json")
            ),
        )
        if self.options["metric"]:
            self.report(60, "Converting units to metric...")
            self.script_en = apply_replacements(
                self.script_en,
                load_replacements(
                    get_resource_path("mahoyo_patcher.data", "unit_conversions.json")
                ),
            )
        if self.options["romanization"]:
            self.report(65, "Converting names to romanized forms...")
            self.script_en = apply_replacements(
                self.script_en,
                load_replacements(
                    get_resource_path("mahoyo_patcher.data", "romanizations.json")
                ),
            )
        if self.options["name_order"]:
            self.report(70, "Converting names to Japanese order...")
            self.script_en = apply_replacements(
                self.script_en,
                load_replacements(
                    get_resource_path("mahoyo_patcher.data", "name_order.json")
                ),
            )
        if self.options["honorifics"]:
            self.report(75, "Applying honorific and title changes...")
            self.script_en = apply_honorifics(self.script_en, self.script_jp)
            self.script_en = apply_replacements(
                self.script_en,
                load_replacements(
                    get_resource_path(
                        "mahoyo_patcher.data", "honorific_edge_cases.json"
                    )
                ),
            )

    def save_script(self) -> None:
        self.report(85, "Saving script...")
        self.script_manager_en.set_script(self.script_en)

    def inject_script(self) -> None:
        self.report(90, "Injecting script...")
        self.hfa_manager.inject(Language.EN, PATCHED_SCRIPT)

    def cleanup(self) -> None:
        self.report(95, "Cleaning up temporary files...")
        extracted_folder: Path = self.game_path / "extracted"
        if extracted_folder.exists():
            shutil.rmtree(extracted_folder)
        self.report(100, "Done")

    def report(self, progress: int, status: str) -> None:
        if self.progress_callback is not None:
            self.progress_callback(progress, status)
