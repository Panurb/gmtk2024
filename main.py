import asyncio
from collections import defaultdict
from enum import Enum
import random

import pygame

from ball import Ball
from camera import Camera
from player import Player
from powerup import Powerup

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WEB = True


class State(Enum):
    QUIT = 0
    GAME = 1
    MENU = 2


class InputHandler:
    def __init__(self):
        self.key_down = defaultdict(bool)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.key_down[event.key] = True
            if event.type == pygame.KEYUP:
                self.key_down[event.key] = False


class Main:
    def __init__(self, width, height):
        # init mixer first to prevent audio delay
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()

        pygame.init()
        pygame.display.set_caption('Ant soccer')

        self.info = pygame.display.Info()
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
        self.camera = Camera(pygame.Vector2(0, 0), 50, self.screen)
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.state = State.GAME

        self.mouse = pygame.Vector2(0, 0)

        self.players = []

        self.players.append(Player(pygame.Vector2(-8, 0), "player1"))
        self.players.append(Player(pygame.Vector2(8, 0), "player2"))

        self.ball = Ball(pygame.Vector2(0, 0), 0.5)

        self.powerups = []
        self.powerup_timer = 300

        self.input_handler = InputHandler()

        self.max_score = 5

        self.win_timer = 0

    def reset(self):
        self.players = []

        self.players.append(Player(pygame.Vector2(-8, 0), "player1"))
        self.players.append(Player(pygame.Vector2(8, 0), "player2"))

        self.ball = Ball(pygame.Vector2(0, 0), 0.1)

        self.powerups = []
        self.powerup_timer = 300

    def input(self):
        self.input_handler.update()

        for player in self.players:
            player.input(self.input_handler)

    def update(self):
        if self.win_timer > 0:
            self.win_timer -= 1
            if self.win_timer == 0:
                self.reset()
            return

        for player in self.players:
            player.update(self.players, self.ball, self.powerups)
            if player.score >= self.max_score:
                self.win_timer = 100
        self.ball.update(self.players)

        self.powerup_timer -= 1

        if len(self.powerups) < 5 and self.powerup_timer <= 0:
            self.powerups.append(Powerup(pygame.Vector2(random.uniform(-10, 10), random.uniform(-5, 5))))
            self.powerup_timer = 300

    def draw(self):
        self.screen.fill(pygame.Color('dark green'))
        for player in self.players:
            player.draw(self.camera)
        self.ball.draw(self.camera)
        for powerup in self.powerups:
            powerup.draw(self.camera)

        if self.win_timer > 0:
            self.camera.draw_text("Player 1 wins!" if self.players[0].score >= self.max_score else "Player 2 wins!", pygame.Vector2(0, 0), 2)

    def main_loop(self):
        while self.state != State.QUIT:
            self.input()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

            pygame.display.update()

    async def main_loop_web(self):
        while self:
            self.input()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)
            await asyncio.sleep(0)


def main():
    main_window = Main(SCREEN_WIDTH, SCREEN_HEIGHT)
    if WEB:
        asyncio.run(main_window.main_loop_web())
    else:
        main_window.main_loop()


if __name__ == '__main__':
    main()
