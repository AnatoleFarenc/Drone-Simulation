from typing import Tuple, Dict, List, Any


class Hub():
    def __init__(self, name: str, pos: Tuple[int, int],
                 complementary_setting: Dict[Any, Any]):
        """ Init Hub parameters """
        self.__c_setting: Dict[Any, Any] = {}
        self.__neighbors: List["Hub"] = []

        self.name = name
        self.pos = pos
        self.c_setting = complementary_setting

    @property
    def name(self) -> str:
        """Return hub name"""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
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
    def c_setting(self) -> Dict[Any, Any]:
        """ Return max drone on this hub """
        return self.__c_setting

    @c_setting.setter
    def c_setting(self, complementary_setting: Dict[Any, Any]) -> None:
        """ Set max drone in thi hub """
        if isinstance(complementary_setting, dict):
            self.__c_setting = complementary_setting
        else:
            raise ValueError("Error: complementary_setting must be dict")

    def __str__(self) -> str:
        return self.__name

    @property
    def neighbors(self) -> List["Hub"]:
        """ Return neibors list of this hub """
        return self.__neighbors

    def append_neighbor(self, neighbor: "Hub") -> None:
        """ Append hub in neighbors list """
        self.__neighbors.append(neighbor)
