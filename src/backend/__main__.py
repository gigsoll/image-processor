import sys
from backend.models.image_pipeline import main

image_path = sys.argv[1]
palette_path = sys.argv[2]

main(image_path, palette_path)
