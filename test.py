import curses
import time


def main(stdscr: curses.window) -> None:
    # Configuration de base
    curses.curs_set(0)  # Cache le curseur
    stdscr.nodelay(False)  # Attend une touche
    stdscr.clear()

    # Initialisation des couleurs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Affichage statique
    stdscr.addstr(1, 5, "Drone Simulation", curses.color_pair(3))
    stdscr.addstr(3, 5, "Start", curses.color_pair(1))
    stdscr.addstr(3, 40, "Goal", curses.color_pair(2))

    # Simulation simple d’un drone qui avance
    for x in range(11, 39):
        stdscr.addstr(3, x, "█", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.05)
        stdscr.addstr(3, x, " ")  # Efface ancienne position

    # Position finale
    # stdscr.addstr(3, 39, "D", curses.color_pair(2))
    stdscr.refresh()

    stdscr.addstr(15, 5, "Press any key to exit...")
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)