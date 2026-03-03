from src import pg
from src.Map import Map
from src.config import H_SIZE, W_SIZE
from src.config import BG_C, HUB_C, START_C, GOAL_C, LINE_C


class Renderer():
    def __init__(self):
        self.tmp_surface = pg.Surface(W_SIZE)

    @property
    def tmp_surface(self) -> pg.Surface:
        return self.__tmp_surface

    @tmp_surface.setter
    def tmp_surface(self, surface: pg.Surface) -> None:
        self.__tmp_surface = surface

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
        for key, value in map.project_pos.items():
            x, y = value
            # x *= SCALE
            # y *= SCALE
            rect = pg.Rect((0, 0), (H_SIZE, H_SIZE))
            rect.center = (x, y)
            if key == 'start':
                pg.draw.rect(self.tmp_surface, START_C, rect)
            elif key == 'goal':
                pg.draw.rect(self.tmp_surface, GOAL_C, rect)
            else:
                pg.draw.rect(self.tmp_surface, HUB_C, rect)

        # draw drone
        for drone in map.drone_lst:
            pg.draw.circle(self.tmp_surface, (255, 255, 255),
                           (drone.proj_pos[0], drone.proj_pos[1]), 10)

        # n_surface = pg.transform.smoothscale(self.tmp_surface, W_SIZE)
        window.blit(self.tmp_surface, (0, 0))
