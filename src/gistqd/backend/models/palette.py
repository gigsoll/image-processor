from dataclasses import dataclass, field, asdict
from copy import copy
import json
import re
import shutil
from typing import Self
from os import path
from platformdirs import user_config_dir


@dataclass()
class Palette:
    name: str
    black: list[int] = field(default_factory=list)
    red: list[int] = field(default_factory=list)
    green: list[int] = field(default_factory=list)
    yellow: list[int] = field(default_factory=list)
    blue: list[int] = field(default_factory=list)
    magenta: list[int] = field(default_factory=list)
    cyan: list[int] = field(default_factory=list)
    white: list[int] = field(default_factory=list)
    additional: list[list[int]] = field(default_factory=list)

    @classmethod
    def factory(
        cls,
        name: str,
        black: str,
        red: str,
        green: str,
        yellow: str,
        blue: str,
        magenta: str,
        cyan: str,
        white: str,
        additional: list[str] | None = None,
    ) -> Self:
        if additional is None:
            additional = []
        return cls(
            name,
            cls._color2rgb(black),
            cls._color2rgb(red),
            cls._color2rgb(green),
            cls._color2rgb(yellow),
            cls._color2rgb(blue),
            cls._color2rgb(magenta),
            cls._color2rgb(cyan),
            cls._color2rgb(white),
            [cls._color2rgb(color) for color in additional],
        )

    @staticmethod
    def _color2rgb(color: str) -> list[int]:
        if color == "":
            return []
        match = re.match(r"#(?:[0-9a-fA-F]{3}){2}", color)
        if match is None:
            raise ValueError("Incorrect hex, should be #123456")
        result = list(int(match.group(0).lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        return result

    @staticmethod
    def _color2hex(color: list[int]) -> str:
        if len(color) != 3:
            return ""
        for channel in color:
            if not isinstance(channel, int) or not (0 <= channel < 256):
                raise ValueError
        return "#%02x%02x%02x" % tuple(color)

    def write(self, path: str) -> None:
        self_dict = asdict(self)
        res_dict = copy(self_dict)
        for key, value in self_dict.items():
            if key not in ["name", "additional"]:
                res_dict[key] = self._color2hex(value)
            if key == "additional":
                res_dict[key] = [self._color2hex(color) for color in value]

        with open(path, "w") as ds:
            json.dump(res_dict, ds, indent=4)

    @classmethod
    def read(cls, pal_path: str) -> "Palette":
        try:
            with open(pal_path, "r") as ds:
                data = json.load(ds)
        except FileNotFoundError:
            cls.handle_missing_palette()
            with open(pal_path, "r") as ds:
                data = json.load(ds)

        data = [data[key] for key in data.keys()]
        return Palette.factory(*data)

    @staticmethod
    def handle_missing_palette():
        shutil.copytree(
            path.abspath(path.join(path.dirname(__file__), "..", "..", "palettes")),
            path.join(user_config_dir("gistqd"), "palettes"),
        )
