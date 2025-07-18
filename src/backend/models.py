from dataclasses import dataclass


@dataclass()
class ImportPalette:
    name: str
    colors: tuple[tuple[int, ...], ...] | set[tuple[int, ...]]


@dataclass()
class ExportPalette:
    name: str
    colors: list[str]


@dataclass()
class ImageData:
    height: int
    width: int
    colors: tuple[tuple[int, ...], ...]
