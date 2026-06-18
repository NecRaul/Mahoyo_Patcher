import sys
from contextlib import ExitStack
from importlib.resources import as_file, files
from importlib.resources.abc import Traversable
from pathlib import Path

_resource_stack = ExitStack()


def get_resource_path(package: str, resource: str) -> Path:
    traversable: Traversable = files(package).joinpath(resource)
    return _resource_stack.enter_context(as_file(traversable))


def autodetect_game_path() -> Path | None:
    if sys.platform == "win32":
        import winreg

        steam_app_id: str = "2052410"
        reg_base: str = (
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App "
            + steam_app_id
        )
        reg_paths: list[str] = [
            reg_base,
            reg_base.replace(
                r"SOFTWARE\Microsoft",
                r"SOFTWARE\Wow6432Node\Microsoft",
            ),
        ]
        for reg_path in reg_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                    result: tuple[str, int] = winreg.QueryValueEx(
                        key, "InstallLocation"
                    )
                    install_location, _ = result
                    if not isinstance(install_location, str):
                        continue
                    game_path = Path(install_location)
                    if game_path.is_dir():
                        return game_path
            except FileNotFoundError:
                continue
    else:
        game_name: str = "Witch On The Holy Night"
        path: Path = Path.home() / ".local/share/Steam/steamapps/common" / game_name
        if path.is_dir():
            return path

    return None
