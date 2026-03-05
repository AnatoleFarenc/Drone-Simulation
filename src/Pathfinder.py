from src.Map import Map
from src.Drone import Drone
from math import inf
import heapq


class Pathinder():
    """ Find the smallest paht from start to the goal"""
    def __init__(self, map: Map):
        self.map = map
        self.__start = map.start
        self.__end = map.end
        self.__next_hubs = []

    @property
    def map(self) -> Map: 
        """ Return map """
        return self.__map

    @map.setter
    def map(self, map: Map) -> None:
        """ Set map """
        self.__map = map

    def get_path_for_drone(self, drone: Drone):
        self.__start = drone.c_hub

        if drone.c_hub.name == self.map.start.name:
            self.__next_hubs.append(drone.c_hub)
            self.__next_hubs += self.map.hub_lst
        else:
            for hub in self.map.hub_lst:
                if hub.name == drone.c_hub.name:
                    hub_i = self.map.hub_lst.index(hub)
                    self.__next_hubs = self.map.hub_lst[hub_i:]
                    break
        self.__next_hubs.append(self.map.end)

        pq = []
        neighbors = self.map.give_adjacent_lst(self.__next_hubs)
        dist = {hub.name: inf for hub in self.__next_hubs if hub.is_visible}
        dist[self.__start.name] = 0

        prev_h = {}
        heapq.heappush(pq, (0, self.__start.name))

        while pq:
            c_d, c_h = heapq.heappop(pq)

            if c_h == self.__end:
                break

            for n_h in neighbors[c_h]:
                if not n_h.is_visible:
                    continue

                weight = n_h.weight
                # if n_h.nb_drone >= n_h.max_drone:
                #     weight += inf
                if n_h.c_setting.get("zone"):
                    if n_h.c_setting["zone"] == "restricted":
                        weight += 10
                    if n_h.c_setting["zone"] == "priority":
                        weight = max(1, weight - 1)

                n_d = c_d + weight
                if n_d < dist[n_h.name]:
                    dist[n_h.name] = n_d
                    prev_h[n_h.name] = self.map.get_hub(c_h)
                    heapq.heappush(pq, (dist[n_h.name], n_h.name))

        path = []
        current = self.__end
        while current.name != self.__start.name:
            path.append(current)
            if prev_h.get(current.name):
                current = prev_h[current.name]
            else:
                return None
        path.reverse()
        return path
