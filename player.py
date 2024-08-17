from enum import Enum

import pygame

from level import Level

CONTROLS = {
    "player1": {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
    },
    "player2": {
        "up": pygame.K_i,
        "down": pygame.K_k,
        "left": pygame.K_j,
        "right": pygame.K_l,
    }
}


class AiState(Enum):
    IDLE = 0
    ATTACK = 1
    DEFEND = 2


class Player:
    def __init__(self, position, name, ai_enabled=False):
        self.start_position = position.copy()
        self.position = position
        self.angle = 0.0
        self.name = name
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 0.1
        self.radius = 0.5
        self.score = 0
        self.respawn_timer = 0
        self.movement_timer = 500
        self.target = pygame.Vector2(0, 0)
        self.ai_enabled = ai_enabled
        self.ai_state = AiState.IDLE

    def add_score(self, score):
        self.score += score

    def input(self, input_handler):
        if self.ai_enabled:
            return # AI doesn't need input

        self.velocity = pygame.Vector2(0, 0)

        if input_handler.key_down[CONTROLS[self.name]["up"]]:
            self.velocity.y = 1
        if input_handler.key_down[CONTROLS[self.name]["down"]]:
            self.velocity.y = -1
        if input_handler.key_down[CONTROLS[self.name]["left"]]:
            self.velocity.x = -1
        if input_handler.key_down[CONTROLS[self.name]["right"]]:
            self.velocity.x = 1

        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed
            self.movement_timer = 0
        else:
            self.movement_timer += 1

    def update(self, players, ball, powerups):
        if self.ai_enabled:
            own_goal = pygame.Vector2(12, 0)
            enemy_goal = pygame.Vector2(-12, 0)

            if self.ai_state == AiState.IDLE:
                if ball.position.x > 1:
                    self.ai_state = AiState.DEFEND

                self.target = self.start_position
            elif self.ai_state == AiState.DEFEND:
                if self.position.x < ball.position.x:
                    self.target = ball.position + pygame.Vector2(0, self.radius + ball.radius + 1)
                else:
                    self.target = (ball.position + own_goal) / 2

                    if self.position.distance_to(self.target) < 0.1:
                        self.ai_state = AiState.ATTACK
            elif self.ai_state == AiState.ATTACK:
                if self.position.x > ball.position.x:
                    self.target = ball.position
                else:
                    self.target = (ball.position + enemy_goal) / 2

                if self.position.x < ball.position.x:
                    self.ai_state = AiState.DEFEND

            if ball.position.x < enemy_goal.x:
                self.ai_state = AiState.IDLE

            self.velocity = self.target - self.position
            if self.velocity.length() > 0:
                self.velocity = self.velocity.normalize() * self.speed

        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer == 0:
                self.position = self.start_position.copy()
            else:
                return

        self.position += self.velocity
        if self.velocity.length() > 0:
            angle = self.velocity.as_polar()[1] + 90
            delta_angle = angle - self.angle
            if delta_angle > 180:
                delta_angle -= 360
            self.angle += 0.5 * delta_angle

        if self.position.distance_to(ball.position) < self.radius + ball.radius:
            ball.kick(ball.position - self.position)

        if self.position.x + self.radius > Level.right:
            self.position.x = Level.right - self.radius
            self.velocity.x *= -1
        if self.position.x - self.radius < Level.left:
            self.position.x = Level.left + self.radius
            self.velocity.x *= -1
        if self.position.y + self.radius > Level.top:
            self.position.y = Level.top - self.radius
            self.velocity.y *= -1
        if self.position.y - self.radius < Level.bottom:
            self.position.y = Level.bottom + self.radius
            self.velocity.y *= -1

    def draw(self, camera, image_handler):
        camera.draw_text(str(self.score), self.start_position + pygame.Vector2(0, 5), 1)

        if self.respawn_timer > 0:
            return

        # transparent black circle
        camera.draw_transparent_circle(pygame.Color(0, 0, 0, 20), self.position, self.radius)
        camera.draw_image(image_handler.get_image(self.name), self.position, pygame.Vector2(self.radius * 2.5, self.radius * 2.5), self.angle)

        if self.movement_timer > 500:
            camera.draw_text(pygame.key.name(CONTROLS[self.name]["up"]), self.position + pygame.Vector2(0, 1), 1)
            camera.draw_text(pygame.key.name(CONTROLS[self.name]["down"]), self.position + pygame.Vector2(0, -1), 1)
            camera.draw_text(pygame.key.name(CONTROLS[self.name]["left"]), self.position + pygame.Vector2(-1, 0), 1)
            camera.draw_text(pygame.key.name(CONTROLS[self.name]["right"]), self.position + pygame.Vector2(1, 0), 1)

        #camera.draw_circle(pygame.Color('black'), self.target, 0.1)
        #camera.draw_text(self.ai_state.name, self.position + pygame.Vector2(0, 2), 1)

    def die(self):
        self.respawn_timer = 100
