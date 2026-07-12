#!/usr/bin/env python3

import subprocess
from pathlib import Path

spec_dir: Path = Path("spec")
spec_dir.mkdir(exist_ok=True)

subprocess.run(
    [
        "uv",
        "run",
        "pyinstaller",
        "--name",
        "Mahoyo_Patcher",
        "--onefile",
        "--windowed",
        "--paths",
        "src",
        "--collect-data",
        "mahoyo_patcher",
        "--icon",
        "src/mahoyo_patcher/resources/icon.ico",
        "--specpath",
        str(spec_dir),
        "src/mahoyo_patcher/__main__.py",
    ],
    check=True,
)

spec: Path = spec_dir / "Mahoyo_Patcher.spec"

text: str = spec.read_text()

replacements: list[tuple[str, str]] = [
    (
        "from PyInstaller.utils.hooks import collect_data_files\n",
        "from PyInstaller.utils.hooks import collect_data_files\n"
        "from pathlib import Path\n\n"
        "project_root = Path(SPECPATH).parent\n",
    ),
    (
        "['../src/mahoyo_patcher/__main__.py']",
        "[str(project_root / 'src/mahoyo_patcher/__main__.py')]",
    ),
    (
        "pathex=['src']",
        "pathex=[str(project_root / 'src')]",
    ),
    (
        "icon=['src/mahoyo_patcher/resources/icon.ico']",
        "icon=[str(project_root / 'src/mahoyo_patcher/resources/icon.ico')]",
    ),
    (
        "a.binaries",
        "[b for b in a.binaries if not b[0].startswith('libfontconfig')]",
    ),
]

for old, new in replacements:
    text = text.replace(old, new)

spec.write_text(text)
