from dataclasses import dataclass, field, asdict
import json
import re
from typing import overload


@dataclass()
class Palette:
    name: str
    black: list[int] | str = field(default_factory=list)
    red: list[int] | str = field(default_factory=list)
    green: list[int] | str = field(default_factory=list)
    yellow: list[int] | str = field(default_factory=list)
    blue: list[int] | str = field(default_factory=list)
    magenta: list[int] | str = field(default_factory=list)
    cyan: list[int] | str = field(default_factory=list)
    white: list[int] | str = field(default_factory=list)
    additional: list[list[int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.black = self._color2rgb(self.black)
        self.red = self._color2rgb(self.red)
        self.green = self._color2rgb(self.green)
        self.yellow = self._color2rgb(self.yellow)
        self.blue = self._color2rgb(self.blue)
        self.magenta = self._color2rgb(self.magenta)
        self.cyan = self._color2rgb(self.cyan)
        self.white = self._color2rgb(self.white)
        self.additional = [self._color2rgb(color) for color in self.additional]

    @overload
    @staticmethod
    def _color2rgb(color: str) -> list[int]: ...

    @overload
    @staticmethod
    def _color2rgb(color: list[int]) -> list[int]: ...

    @staticmethod
    def _color2rgb(color: str | list[int]) -> list[int]:
        if isinstance(color, list):
            if len(color) not in [0, 3]:
                raise ValueError("Number of channels should be 3")
            for channel in color:
                if not isinstance(channel, int) or not (0 <= channel < 256):
                    raise ValueError(
                        "channel value should be a number in range [0, 255]"
                    )
            return color
        if color == "":
            return []
        match = re.match(r"#(?:[0-9a-fA-F]{3}){2}", color)
        if match is None:
            raise ValueError("Incorrect hex, should be #123456")
        color = list(int(match.group(0).lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        return color

    @staticmethod
    def _color2hex(color: list[int]) -> str:
        if len(color) != 3:
            return ""
        return "#%02x%02x%02x" % tuple(color)

    def write(self, path: str) -> None:
        self_dict = asdict(self)
        for key, value in self_dict.items():
            if key not in ["name", "additional"]:
                self_dict[key] = self._color2hex(value)
            if key == "additional":
                self_dict[key] = [self._color2hex(color) for color in value]

        with open(path, "w") as ds:
            json.dump(self_dict, ds, indent=4)

    @staticmethod
    def read(path: str) -> "Palette":
        with open(path, "r") as ds:
            data = json.load(ds)
        return Palette(**data)


@dataclass()
class ImageData:
    height: int
    width: int
    colors: tuple[tuple[int, ...], ...]
