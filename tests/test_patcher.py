import shutil
from pathlib import Path

import pytest

from mahoyo_patcher.constants import PATCHED_SCRIPT, SCRIPT_EN, SCRIPT_JP
from mahoyo_patcher.core.honorifics import apply_honorifics
from mahoyo_patcher.models import ScriptManager, apply_replacements, load_replacements
from mahoyo_patcher.utils import get_resource_path

FIXTURE_PATH = Path(__file__).parent / "fixtures"
SCRIPT_EN_FIXTURE = FIXTURE_PATH / "script_en.txt"
SCRIPT_JP_FIXTURE = FIXTURE_PATH / "script_jp.txt"
PATCHED_SCRIPT_FIXTURE = FIXTURE_PATH / "script_en_patched.txt"


@pytest.mark.skipif(
    not all(
        fixture.exists()
        for fixture in [SCRIPT_EN_FIXTURE, SCRIPT_JP_FIXTURE, PATCHED_SCRIPT_FIXTURE]
    ),
    reason=(
        "script_en.txt, script_jp.txt, and script_en_patched.txt fixtures "
        "are not present"
    ),
)
def test_script_en_reproduces_script_en_patched(tmp_path: Path) -> None:
    extracted_path = tmp_path / "extracted"
    extracted_path.mkdir()

    shutil.copyfile(SCRIPT_EN_FIXTURE, tmp_path / SCRIPT_EN)
    shutil.copyfile(SCRIPT_JP_FIXTURE, tmp_path / SCRIPT_JP)
    shutil.copyfile(PATCHED_SCRIPT_FIXTURE, tmp_path / PATCHED_SCRIPT)

    script_manager = ScriptManager(tmp_path, SCRIPT_EN, PATCHED_SCRIPT)
    script_en: list[str] = script_manager.get_script()
    script_jp: list[str] = (
        (tmp_path / SCRIPT_JP).read_text(encoding="utf-8").splitlines(keepends=True)
    )

    for filename in [
        "translation_mistakes.json",
        "americanisms.json",
        "unit_conversions.json",
        "romanizations.json",
        "name_order.json",
    ]:
        script_en = apply_replacements(
            script_en,
            load_replacements(get_resource_path("mahoyo_patcher.data", filename)),
        )

    script_en = apply_honorifics(script_en, script_jp)
    script_en = apply_replacements(
        script_en,
        load_replacements(
            get_resource_path("mahoyo_patcher.data", "honorific_edge_cases.json")
        ),
    )
    script_manager.set_script(script_en)

    assert (tmp_path / PATCHED_SCRIPT).read_text(
        encoding="utf-8"
    ) == PATCHED_SCRIPT_FIXTURE.read_text(encoding="utf-8")
