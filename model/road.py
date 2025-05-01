from collections import deque
import random
import math
import pygame
import numpy as np
from utils.colors import Colors
from utils.directions import Directions
from utils.sizes import Sizes


class Road:
    def __init__(self, direction, traffic_light, crosswalk, image, num_lanes = 2):
        self.direction = direction
        self.traffic_light = traffic_light
        self.crosswalk = crosswalk

        self.num_lanes = num_lanes


        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()


        if self.direction == Directions.NORTH:
            self.rect.midtop = (Sizes.WIDTH // 2, 0)
            self.crosswalk.rect.midbottom= self.rect.midbottom
            self.traffic_light.rect.midright = (self.rect.left - 20, self.rect.bottom - Sizes.TRAFFIC_LIGHT_HEIGHT)
            self.stop_line = self.crosswalk.rect.top
        elif self.direction == Directions.SOUTH:
            self.rect.midbottom = (Sizes.WIDTH // 2, Sizes.HEIGHT)
            self.crosswalk.rect.midtop = self.rect.midtop
            self.traffic_light.rect.midleft = (self.rect.right + 20, self.rect.top + Sizes.TRAFFIC_LIGHT_HEIGHT)
            self.stop_line = self.crosswalk.rect.bottom
        elif self.direction == Directions.EAST:
            self.rect.midright = (Sizes.WIDTH, Sizes.HEIGHT // 2)
            self.crosswalk.rect.midleft = self.rect.midleft
            self.traffic_light.rect.midleft = (self.rect.left + 40, self.rect.top - Sizes.TRAFFIC_LIGHT_WIDTH)
            self.stop_line = self.crosswalk.rect.right
        elif self.direction == Directions.WEST:
            self.rect.midleft = (0, Sizes.HEIGHT // 2)
            self.crosswalk.rect.midright = self.rect.midright
            self.traffic_light.rect.midright = (self.rect.right - 40, self.rect.bottom + Sizes.TRAFFIC_LIGHT_WIDTH)
            self.stop_line = self.crosswalk.rect.left


        self.spawn_positions = self.calculate_spawn_positions()
        self.last_spawn = pygame.time.get_ticks()


    def calculate_spawn_positions(self):
        positions = []
        for lane in range(self.num_lanes):
            if self.direction == Directions.NORTH:
                lane_spacing = self.rect.width // 4
                x = self.rect.left + lane_spacing * (lane + 0.5)
                y = self.rect.top
            elif self.direction == Directions.SOUTH:
                lane_spacing = self.rect.width // 4
                x = self.rect.right - lane_spacing * (lane + 0.5)
                y = self.rect.bottom
            elif self.direction == Directions.EAST:
                lane_spacing = self.rect.height // 4
                x = self.rect.right
                y = self.rect.top + lane_spacing * (lane + 0.5)
            else: # west
                lane_spacing = self.rect.height // 4
                x = self.rect.left
                y = self.rect.bottom - lane_spacing * (lane + 0.5)
            positions.append((x, y))
        print("positions", positions)
        return positions

    def get_available_lanes(self, cars):
        available_lanes = []
        for lane in range(self.num_lanes):
            spawn_pos = self.spawn_positions[lane]

            # Create collision area (adjust values based on car size)
            spawn_rect = pygame.Rect(
                spawn_pos[0] - (Sizes.CAR_SIZE // 2),  # Half car width
                spawn_pos[1] - (Sizes.CAR_SIZE // 2),    # Half car height
                Sizes.CAR_SIZE, Sizes.CAR_SIZE                # Car dimensions
            )

            # Check collisions with existing cars
            if not any(car.rect.colliderect(spawn_rect) for car in cars):
                available_lanes.append(lane)

        return available_lanes


    def draw(self, screen):
        screen.blit(self.image, self.rect)
