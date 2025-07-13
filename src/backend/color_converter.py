import cv2
from PIL import Image
import numpy as np
from .models import ImportPalette, ImageData
from .function_timer import function_timer
from .palete_io import read_palete


@function_timer
def read_image(file_path: str) -> ImageData:
    image = cv2.imread(file_path)
    if image is None:
        raise FileNotFoundError("Image is wrong")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    color_line = image.reshape(-1, 3)
    tuple_line: tuple[tuple[int, ...], ...] = tuple(
        map(lambda row: (int(row[0]), int(row[1]), int(row[2])), color_line)
    )
    return ImageData(image.shape[0], image.shape[1], tuple_line)


@function_timer
def quantize(image: ImageData, n_clusters):
    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        10,
        1.0,
    )  # KMeans stops in case either 10 iterations happened or 100% quality labels acheaved
    flags = cv2.KMEANS_RANDOM_CENTERS  # random starting points
    z = np.float32(np.array(image.colors))
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
def get_unique_colors(image: ImageData) -> ImportPalette:
    colors = image.colors
    unique_colors: ImportPalette = ImportPalette(
        name="unique_colors", colors=set(colors)
    )
    return unique_colors


@function_timer
def map_palette_euclidean(
    colors: ImportPalette, palette: ImportPalette
) -> dict[tuple[int, ...], tuple[int, ...]]:
    mapping: dict[tuple[int, ...], tuple[int, ...]] = {}
    for color in colors.colors:
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

    return mapping


@function_timer
def map_image(image: ImageData, mapping: dict[tuple, tuple]) -> None:
    new_colors = np.array([mapping[color] for color in image.colors])
    img = Image.fromarray(
        new_colors.reshape(image.height, image.width, 3).astype(np.uint8)
    )
    img.show()


@function_timer
def main(image_path: str, palette_path: str) -> None:
    picture = read_image(image_path)
    palette = read_palete(palette_path)
    unique = get_unique_colors(picture)
    mapping = map_palette_euclidean(unique, palette)
    map_image(picture, mapping)
