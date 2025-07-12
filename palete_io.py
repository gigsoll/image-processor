import json
from dataclasses import asdict
from models import ImportPalette, ExportPalette


def read_palete(file_path: str) -> ImportPalette:
    with open(file_path, "r") as palettte_file:
        palette_data = json.load(palettte_file)

    name, hexes = palette_data["name"], palette_data["colors"]

    colors = [
        list(int(hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)) for hex in hexes
    ]
    return ImportPalette(name=name, colors=colors)


def write_palete(file_path, palete: ImportPalette) -> None:
    colors = ["#%02x%02x%02x" % tuple(color) for color in palete.colors]
    export = asdict(ExportPalette(name=palete.name, colors=colors))

    with open(file_path, "w") as palette_steam:
        json.dump(export, palette_steam, indent=4)


if __name__ == "__main__":
    write_palete(
        "./palletes/catpuccin_mocha.json",
        read_palete("./palletes/catpuccin_mocha.json"),
    )
