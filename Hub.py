from typing import LiteralString, Tuple, Dict


class Hub():
    def __init__(self, name: LiteralString, pos: Tuple[int, int],
                 complementary_setting: Dict = {}):
        self.__name = None
        self.__pos = None
        self.__color = None
        self.__max_drone = None
        self.name = name
        self.pos = pos
        self.__c_setting = complementary_setting

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
        if isinstance(x, int) and isinstance(y, int):
            self.__pos = coordinates
        else:
            raise ValueError("Error: coordinates must be integers")

    @property
    def c_setting(self) -> int:
        """ Return max drone on this hub """
        return self.__c_setting

    @c_setting.setter
    def c_setting(self, complementary_setting: Dict) -> None:
        """ Set max drone in thi hub """
        if isinstance(complementary_setting, dict):
            self.__c_setting = complementary_setting
        else:
            raise ValueError("Error: complementary_setting must be dict")
