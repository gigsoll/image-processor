from PIL import Image
from KMeans import KMeans
import matplotlib.pyplot as plt
import numpy as np


def process_image():
    image_path = "./images/fire.png"
    im: Image = Image.open(image_path)
    pixels = list(im.getdata())
    pixels = list(set(pixels))
    plot(pixels)


def plot(pixels: np.array):
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    pnp = np.asarray(pixels)
    ax.scatter(pnp[:, 0], pnp[:, 1], pnp[:, 2])
    plt.show()


if __name__ == "__main__":
    process_image()
