from typing import Dict, List, Tuple
import re
import sys


def get_data(map_path: str) -> Dict:
    """ Get data on map file """
    map_data = {}
    index_hub = 1
    index_connection = 0
    nb_start_h = 0
    nb_end_h = 0
    try:
        with open(map_path, 'r') as file:
            for i, line in enumerate(file, start=1):
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        key, value = line.split(":", 1)
                    except ValueError:
                        raise ValueError("Error: missing key or value\n"
                                         f"line {i}: {line}")

                    if (
                        "hub" in key
                        and key not in {"hub", "start_hub", "end_hub"}
                    ):
                        raise ValueError(f"Error: invalid key for hub\n"
                                         f"line {i}: {line}")

                    if key == "start_hub":
                        nb_start_h += 1
                    if key == "end_hub":
                        nb_end_h += 1
                    if nb_start_h > 1 or nb_end_h > 1:
                        raise ValueError("Error: too much start or end hub")

                    if line.startswith("hub"):
                        key += str(index_hub)
                        index_hub += 1
                    if "connection" in line:
                        key += str(index_connection)
                        index_connection += 1
                    # clean multiple space in setting
                    value = ' '.join(value.split())
                    map_data.update({key: value})
    except FileNotFoundError:
        print(f"Error: Map file not found : {map_path}")
        sys.exit()
    return map_data


def check_meta_data(meta_data: str, valid_setting: List[str]) -> None:
    """ Validate metadata block against allowed keys """
    # check braket
    if meta_data[0] != '[' or meta_data[-1] != ']':
        raise ValueError("Error: meta data must be contain in '[]': "
                         f"{meta_data}")
    # check data
    meta_data = re.sub(r"[\[\]]", '', meta_data)
    data_lst = meta_data.split(' ')
    for data in data_lst:
        try:
            key, value = data.split('=')
        except ValueError:
            raise ValueError(f"Error: wrong format for meta data: {data_lst}")
        if key not in valid_setting:
            raise ValueError(f"Error: wrong setting: {key}:[{meta_data}]")
        if not value.strip():
            raise ValueError(f"Error: missing value: {key} {value}")
        if key == "max_drones" or key == "max_link_capacity":
            if not value.isnumeric():
                raise ValueError(f"Error: for '{key}' the paramer must be "
                                 f"positive interger : '{key}: {value}'")
        if key == "color":
            if not value.isalpha() or not value.islower():
                raise ValueError(f"Error: for '{key}' the paramer must be "
                                 f"an color : '{key}: {value}'")
        if key == "zone":
            valid_zone = ["normal", "blocked", "restricted", "priority"]
            if value not in valid_zone:
                raise ValueError(f"Error: for '{key}' the paramer must be "
                                 f"a valid zone : '{key}: {value}'")


def check_data(map_data: Dict) -> None:
    """ Check id dic contain a good data """
    keys_data = list(map_data)

    # check number of drone
    if keys_data[0] != "nb_drones":
        raise ValueError("Error: Invalid first line: nb_drones")

    # check end and start hub
    if 'start_hub' not in keys_data or 'end_hub' not in keys_data:
        raise ValueError("Error: start_hub or end_hub missing")

    # check hub
    hub_lst = [value for key, value in map_data.items()
               if key.startswith("hub")]
    hub_lst.append(map_data['start_hub'])
    hub_lst.append(map_data['end_hub'])
    name_lst = []
    for hub in hub_lst:
        # check unique name for all hub
        hub_data = hub.split(' ')
        if len(hub_data) < 3:
            raise ValueError(f"Error: missing argument: {hub}")
        name = hub_data[0]
        if not hub_data[1].isnumeric() and not hub_data[1].startswith('-'):
            raise ValueError("Error invalid character in name: "
                             f"{name} {hub_data[1]}")
        if name in name_lst:
            raise ValueError(f"Error: no hub name duplicate authorize: {name}")
        else:
            name_lst.append(name)
        # check valid name
        if '-' in name or ' ' in name:
            raise ValueError(f"Error: invalid character in name: {name}")
        # check metadata
        if len(hub.split(' ')) > 3:
            meta_data = hub.split(' ', 3)[3]
            check_meta_data(meta_data,
                            ['zone', 'color', 'max_drones'])

    # check connection
    hub_con = [value for key, value in map_data.items()
               if key.startswith("connection")]
    connection_lst: List[Tuple[str, str]] = []
    for con in hub_con:
        # check existing hub
        con_data = con.split(' ')
        if (len(con_data) > 1 and not con_data[1].startswith('[')
                or con_data[0].count('-') != 1):
            raise ValueError("Error invalid connection name: "
                             f"'{con}'")
        con_1, con_2 = con_data[0].split('-')
        if con_1 not in name_lst or con_2 not in name_lst:
            raise ValueError(f"Error: unknow hub: {con_1}-{con_2}")
        # no duplicate
        for connection in connection_lst:
            if con_1 in connection and con_2 in connection:
                raise ValueError("Error: no duplicate authorized:\n"
                                 f"{connection[0]}-{connection[1]} "
                                 f"| {con_1}-{con_2}")
        connection_lst.append((con_1, con_2))
        # check metadata
        if len(con.split(' ')) > 1:
            meta_data = con.split(' ', 1)[1]
            check_meta_data(meta_data, ['max_link_capacity'])


def main() -> None:
    """ Debug parser with sample test map """
    from src.Map import Map

    path = "data/maps/test/test.txt"
    try:
        map_data = get_data(path)
        check_data(map_data)
        mape = Map.map_init(map_data)
    except Exception as e:
        print("Invalid map file format")
        print(e)
        sys.exit()

    print()
    print("### Map Data ###")
    print(f"Drones: {mape.nb_drone}")
    print()

    print("## Hub")
    print(f"{mape.start.name}: {mape.start.pos}")
    print()
    for hub in mape.hub_lst:
        print(f"{hub.name}: {hub.pos}")
    print()
    print(f"{mape.end.name}: {mape.end.pos}")

    print()

    print("## Connection")
    for i, connection in enumerate(mape.connection_lst):
        print(f"connection {i}: {connection}")
    print()

    print("### Collor ###")
    print(f"{mape.start.name}: {mape.start.c_setting['color']}")
    for hub in mape.hub_lst:
        print(f"{hub.name}: {hub.c_setting['color']}")
    print(f"{mape.end.name}: {mape.end.c_setting['color']}")


if __name__ == "__main__":
    main()
