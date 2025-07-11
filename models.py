from dataclasses import dataclass
from numpy._typing import NDArray


@dataclass()
class ImportPalette:
    name: str
    colors: list[list[int]] | NDArray


@dataclass()
class ExportPalette:
    name: str
    colors: list[str]


@dataclass()
class ImageData:
    height: int
    width: int
    colors: list[list[int]] | NDArray
