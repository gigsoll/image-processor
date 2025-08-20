import numpy as np
from numpy._typing import NDArray
from backend.helpers.function_timer import function_timer
import math
from backend.models.palette import Palette


class OrdereDithering:
    def __init__(self, table_size: int, image: NDArray) -> None:
        if table_size not in [2, 4, 8]:
            raise ValueError("Wront table size, it should be 2, 4 or 8")

        table_map: dict[int, list[list[int]]] = {
            2: [[0, 2], [3, 1]],
            4: [
                [0, 8, 2, 10],
                [12, 4, 14, 6],
                [3, 11, 1, 9],
                [15, 7, 13, 5],
            ],
            8: [
                [0, 32, 8, 40, 2, 34, 8, 42],
                [48, 16, 56, 24, 50, 18, 58, 26],
                [12, 44, 4, 26, 14, 46, 6, 38],
                [60, 28, 52, 20, 62, 30, 54, 22],
                [3, 35, 11, 43, 1, 33, 9, 41],
                [51, 19, 59, 27, 49, 17, 57, 25],
                [15, 47, 7, 39, 13, 45, 5, 37],
                [63, 31, 55, 23, 61, 29, 53, 21],
            ],
        }
        self.table: list[list[float]] = self._preprocess_table(table_map[table_size])
        self.image: NDArray = image

    @function_timer
    def _dither(self) -> NDArray:
        image: NDArray = self.image / 255
        n = len(self.table)
        x_tile, y_tile = (
            math.ceil(image.shape[0] / n),
            math.ceil(image.shape[1] / n),
        )
        x_over, y_over = (x_tile * n - image.shape[0], y_tile * n - image.shape[1])
        tile_map = np.tile(self.table, (x_tile, y_tile))
        tile_map = self._reshape(tile_map, x_over, y_over)
        b = (image[:, :, 0] > tile_map).astype(int)
        g = (image[:, :, 1] > tile_map).astype(int)
        r = (image[:, :, 2] > tile_map).astype(int)
        bgr: NDArray = np.stack((b, g, r), axis=-1)
        return bgr

    def apply_basic_colors(self) -> NDArray:
        colors = self._dither() * 255
        return colors

    def apply_color_palette(self, palette_path: str) -> NDArray:
        colors = self._dither()
        palette = Palette.read(palette_path)

        def reverse(rgb: list[int]) -> list[int]:
            return list(reversed(rgb))

        processed = {
            (0, 0, 0): reverse(palette.black),
            (0, 0, 1): reverse(palette.red),
            (0, 1, 0): reverse(palette.green),
            (0, 1, 1): reverse(palette.yellow),
            (1, 0, 0): reverse(palette.blue),
            (1, 0, 1): reverse(palette.magenta),
            (1, 1, 0): reverse(palette.cyan),
            (1, 1, 1): reverse(palette.white),
        }

        for key, value in processed.items():
            keys = np.array(key)
            mask = np.all(colors == keys, axis=-1)
            indexes = np.where(mask)
            colors[indexes] = value

        return colors

    @staticmethod
    def _reshape(table: NDArray, x_over, y_over) -> NDArray:
        if x_over > 0 and y_over > 0:
            return table[:-x_over, :-y_over]
        elif x_over > 0:
            return table[:-x_over, :]
        elif y_over > 0:
            return table[:, :-y_over]
        else:
            return table

    def _preprocess_table(self, table: list[list[int]]) -> list[list[float]]:
        max, n = np.amax(table), len(table)
        result: list[list[float]] = [
            [float(table[i][j] / n**2 - (0.5 * 1 / max)) for i in range(len(table))]
            for j in range(len(table[0]))
        ]
        return result
