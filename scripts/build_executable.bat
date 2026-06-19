@echo off
setlocal

cd /d "%~dp0\.."
uv run pyinstaller --clean --noconfirm spec\Mahoyo_Patcher.spec
