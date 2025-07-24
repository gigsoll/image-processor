import cv2
import math
import numpy as np
from numpy._typing import NDArray

from backend.function_timer import function_timer
from backend.models import Palette


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

    @function_timer
    def scale_down(self) -> NDArray:
        MIN_DIM1 = 1600
        MIN_DIM2 = 900
        shape = self.image.shape[0:2]
        reshape_area, image_area = MIN_DIM1 * MIN_DIM2, shape[0] * shape[1]
        scale_factor: float = 1
        if image_area > reshape_area:
            scale_factor = round(image_area / reshape_area, 3)
        scaled_down: NDArray = cv2.resize(
            self.image, tuple(math.floor(d / scale_factor) for d in shape)
        )
        return scaled_down

    def _get_closest_color(
        self, color: list[int], colors_list: list[list[int]]
    ) -> list[int]:
        color_array = np.array(color, dtype=np.float64)
        colors_array = np.array(colors_list, dtype=np.float64)

        distances = np.sum((colors_array - color_array) ** 2, axis=1)
        closest_id = np.argmin(distances)

        return colors_list[closest_id]

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
        resized = self.image.reshape(-1, 3)
        unique = np.unique(resized, axis=0)
        mapping = self.create_mapping(unique, self.colors)
        colors_1d = self.image.reshape(-1, 3)
        tuple_line: tuple[tuple[int, ...], ...] = tuple(
            map(lambda row: (int(row[0]), int(row[1]), int(row[2])), colors_1d)
        )

        mapped = np.array([mapping[color] for color in tuple_line], dtype="uint8")
        dim = self.image.shape
        return cv2.cvtColor(mapped.reshape(dim), cv2.COLOR_RGB2BGR)
