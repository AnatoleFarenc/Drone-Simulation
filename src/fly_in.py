from src.parser import get_data, check_data
from src.Map import Map
from src.Renderer import Renderer
from src.Pathfinder import Pathinder
from src import pg
# import sys
import math
from src.config import W_SIZE


def main():

    # path = "data/maps/easy/01_linear_path.txt"
    # path = "data/maps/easy/02_simple_fork.txt"
    # path = "data/maps/easy/03_basic_capacity.txt"
    # path = "data/maps/medium/01_dead_end_trap.txt"
    # path = "data/maps/medium/02_circular_loop.txt"
    # path = "data/maps/medium/03_priority_puzzle.txt"
    path = "data/maps/hard/01_maze_nightmare.txt"
    # path = "data/maps/hard/02_capacity_hell.txt"
    # path = "data/maps/hard/03_ultimate_challenge.txt"
    # path = "data/maps/test.txt"
    # path = "data/maps/challenger/01_the_impossible_dream.txt"

    # try:
    map_data = get_data(path)
    check_data(map_data)
    map = Map.map_init(map_data)
    # except Exception as e:
    #     print("Invalid map file format")
    #     print(e)
    #     sys.exit()

    pg.init()

    window = pg.display.set_mode(W_SIZE, pg.SCALED | pg.RESIZABLE)
    pg.display.set_caption("FLY IN")
    clock = pg.time.Clock()

    is_open = True
    renderer = Renderer()

    pf = Pathinder(map)
    nb_turn = 0
    t = 0
    move_duration = 1.0
    move_drone = []

    for drone in map.drone_lst:
        drone.proj_pos[0] = map.project_pos[map.start.name][0]
        drone.proj_pos[1] = map.project_pos[map.start.name][1]

    while is_open:
        dt = clock.tick(60) / 1000
        t += dt
        progress = t / move_duration
        progress = min(progress, 1)
        progress = (1 - math.cos(progress * math.pi)) / 2

        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_open = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    is_open = False

        for drone in move_drone:
            x_1, y_1 = drone.start_pos
            x_2, y_2 = drone.end_pos
            drone.proj_pos[0] = x_1 + (x_2 - x_1) * progress
            drone.proj_pos[1] = y_1 + (y_2 - y_1) * progress

        if progress >= 1 and map.nb_drone != map.end.nb_drone:
            for drone in move_drone:
                drone.proj_pos = list(drone.end_pos[:])
            t = 0
            nb_turn += 1
            print(f"Turn: {nb_turn}")
            move_drone.clear()

            for drone in map.drone_lst:
                map.update_wheight()
                drone.path = pf.get_path_for_drone(drone)
                if drone.path:
                    if map.set_target_drone(drone, drone.path.pop(0)):
                        if not drone.stay:
                            print(f"{drone.name}-{drone.n_hub.name}", end=' ')
                            drone.start_pos = drone.proj_pos[:]
                            n_h_name = drone.n_hub.name
                            drone.end_pos = map.project_pos[n_h_name][:]
                            move_drone.append(drone)
                    else:
                        print(f"{drone.name}-{drone.c_hub.name}-"
                              f"{drone.n_hub.name}", end=' ')
                        # drone.start_pos = drone.proj_pos[:]
                        # n_h_pos = map.project_pos[drone.n_hub.name][:]
                        # mid_con_pos = tuple(coordinate / 2 
                        #                     for coordinate in n_h_pos)
                        # drone.end_pos = mid_con_pos
                        # move_drone.append(drone)

            print('\n')
            map.clean_connection()

            if map.nb_drone == map.end.nb_drone:
                print()
                print(f"Total turn : {nb_turn}")
                print(f"{map.end.nb_drone}/{map.nb_drone} drone "
                      f"in {map.end.name}")
                # is_open = False

        renderer.render(window, map)
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
