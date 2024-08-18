import random

import pygame


class Level:
    left = -12
    right = 12
    top = 6
    bottom = -6

    goal_width = 6
    goal_post_radius = 0.5

    shadow_color = pygame.Color(0, 0, 0, 50)

    @staticmethod
    def goal_posts():
        return [
            pygame.Vector2(Level.right + Level.goal_post_radius, Level.goal_width / 2),
            pygame.Vector2(Level.right + Level.goal_post_radius, -Level.goal_width / 2),
            pygame.Vector2(Level.left - Level.goal_post_radius, Level.goal_width / 2),
            pygame.Vector2(Level.left - Level.goal_post_radius, -Level.goal_width / 2)
        ]

    @staticmethod
    def random_position(margin=0):
        return pygame.Vector2(random.uniform(Level.left + margin, Level.right - margin),
                              random.uniform(Level.bottom + margin, Level.top - margin))
