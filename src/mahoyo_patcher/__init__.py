from importlib.metadata import PackageNotFoundError, version

__all__: list[str] = ["__version__"]

try:
    __version__: str = version("mahoyo-patcher")
except PackageNotFoundError:
    __version__ = "dev"
