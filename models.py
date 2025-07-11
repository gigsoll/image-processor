from dataclasses import dataclass


@dataclass()
class ImportPalette:
    name: str
    colors: list[list[int]]


@dataclass()
class ExportPalette(ImportPalette):
    colors: list[str]


@dataclass()
class ImageData:
    height: int
    width: int
    colors: list[list[int]]
