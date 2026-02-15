from typing import LiteralString, Tuple


class Hub():
    def __init__(self, name: LiteralString, pos: Tuple[int, int],
                 color: LiteralString):
        self.__name = None
        self.__pos = None
        self.__color = None
        self.name = name
        self.pos = pos
        self.color = color

    @property
    def name(self) -> LiteralString:
        """Return hub name"""
        return self.__name

    @name.setter
    def name(self, value: LiteralString) -> None:
        """Set hub name (non-empty string)"""
        if isinstance(value, str) and value:
            self.__name = value
        else:
            raise ValueError("Error: name must be a non-empty string")

    @property
    def pos(self) -> Tuple[int, int]:
        """Return hub coordinates as (x, y)"""
        return self.__pos

    @pos.setter
    def pos(self, coordinates: Tuple[int, int]) -> None:
        """Set hub coordinates; requires two non-negative integers"""
        if not isinstance(coordinates, tuple):
            raise TypeError("Error: pos must be a tuple of two integers")
        x, y = coordinates
        if isinstance(x, int) and isinstance(y, int) and x >= 0 and y >= 0:
            self.__pos = coordinates
        else:
            raise ValueError("Error: coordinates is negative integers")

    @property
    def color(self) -> LiteralString:
        """Return hub color"""
        return self.__color

    @color.setter
    def color(self, value: LiteralString) -> None:
        """Set hub color (non-empty string)"""
        if isinstance(value, str) and value:
            self.__color = value
        else:
            raise ValueError("Error: color must be a non-empty string")
