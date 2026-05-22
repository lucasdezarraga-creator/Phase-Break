import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

PLAYER_SPEED = 450
BALL_RADIUS = 25
BALL_SPEED = 450
BRICK_ROWS = 4
BRICK_COLUMNS = 7
BRICK_WIDTH = 120
BRICK_HEIGHT = 40
BRICK_GAP = 45
OFFSET_X = 80
OFFSET_Y = 80

BRICK_COLORS = [
    (0, 212, 255),
    (77, 182, 255),
    (0, 255, 191),
    (0, 150, 136)
]

paddle = pygame.Rect(0, 610, 250, 30)
paddle.centerx = screen.get_width() / 2

ball_pos = pygame.Vector2(paddle.centerx, paddle.top - BALL_RADIUS)
ball_velo = pygame.Vector2(0,0)

bricks = []

current_ball_color = BRICK_COLORS[3]

for row in range(BRICK_ROWS):
    for column in  range(BRICK_COLUMNS):
        x = OFFSET_X + column * (BRICK_WIDTH + BRICK_GAP)
        y = OFFSET_Y + row * (BRICK_COLUMNS + BRICK_GAP)

        brick_color = BRICK_COLORS[row]

        brick = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append({"rect": brick, "color": brick_color})

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

        if ball_pos.y - BALL_RADIUS > screen.get_height():
            was_launched = False
            ball_pos = ball_pos = pygame.Vector2(paddle.centerx, paddle.top - BALL_RADIUS)

        if ball_rect.colliderect(paddle):
            ball_pos.y = paddle.top - BALL_RADIUS
            ball_velo.y *= -1

            if ball_pos.x < paddle.centerx:
                ball_velo.x -= 100
            else:
                ball_velo.x += 100
            current_ball_color = random.choice(BRICK_COLORS)

            ball_velo.x = max(-400, min(400, ball_velo.x))

        for brick in bricks[:]:
            if ball_rect.colliderect(brick["rect"]):
                offset_left = ball_rect.right - brick["rect"].left
                offset_right = brick["rect"].right - ball_rect.left 
                offset_top = ball_rect.bottom - brick["rect"].top
                offset_bottom = brick["rect"].bottom - ball_rect.top

                smallest_offest = min(offset_left, offset_right, offset_top, offset_bottom)

                if smallest_offest == offset_left:
                    ball_pos.x = brick["rect"].left - BALL_RADIUS
                    ball_velo.x *= -1
                elif smallest_offest == offset_right:
                    ball_pos.x = brick["rect"].right + BALL_RADIUS
                    ball_velo.x *= -1
                elif smallest_offest == offset_top:
                    ball_pos.y = brick["rect"].top - BALL_RADIUS
                    ball_velo.y *= -1
                elif smallest_offest == offset_bottom:
                    ball_pos.y = brick["rect"].bottom + BALL_RADIUS
                    ball_velo.y *= -1

                if current_ball_color == brick["color"]:
                    bricks.remove(brick)
                break

    if paddle.left < 0:
        paddle.left = 0
    elif paddle.right > screen.get_width():
        paddle.right = screen.get_width()

    screen.fill((12, 48, 92))
    pygame.draw.rect(screen, (235, 245, 255), paddle)
    pygame.draw.circle(screen, current_ball_color, ball_pos, BALL_RADIUS)

    for brick in bricks:
        pygame.draw.rect(screen, brick["color"], brick["rect"])

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()