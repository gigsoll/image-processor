import cv2
import numpy as np
from models import ImportPalette


def get_unique_colors(file_path: str) -> ImportPalette:
    image = cv2.imread(file_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    color_line = np.dstack(image.transpose(2, 0, 1).reshape(3, -1))[0]

    unique_colors: ImportPalette = ImportPalette(
        name="unique_colors", colors=np.unique(color_line, axis=0)
    )
    return unique_colors


if __name__ == "__main__":
    print(get_unique_colors("./images/Linux.png"))
