from parser import get_data, check_data


def main():
    path = "maps/easy/01_linear_path.txt"
    map_data = get_data(path)
    try:
        check_data(map_data)
    except Exception as e:
        print("Invalid map file format")
        print(e)


if __name__ == "__main__":
    main()
