import cv2
from typing import Self
from numpy._typing import NDArray
from PIL import Image
from gistqd.backend.helpers.function_timer import function_timer
from gistqd.backend.processors.palette_quantizer import PaletteRemaper
from gistqd.backend.processors.ordered_dithering import OrdereDithering


class ImagePipeline:
    @function_timer
    def __init__(self, image_path: str) -> None:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError("Image is wrong")

        self.in_path = image_path
        self.image: NDArray = image

    def remap_to_existing_palette(self, palette_path: str) -> Self:
        remaper = PaletteRemaper(self.image, palette_path)
        self.image = remaper.map_to_colors()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
        return self

    def quantize(self, n_colors) -> Self:
        allowed_colors: list[int] = [8, 27, 64]
        n_div_map: dict[int, int] = {8: 128, 27: 86, 64: 64}
        if n_colors not in allowed_colors:
            raise ValueError(f"Wrong number of colors, should be in {allowed_colors}")
        div = n_div_map[n_colors]
        self.image = cv2.cvtColor(
            PaletteRemaper.quantize(self.image, div), cv2.COLOR_RGB2BGR
        )
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

        return self

    def denoice(self) -> Self:
        new_image = cv2.fastNlMeansDenoisingColored(self.image, None, 10, 10, 7, 21)
        self.image = new_image
        return self

    def dither_basic(self, grid_size: int) -> Self:
        od = OrdereDithering(grid_size, self.image)
        self.image = od.apply_basic_colors()
        return self

    def dither_palette(self, grid_size: int, palette_path: str) -> Self:
        od = OrdereDithering(grid_size, self.image)
        self.image = od.apply_color_palette(palette_path)
        return self

    def write(self, path: str) -> None:
        cv2.imwrite(path, self.image)


@function_timer
def main(image_path: str, palette_path: str) -> None:
    image = ImagePipeline(image_path).denoice().remap_to_existing_palette(palette_path)
    Image.fromarray(image.image).show()
