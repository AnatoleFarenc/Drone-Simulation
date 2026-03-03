import pygame

SPEED = 200  # pixels per second


def main():
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Camera test")

    clock = pygame.time.Clock()

    camera = [0, 0]

    rects = [
        pygame.Rect((400, 300), (10, 10)),
        pygame.Rect((-10, 10), (10, 10))
    ]

    colors = [(255, 0, 0), (0, 0, 255)]

    running = True
    while running:
        dt = clock.tick(60) / 1000  # delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            camera[1] += SPEED * dt
        if keys[pygame.K_UP]:
            camera[1] -= SPEED * dt
        if keys[pygame.K_LEFT]:
            camera[0] -= SPEED * dt
        if keys[pygame.K_RIGHT]:
            camera[0] += SPEED * dt

        window.fill((255, 255, 255))

        for i, rect in enumerate(rects):
            display_rect = rect.move(-camera[0], -camera[1])
            pygame.draw.rect(window, colors[i], display_rect)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()