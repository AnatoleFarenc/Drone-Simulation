from src.Menu import Menu


def main():
    """ Entry point of fly-in application """

    # info = False
    # import sys
    # if len(sys.argv) >= 2:
    #     if sys.argv[1] == "--capacity-info":
    #         info = True
    # Menu.menu_init(info)
    Menu.menu_init()
    Menu().run()


if __name__ == "__main__":
    main()
