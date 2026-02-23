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

    # path = "data/maps/easy/01_linear_path.txt"
    # path = "data/maps/medium/01_dead_end_trap.txt"
    # path = "data/maps/hard/01_maze_nightmare.txt"
    path = "data/maps/hard/02_capacity_hell.txt"
    # path = "data/maps/hard/03_ultimate_challenge.txt"
    try:
        map_data = get_data(path)
        check_data(map_data)
        map = Map.map_init(map_data)
    except Exception as e:
        print("Invalid map file format")
        print(e)
        sys.exit()

    map.set_neighbor()

    end = False
    nb_turn = 0
    find_path = Pathinder(map)
    map.gen_drone()
    while not end:
        nb_turn += 1
        for drone in map.drone_lst:
            map.update_wheight()
            drone.path = find_path.get_path(drone.c_hub)
            if drone.path:
                map.set_target_drone(drone, drone.path.pop(0))
                if not drone.stay:
                    print(f"{drone.name} go to {drone.n_hub.name}")
                else:
                    print(f"{drone.name} stay put")
            else:
                print(f"{drone.name} stay put")
        print()
        if map.end.nb_drone == map.nb_drone:
            end = True
    print()
    print(f"{map.end.nb_drone}/{map.nb_drone} drone in {map.end.name}")
    print(f"turn: {nb_turn}")


if __name__ == "__main__":
    main()
