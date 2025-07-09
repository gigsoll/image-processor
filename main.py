from PIL import Image
from KMeans import KMeans


def create_mapping(image_path: str, palete_size: int) -> dict[tuple, list]:
    im: Image = Image.open(image_path).convert("RGB")

    colors = im.getcolors(maxcolors=im.height * im.width)
    color_data = dict(
        zip([color[1] for color in colors], [color[0] for color in colors])
    )
    colors = [color[1] for color in colors]
    palette = [
        color[0]
        for color in sorted(color_data.items(), key=lambda x: x[1], reverse=True)[
            :palete_size
        ]
    ]
    k_means = KMeans(colors, palette)
    maping = k_means.asign_to_centroid()
    return maping


def process_image(image_path: str, n_colors: int) -> None:
    image: Image = Image.open(image_path).convert("RGB").quantize(colors=n_colors)
    # maping = create_mapping(image_path, n_colors)
    # pixels = image.load()
    # for i in range(image.size[0]):
    #     for j in range(image.size[1]):
    #         for color, mapped_to in maping.items():
    #             if pixels[i, j] in mapped_to:
    #                 pixels[i, j] = color
    #                 break
    image.show()


if __name__ == "__main__":
    process_image("./images/Mountain.jpg", 10)
