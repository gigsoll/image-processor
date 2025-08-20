from dataclasses import asdict, dataclass
from os import path, makedirs
import os
from platformdirs import PlatformDirs
import tomllib
import shutil


@dataclass()
class Config:
    palette_dir: str
    default_output_dir: str
    quantize_n_colors: int
    dither_grid_size: str

    def read_config(self):
        platform_dirs = PlatformDirs("gistqd", "gigsoll")
        config_dir = platform_dirs.user_config_path
        config_location = path.join(config_dir, "config.toml")
        if not path.exists(config_dir):
            makedirs(config_dir)
            makedirs(path.join(config_dir, "palettes"))
        if not path.exists(config_location):
            shutil.copy("default.toml", config_location)

        with open(config_location, "rb") as config_file:
            config_content = tomllib.load(config_file)
        print(config_content)


c = Config("", "", 1, "")
c.read_config()
