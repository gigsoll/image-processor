from pydantic import BaseModel


class ImportPalette(BaseModel):
    name: str
    colors: list[tuple[int, int, int]]


class ExportPalette(ImportPalette):
    colors: list[str]
