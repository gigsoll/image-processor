import re
import numpy as np
import cv2
from numpy._typing import NDArray
from .function_timer import function_timer
import math


class OrdereDithering:
    def __init__(self) -> None:
        self.x2_table = self.preprocess_table([[0, 2], [3, 1]])
        self.x4_table = self.preprocess_table(
            [
                [0, 8, 2, 10],
                [12, 4, 14, 6],
                [3, 11, 1, 9],
                [15, 7, 13, 5],
            ]
        )
        self.x8_table = self.preprocess_table(
            [
                [0, 32, 8, 40, 2, 34, 8, 42],
                [48, 16, 56, 24, 50, 18, 58, 26],
                [12, 44, 4, 26, 14, 46, 6, 38],
                [60, 28, 52, 20, 62, 30, 54, 22],
                [3, 35, 11, 43, 1, 33, 9, 41],
                [51, 19, 59, 27, 49, 17, 57, 25],
                [15, 47, 7, 39, 13, 45, 5, 37],
                [63, 31, 55, 23, 61, 29, 53, 21],
            ]
        )
        self.dither(self.x4_table)

    @function_timer
    def dither(self, table):
        image = cv2.imread("./images/ліс.png") / 255
        n = len(table)
        x_tile, y_tile = (
            math.ceil(image.shape[0] / n),
            math.ceil(image.shape[1] / n),
        )
        x_over, y_over = (image.shape[0] % n, image.shape[1] % n)
        tile_map = np.tile(table, (x_tile, y_tile))
        tile_map = self._reshape(tile_map, x_over, y_over)
        b = (image[:, :, 0] > tile_map).astype(int)
        g = (image[:, :, 1] > tile_map).astype(int)
        r = (image[:, :, 2] > tile_map).astype(int)
        bgr = np.stack((b, g, r), axis=-1)
        colors = bgr * 255
        cv2.imwrite("res.png", colors)

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

    def preprocess_table(self, table: list[list[int]]) -> list[list[float]]:
        max, n = np.amax(table), len(table)
        result: list[list[float]] = [
            [float(table[i][j] / n**2 - (0.5 * 1 / max)) for i in range(len(table))]
            for j in range(len(table[0]))
        ]
        return result


od = OrdereDithering()
