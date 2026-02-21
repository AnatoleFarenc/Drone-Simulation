from .parser import get_data, check_data
from .Map import Map
from .Pathfinder import Pathinder
from typing import Any
import sys


def debug_info_map(map: Map) -> None:
    """ Display map info """
    print("### Map Data ###\n")
    print("Start:")
    print(f"  - name: {map.start.name}")
    print(f"  - pos: {map.start.pos}")
    print(f"  - color: {map.start.c_setting['color']}")
    for i, hub in enumerate(map.hub_lst, 1):
        print(f"Hub {i}:")
        print(f"  - name: {hub.name}")
        print(f"  - pos: {hub.pos}")
        print(f"  - color: {hub.c_setting['color']}")
    print("End:")
    print(f"  - name: {map.end.name}")
    print(f"  - pos: {map.end.pos}")
    print(f"  - color: {map.end.c_setting['color']}")
    print()

    print("Connection:")
    for connection in map.connection_lst:
        print(f"  - connection: {connection} -> [{connection.c_setting}]")


def debug_lst(lst: Any) -> None:
    print(f"{[elem.name for elem in lst]}")


def main():

    path = "data/maps/easy/01_linear_path.txt"
    # path = "data/maps/hard/01_maze_nightmare.txt"
    # path = "data/maps/hard/02_capacity_hell.txt"
    try:
        map_data = get_data(path)
        check_data(map_data)
        map = Map.map_init(map_data)
    except Exception as e:
        print("Invalid map file format")
        print(e)
        sys.exit()

    map.set_neighbor()

    # map.gen_drone()
    # for drone in map.drone_lst:
    #     map.set_target_drone(drone, map.get_hub('gate1'))

    # print(f"drone in hub: {map.get_hub('start').nb_drone}")
    # debug_lst(map.drone_lst)
    # map.move_drone()
    # for drone in map.drone_lst:
    #     if drone.c_hub.name == "gate1":
    #         print(drone.name)
    # print(f"drone in hub: {map.get_hub('start').nb_drone}")

    path_find = Pathinder(map)
    path = path_find.get_path()
    for i, hub in enumerate(path):
        print(f"{i}: {hub.name}")


if __name__ == "__main__":
    main()
