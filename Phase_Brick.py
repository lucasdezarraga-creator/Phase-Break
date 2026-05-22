import pygame
import random
import sys

class PhaseBricks:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.PLAYER_SPEED = 450
        self.BALL_RADIUS = 25
        self.BALL_SPEED = 450
        self.BRICK_ROWS = 4
        self.BRICK_COLUMNS = 9
        self.BRICK_WIDTH = 120
        self.BRICK_HEIGHT = 40
        self.BRICK_GAP = 10
        self.OFFSET_X = 60
        self.OFFSET_Y = 80

        self.BRICK_COLORS = [
            (0, 212, 255),
            (77, 182, 255),
            (0, 255, 191),
            (0, 150, 136)
        ]

        self.reset()

    def create_bricks(self):
        new_bricks = []
        for row in range(self.BRICK_ROWS):
            for column in  range(self.BRICK_COLUMNS):
                x = self.OFFSET_X + column * (self.BRICK_WIDTH + self.BRICK_GAP)
                y = self.OFFSET_Y + row * (self.BRICK_HEIGHT + self.BRICK_GAP)

                brick_color = self.BRICK_COLORS[row]

                brick = pygame.Rect(x, y, self.BRICK_WIDTH, self.BRICK_HEIGHT)
                new_bricks.append({"rect": brick, "color": brick_color})
        return new_bricks

    def reset(self):
        self.paddle = pygame.Rect(0, 610, 250, 30)
        self.paddle.centerx = self.screen.get_width() / 2

        self.ball_pos = pygame.Vector2(self.paddle.centerx, self.paddle.top - self.BALL_RADIUS)
        self.ball_velo = pygame.Vector2(0,0)

        self.current_ball_color = self.BRICK_COLORS[3]
        self.bricks = self.create_bricks()

        self.was_launched = True

        self.ball_velo.x = self.BALL_SPEED * 0.7
        self.ball_velo.y = -self.BALL_SPEED * 0.7

        return self.get_game_data()

    def get_game_data(self):
        return(
            self.paddle.x,
            self.ball_pos.x,
            self.ball_pos.y,
            self.ball_velo.x,
            self.ball_velo.y
        )

    def step(self, action, dt = 0.016):
        reward = 100
        done = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if action == 0:
            self.paddle.x -= self.PLAYER_SPEED * dt
        elif action == 2: 
            self.paddle.x += self.PLAYER_SPEED * dt

        if self.paddle.left < 0:
            self.paddle.left = 0
        elif self.paddle.right > self.screen.get_width():
            self.paddle.right = self.screen.get_width()

        if self.was_launched:
            self.ball_pos.x += self.ball_velo.x * dt
            self.ball_pos.y += self.ball_velo.y * dt

            ball_rect = pygame.Rect(self.ball_pos.x - self.BALL_RADIUS, self.ball_pos.y - self.BALL_RADIUS, self.BALL_RADIUS * 2, self.BALL_RADIUS * 2)

            if self.ball_pos.x - self.BALL_RADIUS < 0:
                self.ball_pos.x = self.BALL_RADIUS
                self.ball_velo.x *= -1
            elif self.ball_pos.x + self.BALL_RADIUS > self.screen.get_width():
                self.ball_pos.x = self.screen.get_width() - self.BALL_RADIUS
                self.ball_velo.x *= -1

            if self.ball_pos.y - self.BALL_RADIUS < 0:
                self.ball_pos.y = self.BALL_RADIUS
                self.ball_velo.y *= -1

            if self.ball_pos.y - self.BALL_RADIUS > self.screen.get_height():
                reward = -500
                done = True

            if ball_rect.colliderect(self.paddle):
                self.ball_pos.y = self.paddle.top - self.BALL_RADIUS
                self.ball_velo.y *= -1
                reward = 30

                if self.ball_pos.x < self.paddle.centerx:
                    self.ball_velo.x -= 100
                else:
                    self.ball_velo.x += 100

                self.ball_velo.x = max(-400, min(400, self.ball_velo.x))
                self.current_ball_color = random.choice(self.BRICK_COLORS)

            for brick in self.bricks[:]:
                if ball_rect.colliderect(brick["rect"]):
                    offset_left   = abs(ball_rect.right - brick["rect"].left)
                    offset_right  = abs(brick["rect"].right - ball_rect.left)
                    offset_top    = abs(ball_rect.bottom - brick["rect"].top)
                    offset_bottom = abs(brick["rect"].bottom - ball_rect.top)

                    smallest_offest = min(offset_left, offset_right, offset_top, offset_bottom)

                    if smallest_offest == offset_left:
                        self.ball_pos.x = brick["rect"].left - self.BALL_RADIUS
                        self.ball_velo.x *= -1
                    elif smallest_offest == offset_right:
                        self.ball_pos.x = brick["rect"].right + self.BALL_RADIUS
                        self.ball_velo.x *= -1
                    elif smallest_offest == offset_top:
                        self.ball_pos.y = brick["rect"].top - self.BALL_RADIUS
                        self.ball_velo.y *= -1
                    elif smallest_offest == offset_bottom:
                        self.ball_pos.y = brick["rect"].bottom + self.BALL_RADIUS
                        self.ball_velo.y *= -1

                    if self.current_ball_color == brick["color"]:
                        self.bricks.remove(brick)
                        reward = 20

                        if len(self.bricks) == 0:
                            reward = 500
                            done = True
                        else:
                            reward = -2
                        break

        self.screen.fill((12, 48, 92))
        pygame.draw.rect(self.screen, (235, 245, 255), self.paddle)
        pygame.draw.circle(self.screen, self.current_ball_color, self.ball_pos, self.BALL_RADIUS)

        for brick in self.bricks:
            pygame.draw.rect(self.screen, brick["color"], brick["rect"])

        pygame.display.flip()

        pygame.event.pump()
        self.clock.tick(120)

        return self.get_game_data(), reward, done
