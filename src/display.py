import curses
from .Map import Map


def init_curses(stdsrc: curses.window):
    """ Display drone map """

    # Init curs
    curses.curs_set(0)
    stdsrc.nodelay(False)
    stdsrc.clear()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)


def display_map(stdscr: curses.window, map: Map):
    """ Draw map hubs in terminal """
    y_offset = 3
    x_offset = 5
    s_x, s_y = map.start.pos
    e_x, e_y = map.end.pos
    s_y += y_offset
    e_y += y_offset
    stdscr.addstr(s_y, s_x, "█", curses.color_pair(2))
    i = 0
    for i, hub in enumerate(map.hub_lst, 1):
        x_offset *= i
        h_x, h_y = hub.pos
        h_y += y_offset
        h_x += x_offset
        stdscr.addstr(h_y, h_x, "█", curses.color_pair(3))
    x_offset *= i
    e_x += x_offset
    stdscr.addstr(e_y, e_x, "█", curses.color_pair(1))
