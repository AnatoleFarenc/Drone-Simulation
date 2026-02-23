from .Map import Map
from .parser import get_data, check_data
import curses
import sys
from typing import Tuple

# env/bin/python3 -m src.Visualizer

GREEN = 1
RED = 2
YELLOW = 3


class Visualizer():
    def __init__(self, stdscr: curses.window, map: Map):
        self.map = map
        self.stdscr = stdscr
        self.size = (self.get_max_pos()[0] + 1, self.get_max_pos()[1] + 1)

        curses.curs_set(0)
        self.stdscr.nodelay(False)
        self.stdscr.clear
        self.init_color()

    @property
    def map(self) -> Map:
        return self.__map

    @map.setter
    def map(self, map: Map) -> None:
        self.__map = map

    @property
    def size(self) -> Tuple[int, int]:
        return self.__size

    @size.setter
    def size(self, size: Tuple[int, int]) -> None:
        self.__size = size

    @property
    def stdscr(self) -> curses.window:
        return self.__stdscr

    @stdscr.setter
    def stdscr(self, stdscr: curses.window) -> None:
        self.__stdscr = stdscr

    def get_max_pos(self) -> Tuple[int, int]:
        pos_lst = [hub.pos for hub in self.map.hub_lst
                   + [self.map.start, self.map.end]]
        x_lst = [pos[0] for pos in pos_lst]
        y_lst = [pos[1] for pos in pos_lst]
        return (max(x_lst), max(y_lst))

    def get_min_pos(self) -> Tuple[int, int]:
        pos_lst = [hub.pos for hub in self.map.hub_lst
                   + [self.map.start, self.map.end]]
        x_lst = [pos[0] for pos in pos_lst]
        y_lst = [pos[1] for pos in pos_lst]
        return (min(x_lst), min(y_lst))

    def init_color(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)


def main(stdscr: curses.window) -> None:
    path = "data/maps/easy/01_linear_path.txt"
    try:
        map_data = get_data(path)
        check_data(map_data)
        map = Map.map_init(map_data)
    except Exception as e:
        print("Invalid map file format")
        print(e)
        sys.exit()

    view = Visualizer(stdscr, map)
    view.stdscr.addstr(1, 5, "Ceci est un test", curses.color_pair(RED))

    stdscr.addstr(15, 5, "Press any key to exit...")
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
