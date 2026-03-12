from typing import Tuple, Dict, List, Any
from math import inf


class Hub():
    def __init__(self, name: str, pos: Tuple[int, int],
                 complementary_setting: Dict[Any, Any],
                 s_e_name: str = ""):
        """ Init Hub parameters """
        self.__c_setting: Dict[Any, Any] = {}
        self.__neighbors: List["Hub"] = []
        self.__nb_drone: int = 0
        self.__max_drone: int = 1
        self.__weight: int = 1
        self.__is_visible = True
        self.__is_blocked = False

        self.name = name
        self.pos = pos
        self.c_setting = complementary_setting

        if self.c_setting.get("max_drones"):
            self.max_drone = int(self.c_setting["max_drones"])
        else:
            if self.name == s_e_name:
                self.max_drone = inf

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

    @property
    def nb_drone(self) -> int:
        """ Return nb drone in hub """
        return self.__nb_drone

    @nb_drone.setter
    def nb_drone(self, nb_drone) -> None:
        """ Set nb dorne in hub """
        self.__nb_drone = nb_drone

    @property
    def weight(self) -> int:
        """ Return weight of hub """
        return self.__weight

    @weight.setter
    def weight(self, weight: int) -> None:
        """ Set weight """
        self.__weight = weight

    @property
    def is_visible(self) -> bool:
        """ Return if the hub is visble """
        return self.__is_visible

    @is_visible.setter
    def is_visible(self, is_visible: bool) -> None:
        """ Set hub visibility """
        self.__is_visible = is_visible

    @property
    def is_blocked(self) -> bool:
        """ Return if the hub is blocked """
        return self.__is_blocked

    @is_blocked.setter
    def is_blocked(self, is_blocked: bool) -> None:
        """ Set hub blocked """
        self.__is_blocked = is_blocked

    @property
    def max_drone(self) -> bool:
        """ Return max drone capacity """
        return self.__max_drone

    @max_drone.setter
    def max_drone(self, max_drone: bool) -> None:
        """ Set max_drone capacity """
        self.__max_drone = max_drone
