from Map import Map
from typing import Dict


def get_data(map_path: str) -> Dict:
    """ Get data on map file """
    map_data = {}
    index_hub = 1
    index_connection = 0
    with open(map_path, 'r') as file:
        for i, line in enumerate(file, start=1):
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split(":", 1)
                if line.startswith("hub"):
                    key += str(index_hub)
                    index_hub += 1
                if "connection" in line:
                    key += str(index_connection)
                    index_connection += 1
                map_data.update({key: value})
        return map_data


def check_data(map_data: Dict) -> None:
    """ Check id dic contain a good data """
    first_line = list(map_data)[0]

    # check number of drone
    if first_line != "nb_drones":
        raise ValueError("Error: Invalid first line: nb_drones")
    try:
        map_data['nb_drones'] = int(map_data["nb_drones"])
        if map_data['nb_drones'] < 0:
            raise TypeError
    except TypeError:
        print("Error: nb_drones mus be positve int")

    # check end and start hub



# def main():
#     path = "maps/hard/"
#     map_data = get_data(path+"01_maze_nightmare.txt")
#     mape = Map.map_init(map_data)

#     print()
#     print("### Map Data ###")
#     print(f"Drones: {mape.nb_drone}")
#     print()

#     print("## Hub")
#     print(f"{mape.start.name}: {mape.start.pos}")
#     print()
#     for hub in mape.hub_lst:
#         print(f"{hub.name}: {hub.pos}")
#     print()
#     print(f"{mape.end.name}: {mape.end.pos}")

#     print()

#     print("## Connection")
#     for i, connection in enumerate(mape.connection_lst):
#         print(f"connection {i}: {connection}")
#     print()

#     print("### Collor ###")
#     print(f"{mape.start.name}: {mape.start.c_setting['color']}")
#     for hub in mape.hub_lst:
#         print(f"{hub.name}: {hub.c_setting['color']}")
#     print(f"{mape.end.name}: {mape.end.c_setting['color']}")




# if __name__ == "__main__":
#     main()
