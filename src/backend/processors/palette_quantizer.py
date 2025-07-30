import cv2
import numpy as np
from numpy._typing import NDArray
from itertools import product

from backend.helpers.function_timer import function_timer
from backend.models.palette import Palette


class PaletteRemaper:
    def __init__(self, image: NDArray, palette_path: str) -> None:
        self.image: NDArray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.colors = self._pal2cols(palette_path)

    @staticmethod
    def _pal2cols(path: str) -> list[list[int]]:
        palette: Palette = Palette.read(path)
        colors: list[list[int]] = palette.additional
        color_names = [
            "black",
            "red",
            "green",
            "blue",
            "yellow",
            "magenta",
            "cyan",
            "white",
        ]
        colors.extend([getattr(palette, color) for color in color_names])
        return colors

    def _get_closest_color(
        self, color: list[int], colors_list: list[list[int]]
    ) -> list[int]:
        color_array = np.array(color, dtype=np.float64)
        colors_array = np.array(colors_list, dtype=np.float64)

        distances = np.sum((colors_array - color_array) ** 2, axis=1)
        closest_id = np.argmin(distances)

        return colors_list[closest_id]

    @staticmethod
    def quantize(image: NDArray, div: int) -> NDArray:
        result = image // div * div + div // 2
        return result

    @function_timer
    def create_mapping(
        self, un_cols: list[list[int]], pal_cols: list[list[int]]
    ) -> dict[tuple[int, ...], list[int]]:
        keys: list[tuple[int, ...]] = [tuple(item) for item in un_cols]
        closest: list[list[int]] = [
            self._get_closest_color(cur, pal_cols) for cur in un_cols
        ]
        return dict(zip(keys, closest))

    @function_timer
    def map_to_colors(self):
        DIVISIOTR = 86  # to get 64 unique colors
        quantized = self.quantize(self.image, DIVISIOTR)
        unique_channel_values = set(
            [c // DIVISIOTR * DIVISIOTR + DIVISIOTR // 2 for c in range(0, 256)]
        )
        unique_colors = list(product(unique_channel_values, repeat=3))
        mapping = self.create_mapping(unique_colors, self.colors)
        for key, value in mapping.items():
            key = np.array(key)
            mask = np.all(quantized == key, axis=-1)
            idx = np.where(mask)
            quantized[idx] = value
        return quantized
