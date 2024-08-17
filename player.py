import pygame


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


class Player:
    def __init__(self, position, name):
        self.start_position = position.copy()
        self.position = position
        self.name = name
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 0.1
        self.radius = 0.5
        self.score = 0
        self.respawn_timer = 0

    def add_score(self, score):
        self.score += score

    def input(self, input_handler):
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

    def update(self, players, ball, powerups):
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer == 0:
                self.position = self.start_position.copy()
            else:
                return

        self.position += self.velocity

        if self.position.distance_to(ball.position) < self.radius + ball.radius:
            ball.kick(self.velocity)

        if self.position.x < -10:
            self.position.x = -10
            self.velocity.x *= -1
        if self.position.x > 10:
            self.position.x = 10
            self.velocity.x *= -1
        if self.position.y < -5:
            self.position.y = -5
            self.velocity.y *= -1
        if self.position.y > 5:
            self.position.y = 5
            self.velocity.y *= -1

        for powerup in powerups:
            if self.position.distance_to(powerup.position) < self.radius + powerup.radius:
                powerup.apply(self, ball)
                powerups.remove(powerup)

    def draw(self, camera):
        if self.respawn_timer > 0:
            return

        camera.draw_circle(pygame.Color('black'), self.position, self.radius)

    def die(self):
        self.respawn_timer = 100
