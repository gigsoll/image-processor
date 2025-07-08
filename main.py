from PIL import Image
import numpy as np
from pprint import pprint

image_path = "./images/fire.png"
im = Image.open(image_path)
x = np.asarray(im)

for el in x:
    for sel in el:
        print(sel)
