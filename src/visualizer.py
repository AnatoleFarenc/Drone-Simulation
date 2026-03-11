from .Map import Map
from .Renderer import Renderer
from . import pg
from .config import W_SIZE
import math


def view_simulation(map: Map, turn_idx: int):
    movers = []
    if turn_idx < 0 or turn_idx >= len(map.movements):
        return movers

    for move_str in map.movements[turn_idx]:
        if move_str.endswith("-stay"):
            continue

        parts = move_str.split("-")
        drone = map.get_drone(parts[0])
        if drone is None:
            continue

        movers.append(drone)

        drone.start_pos = list(drone.proj_pos)

        if len(parts) == 2:
            target = map.get_hub(parts[1])
        else:
            hub1 = map.get_hub(parts[1])
            hub2 = map.get_hub(parts[2])
            x1, y1 = map.project_pos[hub1.name]
            x2, y2 = map.project_pos[hub2.name]
            drone.end_pos = ((x1 + x2) / 2, (y1 + y2) / 2)
            drone.c_hub = hub2
            continue

        if target is not None:
            drone.end_pos = map.project_pos[target.name]
            drone.c_hub = target

    return movers


def animate(map: Map, speed: float = 1.0):
    if not map.movements:
        map.play_map()

    for d in map.drone_lst:
        d.c_hub = map.start

    pg.init()
    window = pg.display.set_mode(W_SIZE, pg.SCALED | pg.RESIZABLE)
    pg.display.set_caption("Fly‑In animation")
    clock = pg.time.Clock()
    renderer = Renderer()

    for d in map.drone_lst:
        d.proj_pos = list(map.project_pos[map.start.name])

    turn = 0
    movers = view_simulation(map, turn)
    t = 0.0
    running = True

    while running and turn < len(map.movements):
        dt = clock.tick(60) / 1000.0
        t += dt

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
                break

        progress = t / speed
        progress = min(progress, 1)
        progress = (1 - math.cos(progress * math.pi)) / 2

        for drone in movers:
            x1, y1 = drone.start_pos
            x2, y2 = drone.end_pos
            drone.proj_pos[0] = x1 + (x2 - x1) * progress
            drone.proj_pos[1] = y1 + (y2 - y1) * progress

        if progress >= 1:
            for drone in movers:
                drone.proj_pos = list(drone.end_pos)
            t = 0
            turn += 1
            movers = view_simulation(map, turn)

        renderer.render(window, map)
        pg.display.flip()

    pg.quit()
