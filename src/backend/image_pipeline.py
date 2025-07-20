from typing import Self
from numpy._typing import NDArray
from PIL import Image
from .function_timer import function_timer
import cv2
from .palette_quantizer import PaletteRemaper


class ImagePipeline:
    @function_timer
    def __init__(self, image_path: str) -> None:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError("Image is wrong")

        self.image: NDArray = image

    def remap_to_existing_palette(self, palette_path: str) -> Self:
        remaper = PaletteRemaper(self.image, palette_path)
        self.image = remaper.remap_to_existing_palette()
        return self

    @function_timer
    def denoice(self) -> Self:
        new_image = cv2.fastNlMeansDenoisingColored(self.image, None, 10, 10, 7, 21)
        self.image = new_image
        return self

    @function_timer
    def dither_basic(self, grid_size: int) -> Self:
        print(grid_size)
        return self

    def write(self, path: str) -> None:
        cv2.imwrite(path, self.image)


@function_timer
def main(image_path: str, palette_path: str) -> None:
    image = ImagePipeline(image_path).denoice().remap_to_existing_palette(palette_path)
    Image.fromarray(image.image).show()
