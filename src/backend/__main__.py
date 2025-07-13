import sys
from .color_converter import main

image_path = sys.argv[1]
palette_path = sys.argv[2]

main(image_path, palette_path)
