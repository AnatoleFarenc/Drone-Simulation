from src import pg
from src.Map import Map
from src.config import H_SIZE, W_SIZE
from src.config import BG_C, HUB_C, START_C, GOAL_C


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

        # n_surface = pg.transform.smoothscale(self.tmp_surface, W_SIZE)
        window.blit(self.tmp_surface, (0, 0))
