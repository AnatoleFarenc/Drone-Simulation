from src import pg
from src.Map import Map
from src.config import H_SIZE, W_SIZE
from src.config import BG_C, HUB_C, LINE_C
import colorsys
import time
import math


class Renderer():
    """ Pygame renderer for map and drones """

    def __init__(self) -> None:
        """ Init temporary drawing surface """
        self.tmp_surface = pg.Surface(W_SIZE)

    @property
    def tmp_surface(self) -> pg.Surface:
        """ Return temporary surface """
        return self.__tmp_surface

    @tmp_surface.setter
    def tmp_surface(self, surface: pg.Surface) -> None:
        """ Set temporary surface """
        self.__tmp_surface = surface

    @staticmethod
    def rainbow_color(t: float) -> tuple[int, int, int]:
        """ Create rainbow color"""
        r, g, b = colorsys.hls_to_rgb(t, 0.5, 1.0)
        return (int(r * 255), int(g * 255), int(b * 255))

    def render(self, window: pg.Surface, map: Map) -> None:
        """ render """
        self.tmp_surface.fill(BG_C)

        # draw connection
        for connection in map.connection_lst:
            h_1, h_2 = connection.hubs
            h_1_pos = map.project_pos[h_1.name]
            h_2_pos = map.project_pos[h_2.name]
            pg.draw.line(self.tmp_surface, LINE_C, h_1_pos, h_2_pos, 10)

        # draw hub
        speed = 1.5
        rainbow_t = (math.sin(time.time() * speed) + 1) / 2

        for key, value in map.project_pos.items():
            x, y = value
            rect = pg.Rect((0, 0), (H_SIZE, H_SIZE))
            rect.center = (x, y)

            hub = map.get_hub(key)
            if hub is None:
                continue
            color = hub.color
            if color == "rainbow":
                color = self.rainbow_color(rainbow_t)
            try:
                pg.draw.rect(self.tmp_surface, color, rect)
            except ValueError:
                pg.draw.rect(self.tmp_surface, HUB_C, rect)

        # draw drone
        for drone in map.drone_lst:
            pg.draw.circle(self.tmp_surface, (255, 255, 255),
                           (drone.proj_pos[0], drone.proj_pos[1]), 10)

        window.blit(self.tmp_surface, (0, 0))
