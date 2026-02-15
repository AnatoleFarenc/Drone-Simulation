from Map import Map


def get_data(map_path: str) -> dict:
    map_data = {}
    with open(map_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split(":", 1)
                map_data.update({key: value})
    return map_data


def main():
    map_data = get_data("01_linear_path.txt")

    for key, value in map_data.items():
        print(f"{key}: {value}")

    map_easy = Map.map_init(map_data)

    print()
    print(f"{map_easy.start.name}: {map_easy.start.pos} -> color: {map_easy.start.color}")
    print(f"{map_easy.end.name}: {map_easy.end.pos} -> color: {map_easy.end.color}")
    print(f"{map_easy.hub_lst[0].name}: {map_easy.hub_lst[0].pos} -> color: {map_easy.hub_lst[0].color}")
    print(f"Connection: {map_easy.connection_lst[0].name}")


if __name__ == "__main__":
    main()
