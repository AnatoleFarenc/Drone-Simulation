from typing import List, Self, LiteralString
from Hub import Hub
import re


class Map():
    def __init__(self):
        self.__nb_drone = 0
        self.__start = None
        self.__end = None
        self.__hub_lst: List[Hub] = []
        self.__connection_lst: List[Hub] = []

    @property
    def nb_drone(self) -> int:
        """ Return nb_drone """
        return self.__nb_drone

    @nb_drone.setter
    def nb_drone(self, nb_drone: int) -> None:
        """ Set number of drone """
        if nb_drone >= 0:
            self.__nb_drone = nb_drone
        else:
            raise ValueError("Error: nb_drone invalid")

    @property
    def start(self) -> Hub:
        """ Return start hub """
        return self.__start

    @start.setter
    def start(self, start_hub: Hub) -> None:
        """ Set start hub """
        self.__start = start_hub

    @property
    def end(self) -> Hub:
        """ Return end hub """
        return self.__end

    @end.setter
    def end(self, end_hub: Hub) -> None:
        """ Set end hub """
        self.__end = end_hub

    @property
    def hub_lst(self) -> List[Hub]:
        """ Return coordinates list of same hub between sart and end """
        return self.__hub_lst

    def append_hub(self, hub: Hub) -> None:
        """ Append hub """
        self.__hub_lst.append(hub)

    @property
    def connection_lst(self) -> List[Hub]:
        """ Return connection list """
        return self.__connection_lst

    def append_connection(self, name: LiteralString) -> None:
        """ Append connection """
        for hub in self.hub_lst:
            if hub.name in name:
                self.__connection_lst.append(hub)
                return
        raise ValueError("Error Hub dosn't exist")

    @classmethod
    def map_init(cls, data: dict) -> Self:
        """ Init data of map and create instance """
        n_map = cls()
        for key, value in data.items():
            if key == "nb_drones":
                n_map.nb_drone = int(value)
                continue
            elif "hub" in key:
                _, name, x, y, color = value.split(" ", 4)
                x = int(x)
                y = int(y)
                color = re.findall("=([^]]+)]", color)[0]
                if name == "start":
                    n_map.start = Hub(name, (x, y), color)
                elif name == "goal":
                    n_map.end = Hub(name, (x, y), color)
                else:
                    n_map.append_hub(Hub(name, (x, y), color))
                continue
            elif "connection" in key:
                n_map.append_connection(value)
                continue
        return n_map
