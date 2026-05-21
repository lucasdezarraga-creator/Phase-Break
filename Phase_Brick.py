import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

paddle = pygame.Rect(screen.get_width() / 2, 610, 250, 30)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((53, 91, 156))

    pygame.draw.rect(screen, (51, 171, 44), paddle)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        paddle.x -= 300 * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        paddle.x += 300 * dt

    if paddle.left < 0:
        paddle.left = -0
    elif paddle.right > screen.get_width():
        paddle.right = screen.get_width()

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()