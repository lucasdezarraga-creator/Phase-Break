import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

PLAYER_SPEED = 450
BOUNCE_ANGLE = 45
BALL_RADIUS = 25

paddle = pygame.Rect(0, 610, 250, 30)
paddle.centerx = screen.get_width() / 2

ballpos = pygame.Vector2(paddle.centerx, paddle.top - BALL_RADIUS)

was_launched = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((53, 91, 156))

    pygame.draw.rect(screen, (51, 171, 44), paddle)
    pygame.draw.circle(screen, (136, 27, 179), ballpos, BALL_RADIUS)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        paddle.x -= PLAYER_SPEED * dt
        if not was_launched:
            ballpos.x = paddle.x + (paddle.width / 2)

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        paddle.x += PLAYER_SPEED * dt
        if not was_launched:
            ballpos.x = paddle.x + (paddle.width / 2)
    if keys[pygame.K_SPACE]:
        was_launched = True

    if paddle.left < 0:
        paddle.left = 0
    elif paddle.right > screen.get_width():
        paddle.right = screen.get_width()


    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()