from .Map import Map
from .Pathfinder import Pathinder


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


def play_simulation(map: Map) -> None:
    pf = Pathinder(map)
    nb_turn = 0
    while map.end.nb_drone < map.nb_drone:
        nb_turn += 1
        print(f"Turn: {nb_turn}")
        for drone in map.drone_lst:
            map.update_wheight()
            drone.path = pf.get_path(drone.c_hub)
            if drone.path:
                map.set_target_drone(drone, drone.path.pop(0))
                if not drone.stay:
                    print(f"{drone.name} go to {drone.n_hub.name}")
                else:
                    print(f"{drone.name} stay put")
            else:
                print("No path find: ", end='')
                print(f"{drone.name} stay put")
        print()

    print()
    print(f"{map.end.nb_drone}/{map.nb_drone} drone in {map.end.name}")
    print(f"turn: {nb_turn}")
