from typing import Self
from numpy._typing import NDArray
import cv2
from PIL import Image
import numpy as np
from .models import ImportPalette
from .function_timer import function_timer
from .palete_io import read_palete


class ImagePipeline:
    @function_timer
    def __init__(self, image_path: str) -> None:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError("Image is wrong")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.image: NDArray = image

    @function_timer
    def remap_to_existing_palette(self, palette_path: str) -> Self:
        """
        Selects unique colors and map them to a color from palette
        based on euclidian distance between unique colors and palette
        """

        # convert image to a line of colors  so they are more faster to process
        colors_1d = self.image.reshape(-1, 3)
        tuple_line: tuple[tuple[int, ...], ...] = tuple(
            map(lambda row: (int(row[0]), int(row[1]), int(row[2])), colors_1d)
        )
        unique_colors: ImportPalette = ImportPalette(
            name="unique_colors", colors=set(tuple_line)
        )

        # go through each color and map it using dict
        mapping: dict[tuple[int, ...], tuple[int, ...]] = {}
        palette = read_palete(palette_path)

        # find the closest color
        for color in unique_colors.colors:
            min_distance = float("inf")
            closest_color: tuple[int, ...] = (0, 0, 0)

            for palette_color in palette.colors:
                distance = (
                    ((color[0]) - (palette_color[0])) ** 2
                    + ((color[1]) - (palette_color[1])) ** 2
                    + ((color[2]) - (palette_color[2])) ** 2
                )
                if distance < min_distance:
                    min_distance = distance
                    closest_color: tuple[int, ...] = palette_color

            mapping[color] = closest_color

        mapped = np.array([mapping[color]
                          for color in tuple_line], dtype="uint8")
        dim = self.image.shape
        self.image = mapped.reshape(dim)
        return self

    @function_timer
    def denoice(self) -> Self:
        new_image = cv2.fastNlMeansDenoisingColored(
            self.image, None, 10, 10, 7, 21)
        self.image = new_image
        return self


@function_timer
def main(image_path: str, palette_path: str) -> None:
    image = ImagePipeline(image_path).denoice(
    ).remap_to_existing_palette(palette_path)
    Image.fromarray(image.image).show()
