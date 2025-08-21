from dataclasses import dataclass
from os import path, makedirs
from platformdirs import PlatformDirs
import tomllib
import shutil


@dataclass(init=False)
class Config:
    palette_dir: str
    default_output_dir: str
    quantize_n_colors: int
    dither_grid_size: str

    def __init__(self, config_path: str | None):
        try:
            config = self.read_config(config_path)
        except FileNotFoundError:
            self._handle_missing_config()
            config = self.read_config(config_path)
        try:
            self.palette_dir = config["palette_dir"]
            self.default_output_dir = config["default_output_dir"]
            self.quantize_n_colors = config["quantize_n_colors"]
            self.dither_grid_size = config["dither_grid_size"]
        except KeyError:
            print("Config is corrupted")

    def read_config(self, config_location: str | None = None) -> dict:
        if config_location is None:
            config_location = self._handle_default_config()

        with open(config_location, "rb") as config_file:
            config_content = tomllib.load(config_file)

        return config_content

    def _handle_default_config(self) -> str:
        platform_dirs = PlatformDirs("gistqd", "gigsoll")
        config_dir = platform_dirs.user_config_path
        self._handle_missing_config()
        config_location = path.join(config_dir, "config.toml")
        return config_location

    @staticmethod
    def _handle_missing_config() -> None:
        platform_dirs = PlatformDirs("gistqd", "gigsoll")
        config_dir = platform_dirs.user_config_path
        if not path.exists(config_dir):
            makedirs(config_dir)
            shutil.copyfile(
                path.join(path.dirname(path.abspath(__file__)), "default.toml"),
                path.join(config_dir, "config.toml"),
            )
