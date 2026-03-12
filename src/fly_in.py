from src.parser import get_data, check_data
from src.Map import Map
import sys
from pathlib import Path
from src.config import ROOT_NAME
from src.Menu import Menu


def main():

    try:
        map_root = Path(ROOT_NAME)

        path_dict = {
            dirm.name: [maps.name for maps in dirm.iterdir() if maps.is_file()]
            for dirm in map_root.iterdir()
            if dirm.is_dir()
        }

        keys = [key for key, _ in path_dict.items()]
        if not keys:
            raise FileNotFoundError
        dir_name = ["challenger", "hard", "medium", "easy"]
        for name in dir_name:
            if name in keys:
                keys.remove(name)
                keys.insert(0, name)
        for dir, _ in path_dict.items():
            path_dict[dir].sort()

    except FileNotFoundError:
        print("Error: Wrong map directory")
        sys.exit(1)

    path = ROOT_NAME + keys[0] + '/' + path_dict[keys[0]][0]

    # path = "data/maps/easy/01_linear_path.txt"
    # path = "data/maps/easy/02_simple_fork.txt"
    # path = "data/maps/easy/03_basic_capacity.txt"
    # path = "data/maps/medium/01_dead_end_trap.txt"
    # path = "data/maps/medium/02_circular_loop.txt"
    # path = "data/maps/medium/03_priority_puzzle.txt"
    # path = "data/maps/hard/01_maze_nightmare.txt"
    # path = "data/maps/hard/02_capacity_hell.txt"
    # path = "data/maps/hard/03_ultimate_challenge.txt"
    # path = "data/maps/test.txt"
    # path = "data/maps/challenger/01_the_impossible_dream.txt"

    try:
        map_data = get_data(path)
        check_data(map_data)
        map = Map.map_init(map_data)
    except Exception as e:
        print("Invalid map file format")
        print(e)
        sys.exit()

    # print(map.print_path())
    # from .visualizer import animate
    # print(animate(map, 0.3))

    Menu.menu_init(map, path, path_dict)
    Menu().run()


if __name__ == "__main__":
    main()
