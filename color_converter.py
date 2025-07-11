import cv2
import math
from PIL import Image
import numpy as np
from models import ImportPalette, ImageData
from palete_io import read_palete


def read_image(file_path: str) -> ImageData:
    image = cv2.imread(file_path)
    if image is None:
        raise FileNotFoundError("Image is wrong")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    color_line = image.reshape(-1, 3)

    Image.fromarray(color_line.reshape(
        image.shape[0], image.shape[1], 3)).show()
    return ImageData(image.shape[0], image.shape[1], color_line)


# TODO: Improve speed of color finding
def get_unique_colors(image: ImageData) -> ImportPalette:
    colors = image.colors
    unique_colors: ImportPalette = ImportPalette(
        name="unique_colors", colors=np.unique(colors, axis=0)
    )
    return unique_colors


# TODO: Reduce time complexity from O(n^2) to something more barable
def map_palette_euclidean(
    colors: ImportPalette, palette: ImportPalette
) -> dict[tuple[int, ...], list[int]]:
    mapping: dict[tuple[int, ...], list[int]] = {}

    for color in colors.colors:
        min_distance = float("inf")
        closest_color = []

        for palette_color in palette.colors:
            distance = math.sqrt(
                (int(color[0]) - int(palette_color[0])) ** 2
                + (int(color[1]) - int(palette_color[1])) ** 2
                + (int(color[2]) - int(palette_color[2])) ** 2
            )
            if distance < min_distance:
                min_distance = distance
                closest_color: list[int] = palette_color

        mapping[tuple(color)] = closest_color

    return mapping


def map_image(image: ImageData, mapping: dict[tuple, list]) -> None:
    new_colors = np.array([mapping[tuple(color)] for color in image.colors])
    img = Image.fromarray(
        new_colors.reshape(image.height, image.width, 3).astype(np.uint8)
    )
    img.show()


if __name__ == "__main__":
    picture = read_image("./images/ign_herakles.png")
    palette = read_palete("./palletes/catpuccin_mocha.json")
    unique = get_unique_colors(picture)
    mapping = map_palette_euclidean(unique, palette)
    map_image(picture, mapping)
