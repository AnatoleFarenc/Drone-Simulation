from src.Menu import Menu


def main():
    """ Entry point of fly-in application """

    Menu.menu_init()
    Menu().run()


if __name__ == "__main__":
    main()
