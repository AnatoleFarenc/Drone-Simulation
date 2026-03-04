from src.Map import Map
from src.Hub import Hub
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

    def dijkstra(self):
        adj = self.map.give_adjacent_lst(self.__next_hubs)
        pq = []

        dist = {hub.name: inf for hub in self.__next_hubs
                if hub.is_visible}

        dist[self.__start.name] = 0

        heapq.heappush(pq, (0, self.__start.name))

        prev = {}

        while pq:
            d, u = heapq.heappop(pq)

            if d > dist[u]:
                continue
            for hub in adj[u]:
                if hub.is_visible:
                    if dist[u] + hub.weight < dist[hub.name]:
                        dist[hub.name] = dist[u] + hub.weight
                        prev[hub.name] = self.map.get_hub(u)
                        heapq.heappush(pq, ((dist[hub.name]), hub.name))
        return prev

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








    def get_path(self, c_hub: Hub):
        self.__start = c_hub
        self.__next_hubs = []
        if c_hub.name == self.map.start.name:
            self.__next_hubs.append(c_hub)
            self.__next_hubs += self.map.hub_lst
        else:
            for hub in self.map.hub_lst:
                if hub.name == c_hub.name:
                    hub_i = self.map.hub_lst.index(hub)
                    self.__next_hubs = self.map.hub_lst[hub_i:]
                    break
        self.__next_hubs.append(self.map.end)
        prev = self.dijkstra()

        path = []
        current = self.map.end
        while current.name != self.__start.name:
            path.append(current)
            if prev.get(current.name):
                current = prev[current.name]
            else:
                return None
        # path.append(self.map.start)
        path.reverse()
        return path
