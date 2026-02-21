from typing import List, Self, LiteralString, Dict
from .Hub import Hub
from .Connection import Connection
from .Drone import Drone
import re


class Map():
    def __init__(self):
        self.__nb_drone = 0
        self.__start = None
        self.__end = None
        self.__hub_lst = []
        self.__connection_lst = []
        self.__drone_lst = []

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

    def get_hub(self, hub_name: str) -> Hub | None:
        """ Return hub in hub list wiht are name """
        if hub_name == self.start.name:
            return self.start
        if hub_name == self.end.name:
            return self.end
        for hub in self.hub_lst:
            if hub.name == hub_name:
                return hub
        return None

    @property
    def connection_lst(self) -> List[Connection]:
        """ Return connection list """
        return self.__connection_lst

    def append_connection(self, name: LiteralString, c_data: Dict) -> None:
        """ Append connection """
        enter, exit = name.split('-', 1)
        hub_lst = self.hub_lst.copy()
        hub_lst.append(self.start)
        hub_lst.append(self.end)
        hub_0 = [hub for hub in hub_lst if hub.name == enter]
        hub_1 = [hub for hub in hub_lst if hub.name == exit]
        if hub_0 and hub_1:
            new_con = Connection((hub_0[0], hub_1[0]), c_data)
            self.connection_lst.append(new_con)
        else:
            raise ValueError("Error: invalid connection")

    @property
    def drone_lst(self) -> List[Drone]:
        """ Return Drone list """
        return self.__drone_lst

    @staticmethod
    def parse_complementary_data(data: str) -> Dict:
        """ Parse they complementary data and return dict with same """
        """ parameters """
        if not data:
            return {}
        data = re.sub(r"[\[\]]", '', data)
        data_dict = dict()
        data_p = data.split(' ')
        for elem in data_p:
            key, value = elem.split('=')
            data_dict.update({key: value})
        return data_dict

    @classmethod
    def map_init(cls, data: dict) -> Self:
        """ Init data of map and create instance """
        n_map = cls()
        for key, value in data.items():
            if key == "nb_drones":
                try:
                    n_map.nb_drone = int(value)
                except (ValueError, TypeError):
                    raise ValueError("Error: invalid numbers to nb_drones: "
                                     f"'{value.strip()}'")
                continue
            elif "hub" in key:
                hub_data = value.split(" ", 3)
                if len(hub_data) > 3:
                    name, x, y, c_data = hub_data
                else:
                    name, x, y = hub_data
                    c_data = None
                try:
                    x = int(x)
                    y = int(y)
                except (ValueError, TypeError):
                    raise ValueError(f"Error: Inalid coordinate:\n"
                                     f"{name} ({x}, {y})")
                c_setting = n_map.parse_complementary_data(c_data)
                if name == "start":
                    n_map.start = Hub(name, (x, y), c_setting)
                elif name == "goal":
                    n_map.end = Hub(name, (x, y), c_setting)
                else:
                    n_map.append_hub(Hub(name, (x, y), c_setting))
                continue
            elif "connection" in key:
                data = value.split(' ')
                if len(data) == 1:
                    n_map.append_connection(data[0], {})
                elif len(data) > 1:
                    c_data = n_map.parse_complementary_data(data[1])
                    n_map.append_connection(data[0], c_data)
                else:
                    raise ValueError("Missing data connection")
                continue
        n_map.start.nb_drone = n_map.nb_drone
        return n_map

    def set_neighbor(self) -> None:
        """ Add hub neighbor to same hub in list """
        hub_lst = self.hub_lst.copy()
        hub_lst.append(self.start)
        hub_lst.append(self.end)
        for hub in hub_lst:
            for con in self.connection_lst:
                hub_1, hub_2 = con.hubs
                if hub.name == hub_1.name:
                    hub.append_neighbor(hub_2)
                elif hub.name == hub_2.name:
                    hub.append_neighbor(hub_1)

    def give_adjacent_lst(self) -> Dict:
        """ Retrun list of neibor and this weight """
        adj = dict()
        adj.update({self.start.name: self.start.neighbors})
        for hub in self.hub_lst:
            adj.update({hub.name: hub.neighbors})
        adj.update({self.end.name: self.end.neighbors})
        return adj

    def gen_drone(self) -> None:
        """ gen drone list """
        for i in range(self.nb_drone):
            name = f"drone{i}"
            self.drone_lst.append(Drone(name, self.start))

    def set_target_drone(self, drone: Drone, target: Hub) -> None:
        """ Set drone to the next hub [target] """
        if drone.c_hub not in target.neighbors:
            print([n.name for n in target.neighbors])
            raise ValueError("Error: target isn't attainable")

        if target.c_setting.get('zone'):
            if target.c_setting['zone'] == 'restricted':
                drone.len_path = 2
        else:
            drone.len_path = 1

        drone.n_hub = target
        drone.nb_move = 0

    def move_drone(self) -> None:
        """ Move drones """
        for drone in self.drone_lst:
            drone.nb_move += 1
            if drone.nb_move >= drone.len_path:
                drone.c_hub.nb_drone -= 1
                drone.n_hub.nb_drone += 1
                drone.c_hub = drone.n_hub
