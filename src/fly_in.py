from src.parser import get_data, check_data
from src.Map import Map
from src.Renderer import Renderer
from src.Pathfinder import Pathinder
import sys
from src.config import W_SIZE
from src.Menu import Menu


def main():

    # path = "data/maps/easy/01_linear_path.txt"
    # path = "data/maps/easy/02_simple_fork.txt"
    # path = "data/maps/easy/03_basic_capacity.txt"
    # path = "data/maps/medium/01_dead_end_trap.txt"
    # path = "data/maps/medium/02_circular_loop.txt"
    # path = "data/maps/medium/03_priority_puzzle.txt"
    # path = "data/maps/hard/01_maze_nightmare.txt"
    # path = "data/maps/hard/02_capacity_hell.txt"
    path = "data/maps/hard/03_ultimate_challenge.txt"
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

    # map.print_path()
    # animate(map)

    Menu.menu_init(map, path)
    Menu().run()

if __name__ == "__main__":
    main()
