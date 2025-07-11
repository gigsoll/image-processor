import cv2
import math
from PIL import Image
import numpy as np
from models import ImportPalette, ImageData
from palete_io import read_palete


def read_image(file_path: str) -> ImageData:
    image = cv2.imread(file_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.bilateralFilter(image, 9, 75, 75)

    color_line = np.dstack(image.transpose(2, 0, 1).reshape(3, -1))[0]

    Image.fromarray(color_line.reshape(
        image.shape[0], image.shape[1], 3)).show()
    return ImageData(image.shape[0], image.shape[1], color_line)


def get_unique_colors(image: ImageData) -> ImportPalette:
    colors = image.colors
    unique_colors: ImportPalette = ImportPalette(
        name="unique_colors", colors=np.unique(colors, axis=0)
    )
    return unique_colors


def map_palette_euclidean(
    colors: ImportPalette, palette: ImportPalette
) -> dict[tuple[int, int, int], tuple[int, int, int]]:
    mapping: dict[tuple[int, int, int], tuple[int, int, int]] = {}

    for color in colors.colors:
        min_distance = float("inf")
        closest_color = None

        for palette_color in palette.colors:
            distance = math.sqrt(
                (int(color[0]) - int(palette_color[0])) ** 2
                + (int(color[1]) - int(palette_color[1])) ** 2
                + (int(color[2]) - int(palette_color[2])) ** 2
            )
            if distance < min_distance:
                min_distance = distance
                closest_color = palette_color

        mapping[tuple(color)] = closest_color

    return mapping


def map_image(image: ImageData, mapping: dict[tuple, tuple]) -> None:
    new_colors = np.array([mapping[tuple(color)] for color in image.colors])
    img = Image.fromarray(
        new_colors.reshape(image.height, image.width, 3).astype(np.uint8)
    )
    img.show()


if __name__ == "__main__":
    picture = read_image("./images/ліс.png")
    palette = read_palete("./palletes/catpuccin_mocha.json")
    unique = get_unique_colors(picture)
    mapping = map_palette_euclidean(unique, palette)
    map_image(picture, mapping)
