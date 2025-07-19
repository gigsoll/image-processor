from .models import ImportPalette, ExportPalette
from numpy._typing import NDArray
from dataclasses import asdict
import json
import numpy as np


class PaletteRemaper:
    def __init__(self, image: NDArray, palette_path: str) -> None:
        self.image = image
        self.palette = self.read_palete(palette_path)

    def _extract_unique_colors(self, image: NDArray) -> ImportPalette:
        """Extract unique colors from image"""
        colors_1d = image.reshape(-1, 3)
        tuple_line: tuple[tuple[int, ...], ...] = tuple(
            map(lambda row: (int(row[0]), int(row[1]), int(row[2])), colors_1d)
        )
        return ImportPalette(name="unique_colors", colors=set(tuple_line))

    def _find_closest_color(
        self, color: tuple[int, ...], palette_colors: tuple[tuple[int, ...], ...]
    ) -> tuple[int, ...]:
        """
        Find the closest color to each part of the pallette using
        euclidian distance
        """
        min_distance = float("inf")
        closest_color: tuple[int, ...] = (0, 0, 0)

        for palette_color in palette_colors:
            distance = (
                ((color[0]) - (palette_color[0])) ** 2
                + ((color[1]) - (palette_color[1])) ** 2
                + ((color[2]) - (palette_color[2])) ** 2
            )
            if distance < min_distance:
                min_distance = distance
                closest_color: tuple[int, ...] = palette_color

        return closest_color

    def _create_color_mapping(
        self, unique_colors: ImportPalette
    ) -> dict[tuple[int, ...], tuple[int, ...]]:
        """
        Create mapping dictionary from unique colors to palette colors
        """
        mapping: dict[tuple[int, ...], tuple[int, ...]] = {}

        for color in unique_colors.colors:
            assert isinstance(self.palette.colors, tuple)
            mapping[color] = self._find_closest_color(color, self.palette.colors)

        return mapping

    def _apply_color_mapping(
        self, image: NDArray, mapping: dict[tuple[int, ...], tuple[int, ...]]
    ) -> NDArray:
        """
        Applies mapping to the image
        """
        colors_1d = image.reshape(-1, 3)
        tuple_line: tuple[tuple[int, ...], ...] = tuple(
            map(lambda row: (int(row[0]), int(row[1]), int(row[2])), colors_1d)
        )

        mapped = np.array([mapping[color] for color in tuple_line], dtype="uint8")
        dim = image.shape
        return mapped.reshape(dim)

    def remap_to_existing_palette(self) -> NDArray:
        """
        Selects unique colors and map them to a color from palette
        based on euclidian distance between unique colors and palette
        """
        # Extract unique colors from image
        unique_colors = self._extract_unique_colors(self.image)

        # Create mapping from unique colors to palette colors
        mapping = self._create_color_mapping(unique_colors)

        # Apply mapping to image
        self.image = self._apply_color_mapping(self.image, mapping)
        return self.image

    def read_palete(self, file_path: str) -> ImportPalette:
        with open(file_path, "r") as palettte_file:
            palette_data = json.load(palettte_file)

        name, hexes = palette_data["name"], palette_data["colors"]

        colors = tuple(
            tuple(int(hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
            for hex in hexes
        )
        return ImportPalette(name=name, colors=colors)

    def write_palete(self, file_path, palete: ImportPalette) -> None:
        colors = ["#%02x%02x%02x" % tuple(color) for color in palete.colors]
        export = asdict(ExportPalette(name=palete.name, colors=colors))

        with open(file_path, "w") as palette_steam:
            json.dump(export, palette_steam, indent=4)
