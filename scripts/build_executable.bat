@echo off
setlocal

cd /d "%~dp0\.."
uv run pyinstaller --clean --noconfirm spec\Mahoyo_Patcher.spec
rename dist\Mahoyo_Patcher.exe Mahoyo_Patcher-windows.exe
