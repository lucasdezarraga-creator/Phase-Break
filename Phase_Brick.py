import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

PLAYER_SPEED = 450
BALL_RADIUS = 25
BALL_SPEED = 450

paddle = pygame.Rect(0, 610, 250, 30)
paddle.centerx = screen.get_width() / 2

ball_pos = pygame.Vector2(paddle.centerx, paddle.top - BALL_RADIUS)
ball_velo = pygame.Vector2(0,0)

brick = pygame.Rect(100, 100, 120, 40)

was_launched = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        paddle.x -= PLAYER_SPEED * dt
        if not was_launched:
            ball_pos.x = paddle.x + (paddle.width / 2)

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        paddle.x += PLAYER_SPEED * dt
        if not was_launched:
            ball_pos.x = paddle.x + (paddle.width / 2)

    if keys[pygame.K_SPACE] and not was_launched:
        was_launched = True

        ball_velo.x = BALL_SPEED * 0.7
        ball_velo.y = -BALL_SPEED * 0.7

    if was_launched:
        ball_pos.x += ball_velo.x * dt
        ball_pos.y += ball_velo.y * dt

        ball_rect = pygame.Rect(ball_pos.x - BALL_RADIUS, ball_pos.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

        if ball_pos.x - BALL_RADIUS < 0:
            ball_pos.x = BALL_RADIUS
            ball_velo.x *= -1
        elif ball_pos.x + BALL_RADIUS > screen.get_width():
            ball_pos.x = screen.get_width() - BALL_RADIUS
            ball_velo.x *= -1

        if ball_pos.y - BALL_RADIUS < 0:
            ball_pos.y = BALL_RADIUS
            ball_velo.y *= -1

        if ball_rect.colliderect(paddle):
            ball_pos.y = paddle.y - BALL_RADIUS
            ball_velo.y *= -1

        if ball_rect.colliderect(brick):
            offset_left = ball_rect.right - brick.left
            offset_right = brick.right - ball_rect.left 
            offset_top = ball_rect.bottom - brick.top
            offset_bottom = brick.bottom - ball_rect.top

            smallest_offest = min(offset_left, offset_right, offset_top, offset_bottom)

            if smallest_offest == offset_left:
                ball_pos.x = brick.left - BALL_RADIUS
                ball_velo.x *= -1
            elif smallest_offest == offset_right:
                ball_pos.x = brick.right + BALL_RADIUS
                ball_velo.x *= -1
            elif smallest_offest == offset_top:
                ball_pos.y = brick.top - BALL_RADIUS
                ball_velo.x *= -1
            elif smallest_offest == offset_bottom:
                ball_pos.y = brick.bottom + BALL_RADIUS
                ball_velo.y *= -1

    if paddle.left < 0:
        paddle.left = 0
    elif paddle.right > screen.get_width():
        paddle.right = screen.get_width()

    screen.fill((53, 91, 156))
    pygame.draw.rect(screen, (51, 171, 44), paddle)
    pygame.draw.rect(screen, (255, 0, 0), brick)
    pygame.draw.circle(screen, (136, 27, 179), ball_pos, BALL_RADIUS)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()