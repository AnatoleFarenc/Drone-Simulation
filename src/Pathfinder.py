from src.Map import Map
from src.Hub import Hub
from src.Drone import Drone
from math import inf, hypot
from typing import List
import heapq


class Pathinder():
    """ Find the smallest paht from start to the goal"""
    def __init__(self, map: Map):
        """ Init pathfinder with map references """
        self.map = map
        self.__start = map.start
        self.__end = map.end
        self.__next_hubs: List[Hub] = []

    @property
    def map(self) -> Map:
        """ Return map """
        return self.__map

    @map.setter
    def map(self, map: Map) -> None:
        """ Set map """
        self.__map = map

    def __heuristic(self, hub: Hub) -> float:
        """ Return heuristic distance to end hub """
        x1, y1 = hub.pos
        x2, y2 = self.__end.pos
        return hypot(x2-x1, y2-y1)

    def __edge_weight(self, c_hub: Hub, n_hub: Hub) -> int:
        """ Compute weight for a map edge """

        con = self.map.search_connection(c_hub.name, n_hub.name)

        zone = n_hub.c_setting.get("zone")
        if zone == "restricted":
            weight = 4
        elif zone == "priority":
            weight = 1
        else:
            weight = 3

        if n_hub.nb_drone >= n_hub.max_drone:
            weight += 1
        if con and con.capacity >= con.m_capacity:
            weight += 2

        return weight

    def get_path_for_drone(self, drone: Drone) -> List[Hub] | None:
        """ Return best path for one drone """
        self.__start = drone.c_hub
        self.__next_hubs = [self.map.start] + self.map.hub_lst + [self.map.end]

        dist = {hub.name: inf for hub in self.__next_hubs if hub.is_visible}
        dist[self.__start.name] = 0
        prev_h: dict[str, Hub] = {}

        pq = [(self.__heuristic(self.__start), 0, self.__start.name)]
        neighbors = self.map.give_adjacent_lst(self.__next_hubs)

        while pq:
            f, g, c_h = heapq.heappop(pq)

            if c_h == self.__end.name:
                break

            for n_h in neighbors[c_h]:
                if not n_h.is_visible or n_h.max_drone <= 0:
                    continue

                current_hub = self.map.get_hub(c_h)
                if current_hub is None:
                    continue
                weight = self.__edge_weight(current_hub, n_h)
                ng = g + weight
                if ng < dist[n_h.name]:
                    dist[n_h.name] = ng
                    prev_h[n_h.name] = current_hub
                    nh_f = ng + self.__heuristic(n_h)
                    heapq.heappush(pq, (nh_f, ng, n_h.name))

        path: List[Hub] = []
        current = self.__end
        while current.name != self.__start.name:
            path.append(current)
            previous_hub = prev_h.get(current.name)
            if previous_hub is None:
                return None
            current = previous_hub
        path.reverse()
        return path
