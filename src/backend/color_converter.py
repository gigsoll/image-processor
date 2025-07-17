from numpy._typing import NDArray
import cv2
from PIL import Image
import numpy as np
from .models import ImportPalette, ImageData
from .function_timer import function_timer
from .palete_io import read_palete


class ImagePipeline:
    @function_timer
    def __init__(self, image_path: str, pallete_path: str) -> None:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError("Image is wrong")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.image: NDArray = image

    @function_timer
    def quantize(self, n_clusters):
        criteria = (
            cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            10,
            1.0,
        )  # KMeans stops in case either 10 iterations happened or 100% quality labels acheaved
        flags = cv2.KMEANS_RANDOM_CENTERS  # random starting points
        z = np.float32(np.array(self.image_data.colors))
        _, labels, centers = cv2.kmeans(
            z,  # type: ignore
            n_clusters,
            None,  # type: ignore
            criteria,
            10,
            flags,
        )

    # TODO: Improve speed of color finding
    @function_timer
    def _get_unique_colors(self) -> tuple[ImportPalette, tuple]:
        colors_1d = self.image.reshape(-1, 3)
        tuple_line: tuple[tuple[int, ...], ...] = tuple(
            map(lambda row: (int(row[0]), int(row[1]), int(row[2])), colors_1d)
        )
        unique_colors: ImportPalette = ImportPalette(
            name="unique_colors", colors=set(tuple_line)
        )
        return unique_colors, tuple_line

    @function_timer
    def _map_palette_euclidean(
        self, palette_path: str
    ) -> tuple[dict[tuple[int, ...], tuple[int, ...]], tuple]:
        mapping: dict[tuple[int, ...], tuple[int, ...]] = {}
        palette = read_palete(palette_path)
        unique_colors, tuple_line = self._get_unique_colors()
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

        return mapping, tuple_line

    @function_timer
    def remap_to_existing_palette(self, palette_path: str) -> ImagePipeline:
        mapping = self._map_palette_euclidean(palette_path)
        for row in self.image:
            for color in row:
                row = mapping[color]

        return self

    @function_timer
    def denoice(img: NDArray) -> NDArray:
        new_image = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        return new_image


@function_timer
def main(image_path: str, palette_path: str) -> None:
    picture = read_image(image_path)
    palette = read_palete(palette_path)
    unique = get_unique_colors(picture)
    mapping = map_palette_euclidean(unique, palette)
    mapped_image = map_image(picture, mapping)
    Image.fromarray(mapped_image).show()
