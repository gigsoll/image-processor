import numpy as np
import cv2
from .function_timer import function_timer


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
        image = cv2.imread("./images/ign_herakles.png") / 255
        n = len(table)
        dithered = (
            np.array(
                [
                    [
                        [
                            int(image[i][j][0] > table[i % n][j % n]),
                            int(image[i][j][1] > table[i % n][j % n]),
                            int(image[i][j][2] > table[i % n][j % n]),
                        ]
                        for j in range(image.shape[1])
                    ]
                    for i in range(image.shape[0])
                ],
                dtype="uint8",
            )
            * 255
        )
        cv2.imwrite("res.png", dithered)

    def preprocess_table(self, table: list[list[int]]) -> list[list[float]]:
        max, n = np.amax(table), len(table)
        result: list[list[float]] = [
            [float(table[i][j] / n**2 - (0.5 * 1 / max)) for i in range(len(table))]
            for j in range(len(table[0]))
        ]
        return result


od = OrdereDithering()
