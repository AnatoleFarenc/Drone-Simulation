import pygame
import math

pygame.init()
WINDOW_SIZE = (500, 400)
SCALE = 3  # Supersampling pour anti-aliasing
LARGE_SIZE = (WINDOW_SIZE[0]*SCALE, WINDOW_SIZE[1]*SCALE)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Camera + Renderer Example")
clock = pygame.time.Clock()

# Couleurs
BG = (30, 30, 40)
LINE_COLOR = (200, 200, 255)
SQUARE_COLOR = (100, 220, 150)
MOBILE_COLOR = (255, 100, 100)

# -------- Camera --------
class Camera:
    def __init__(self, width, height, scale=1):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = 200  # pixels/sec

    def apply(self, pos):
        """Convert world coordinates to screen coordinates"""
        sx = (pos[0] - self.x) * self.scale
        sy = (pos[1] - self.y) * self.scale
        return int(sx), int(sy)

    def handle_input(self, keys, dt):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.x += self.speed * dt
        if keys[pygame.K_UP]:
            self.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.y += self.speed * dt

camera = Camera(WINDOW_SIZE[0], WINDOW_SIZE[1], SCALE)

# -------- Renderer --------
class Renderer:
    def __init__(self, camera):
        self.camera = camera
        self.temp_surface = pygame.Surface(LARGE_SIZE)

    def render(self, static_objects, moving_objects):
        self.temp_surface.fill(BG)

        # Dessiner objets statiques
        for obj in static_objects:
            if obj["type"] == "rect":
                rect = pygame.Rect(0, 0, obj["size"][0]*SCALE, obj["size"][1]*SCALE)
                rect.center = self.camera.apply(obj["pos"])
                pygame.draw.rect(self.temp_surface, obj["color"], rect)
            elif obj["type"] == "line":
                start = self.camera.apply(obj["start"])
                end = self.camera.apply(obj["end"])
                pygame.draw.aaline(self.temp_surface, obj["color"], start, end)

        # Dessiner objets mobiles
        for obj in moving_objects:
            rect = pygame.Rect(0, 0, obj["size"][0]*SCALE, obj["size"][1]*SCALE)
            rect.center = self.camera.apply(obj["pos"])
            pygame.draw.rect(self.temp_surface, obj["color"], rect)

        # Anti-aliasing via supersampling
        small_surface = pygame.transform.smoothscale(self.temp_surface, WINDOW_SIZE)
        screen.blit(small_surface, (0, 0))

renderer = Renderer(camera)

# -------- Objets --------
static_objects = [
    {"type":"rect", "pos":(100, 150), "size":(40, 40), "color":SQUARE_COLOR},
    {"type":"rect", "pos":(400, 150), "size":(40, 40), "color":SQUARE_COLOR},
    {"type":"line", "start":(100,150), "end":(400,150), "color":LINE_COLOR}
]

# Mobile object initial position
t = 0
moving_objects = [{"pos":(250, 300), "size":(30,30), "color":MOBILE_COLOR}]

# -------- Boucle principale --------
running = True
while running:
    dt = clock.tick(60)/1000
    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gérer la caméra via flèches
    keys = pygame.key.get_pressed()
    camera.handle_input(keys, dt)

    # Exemple animation : objet mobile qui oscille horizontalement
    moving_objects[0]["pos"] = (250 + 100*math.sin(t), 300)

    # Rendu
    renderer.render(static_objects, moving_objects)
    pygame.display.flip()

pygame.quit()