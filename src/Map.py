from typing import List, Self, Dict
from src.Hub import Hub
from src.Connection import Connection
from src.Drone import Drone
from src.config import W_SIZE, OFFSET_EDGE
import re


class Map():
    def __init__(self):
        self.__nb_drone = 0
        self.__start = None
        self.__end = None
        self.__hub_lst = []
        self.__connection_lst = []
        self.__drone_lst = []
        self.__project_pos = dict()
        self.__movements = []

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

    def append_connection(self, name: str, c_data: Dict) -> None:
        """ Append connection """
        enter, exit = name.split('-', 1)
        hub_lst = self.hub_lst.copy() + [self.start, self.end]
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

    @property
    def project_pos(self) -> Dict:
        """ Return project hub coordinates """
        return self.__project_pos

    @project_pos.setter
    def project_pos(self, p_pos: Dict) -> None:
        """ Set projet pos list """
        self.__project_pos = p_pos

    @property
    def movements(self) -> List[List[str]]:
        """ Return list of different movement to drone """
        return self.__movements

    @movements.setter
    def movements(self, movements: List[List[str]]) -> None:
        """ Set movements list """
        self.__movements = movements

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

    def get_project_hub_coordinate(self) -> None:
        """ Return one list of project coordinate to display on surface """
        hub_lst = [self.start] + self.hub_lst.copy() + [self.end]
        x_min = min(hub.pos[0] for hub in hub_lst)
        x_max = max(hub.pos[0] for hub in hub_lst)
        y_min = min(hub.pos[1] for hub in hub_lst)
        y_max = max(hub.pos[1] for hub in hub_lst)
        width, height = W_SIZE

        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        hubs_width = max(1, x_max - x_min)
        hubs_height = max(1, y_max - y_min)
        # distance of hub in surface (add offset_edge to not touch edge)
        scale = OFFSET_EDGE * min(width / hubs_width, height / hubs_height)

        # create project pos
        self.project_pos = {}
        for hub in hub_lst:
            x, y = hub.pos

            x -= x_center
            y -= y_center
            x_p = width/2 + x * scale
            y_p = height/2 - y * scale
            self.project_pos.update({hub.name: (x_p, y_p)})

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
                if "start" in name:
                    n_map.start = Hub(name, (x, y), c_setting)
                elif "goal" in name:
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
        n_map.set_neighbor()
        n_map.gen_drone()
        n_map.get_project_hub_coordinate()
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

    def give_adjacent_lst(self, hub_lst: List[Hub]) -> Dict:
        """ Retrun list of neibor and this weight """
        adj = dict()
        for hub in hub_lst:
            if hub.is_visible or hub == hub_lst[0]:
                neighbors = [n for n in hub.neighbors if n in hub_lst]
                adj.update({hub.name: neighbors})
        return adj

    def gen_drone(self) -> None:
        """ gen drone list """
        for i in range(self.nb_drone):
            name = f"D{i + 1}"
            self.drone_lst.append(Drone(name, self.start))

    def search_connection(self, h_n1, h_n2) -> Connection:
        """ Search connection between to hub name """
        for con in self.connection_lst:
            h1, h2 = con.hubs
            if (h1.name == h_n1 and h2.name == h_n2 or
               h1.name == h_n2 and h2.name == h_n1):
                return con
        raise ValueError("Error connection does not exist: "
                         f"{h_n1}-{h_n2}")
    
    def get_drone(self, drone_name: str) -> Drone | None:
        """ Return drone with same name """
        for drone in self.drone_lst:
            if drone.name == drone_name:
                return drone
        return None

    def update_wheight(self) -> None:
        hub_lst = self.hub_lst
        for hub in hub_lst:
            if hub.c_setting.get("zone"):
                if hub.c_setting['zone'] == 'blocked':
                    hub.is_visible = False
                    continue
                if hub.c_setting['zone'] == 'restricted':
                    hub.weight = 4
                elif hub.c_setting['zone'] == 'priority':
                    hub.weight = 1
                else:
                    hub.weight = 2

            if hub.nb_drone >= hub.max_drone:

                hub.is_blocked = True
            else:
                hub.is_blocked = False

    def set_target(self, drone: Drone, target: Hub) -> None:
        """ Set target to the drone """

        if drone.nb_step < drone.len_path and drone.nb_step > 0:
            return

        drone.n_hub = target

        con = self.search_connection(drone.c_hub.name, drone.n_hub.name)

        if target.c_setting.get("zone") == "restricted":
            drone.len_path = 2
        else:
            drone.len_path = 1

        if (target.nb_drone >= target.max_drone or
                con.capacity >= con.m_capacity):
            drone.stay = True
            drone.n_hub.weight += 2
        else:
            con.capacity += 1
            drone.n_hub.nb_drone += 1
            drone.c_hub.nb_drone -= 1
            drone.stay = False

    def move_drone(self, drone: Drone) -> str:
        """ Move the drone to the next destionation """
        if drone.stay:
            return f"{drone.name}-stay"
        drone.nb_step += 1
        if drone.nb_step >= drone.len_path:
            # print(f"{drone.name}-{drone.n_hub.name}", end=' ')
            # print()
            con = self.search_connection(drone.c_hub.name, drone.n_hub.name)
            con.capacity = 0
            drone.c_hub = drone.n_hub
            drone.nb_step = 0

            # n_h_name = drone.n_hub.name
            # drone.end_pos = self.project_pos[n_h_name][:]
            return f"{drone.name}-{drone.n_hub.name}"
        else:
            # print(f"{drone.name}-{drone.c_hub.name}-"
            #       f"{drone.n_hub.name}", end=' ')
            # print()
            return (f"{drone.name}-{drone.c_hub.name}-"
                    f"{drone.n_hub.name}")
            # x1, y1 = self.project_pos[drone.c_hub.name]
            # x2, y2 = self.project_pos[drone.n_hub.name]
            # drone.end_pos = ((x1 + x2) / 2, (y1 + y2) / 2)

    def play_map(self) -> List[List[str]]:
        from src.Pathfinder import Pathinder
        pf = Pathinder(self)
        self.movements = []
        self.update_wheight()
        while self.end.nb_drone < self.nb_drone:
            movements_turn = []
            for drone in self.drone_lst:
                drone.path = pf.get_path_for_drone(drone)
                if drone.path:
                    self.set_target(drone, drone.path.pop(0))
                    movements_turn.append(self.move_drone(drone))
                else:
                    movements_turn.append(f"{drone.name}-stay")
            self.movements.append(movements_turn)
        return self.movements

    def print_path(self):
        if not self.movements:
            self.play_map()
            if not self.movements:
                raise ValueError("Error: No movement find")

        for i, elem in enumerate(self.movements, 1):
            print(f"Turn: {i}")
            print(" ".join(elem))

        print()
        print(f"Total Turn: {len(self.movements)}")
