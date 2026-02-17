from .parser import get_data, check_data
from .Map import Map
import sys


def main():
    # path = "maps/easy/01_linear_path.txt"
    # path = "maps/hard/01_maze_nightmare.txt"
    path = "data/maps/hard/02_capacity_hell.txt"
    try:
        map_data = get_data(path)
        check_data(map_data)
        map = Map.map_init(map_data)
    except FileNotFoundError as e:
        print("Invalid map file format")
        print(e)
        sys.exit()

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


if __name__ == "__main__":
    main()
