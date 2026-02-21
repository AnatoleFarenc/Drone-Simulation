from .Map import Map
from math import inf
import heapq


class Pathinder():
    """ Find the smallest paht from start to the goal"""
    def __init__(self, map: Map):
        self.map = map

    @property
    def map(self) -> Map: 
        """ Return map """
        return self.__map

    @map.setter
    def map(self, map: Map) -> None:
        """ Set map """
        self.__map = map

    def dijkstra(self):
        adj = self.map.give_adjacent_lst()
        pq = []

        dist = {hub.name: inf for hub in self.map.hub_lst +
                [self.map.start, self.map.end]}
        dist[self.map.start] = 0

        dist[self.map.start.name] = 0
        heapq.heappush(pq, (0, self.map.start.name))

        prev = {}

        while pq:
            d, u = heapq.heappop(pq)

            if d > dist[u]:
                continue
            for hub in adj[u]:
                if dist[u] + hub.weight < dist[hub.name]:
                    dist[hub.name] = dist[u] + hub.weight
                    prev[hub.name] = self.map.get_hub(u)
                    heapq.heappush(pq, ((dist[hub.name]), hub.name))
        return prev

    def get_path(self):
        prev = self.dijkstra()

        path = []
        current = self.map.end
        while current.name != self.map.start.name:
            path.append(current)
            current = prev[current.name]
        path.append(self.map.start)
        path.reverse()
        return path
