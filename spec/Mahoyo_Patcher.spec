# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from pathlib import Path

project_root = Path(SPECPATH).parent

datas = []
datas += collect_data_files('mahoyo_patcher')


a = Analysis(
    [str(project_root / 'src/mahoyo_patcher/__main__.py')],
    pathex=[str(project_root / 'src')],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [b for b in a.binaries if not b[0].startswith('libfontconfig')],
    a.datas,
    [],
    name='Mahoyo_Patcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[str(project_root / 'src/mahoyo_patcher/resources/icon.ico')],
)
