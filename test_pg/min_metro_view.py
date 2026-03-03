import pygame
import math

pygame.init()
WINDOW_SIZE = (1000, 700)
SCALE = 3  # facteur pour agrandir la surface temporaire
LARGE_SIZE = (WINDOW_SIZE[0]*SCALE, WINDOW_SIZE[1]*SCALE)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Drone Flow Visualization")

clock = pygame.time.Clock()
running = True

# Palette moderne
BG = (18, 18, 25)
LINE = (90, 90, 110)
START = (80, 220, 120)
NORMAL = (80, 140, 255)
GOAL = (240, 80, 80)

# Noeuds
nodes = {
    "start": (200, 350),
    "wp1": (400, 250),
    "wp2": (400, 450),
    "center": (600, 350),
    "goal": (800, 350),
}

connections = [
    ("start", "wp1"),
    ("start", "wp2"),
    ("wp1", "center"),
    ("wp2", "center"),
    ("center", "goal"),
]

# 1️⃣ Pré-dessiner tout ce qui est statique
static_surface = pygame.Surface(LARGE_SIZE)
static_surface.fill(BG)

# Dessiner connexions
for a, b in connections:
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]
    pygame.draw.line(static_surface, LINE,
                     (x1*SCALE, y1*SCALE),
                     (x2*SCALE, y2*SCALE),
                     4*SCALE)

# Dessiner hubs
for name, pos in nodes.items():
    x, y = pos
    x *= SCALE
    y *= SCALE
    if name == "start":
        pygame.draw.circle(static_surface, START, (x, y), 20*SCALE)
    elif name == "goal":
        size = 22*SCALE
        triangle = [
            (x, y - size),
            (x - size, y + size),
            (x + size, y + size),
        ]
        pygame.draw.polygon(static_surface, GOAL, triangle)
    else:
        rect = pygame.Rect(0, 0, 40*SCALE, 40*SCALE)
        rect.center = (x, y)
        pygame.draw.rect(static_surface, NORMAL, rect, border_radius=8*SCALE)

t = 0

while running:
    dt = clock.tick(60) / 1000
    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2️⃣ Copier la surface statique
    temp_surface = static_surface.copy()

    # 3️⃣ Dessiner drones animés
    x1, y1 = nodes["start"]
    x2, y2 = nodes["wp1"]
    interp = (math.sin(t) + 1) / 2
    dx = x1 + (x2 - x1) * interp
    dy = y1 + (y2 - y1) * interp
    pygame.draw.circle(temp_surface, (255, 255, 255), (int(dx*SCALE), int(dy*SCALE)), 6*SCALE)

    # 4️⃣ Réduire avec lissage
    small_surface = pygame.transform.smoothscale(temp_surface, WINDOW_SIZE)

    # 5️⃣ Afficher
    screen.blit(small_surface, (0, 0))
        pygame.display.flip()

pygame.quit()