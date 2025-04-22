import random
import pygame
from math import cos, radians, sin
from utils.colors import Colors
from utils.sizes import Sizes
from utils.directions import Directions
from utils.turn_state import TurnState


class Car:
    def __init__(self, direction):
        self.direction = direction
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.waiting_time = 0.0
        self.total_wait = 0.0
        self.turn = random.choice([TurnState.STRAIGHT, TurnState.TURNING])
        self.turn_direction = None
        self.turn_progress = 0
        self.angle = 0
        self.set_initial_position()
        self.set_turn_direction()

    def set_initial_position(self):
        offset = Sizes.CAR_SIZE * 3
        if self.direction == Directions.NORTH:
            self.x = Sizes.WIDTH // 2 + Sizes.ROAD_WIDTH // 4
            self.y = Sizes.HEIGHT + offset
        elif self.direction == Directions.SOUTH:
            self.x = Sizes.WIDTH // 2 - Sizes.ROAD_WIDTH // 4
            self.y = -offset
        elif self.direction == Directions.EAST:
            self.x = -offset
            self.y = Sizes.HEIGHT // 2 + Sizes.ROAD_WIDTH // 4
        elif self.direction == Directions.WEST:
            self.x = Sizes.WIDTH + offset
            self.y = Sizes.HEIGHT // 2 - Sizes.ROAD_WIDTH // 4

    def set_turn_direction(self):
        if self.turn == TurnState.TURNING:
            if self.direction in [Directions.NORTH, Directions.SOUTH]:
                self.turn_direction = random.choice([Directions.EAST, Directions.WEST])
            else:
                self.turn_direction = random.choice([Directions.NORTH, Directions.SOUTH])

    def calculate_turn_radius(self):
        if self.direction == [Directions.NORTH, Directions.SOUTH]:
            return Sizes.ROAD_WIDTH // 2
        return Sizes.ROAD_WIDTH // 2

    def update_turn(self):
        if self.turn != TurnState.TURNING or self.turn_progress >= 90:
            self.turn = TurnState.COMPLETED
            return
        
        radius = self.calculate_turn_radius()
        self.angle += 3
        self.turn_progress += 3

        if self.direction == Directions.NORTH:
            if self.turn_direction == Directions.EAST:
                self.x += radius * (1 - cos(radians(self.angle)))
                self.y -= radius * sin(radians(self.angle))
            else:
                self.x -= radius * (1 - cos(radians(self.angle)))
                self.y -= radius * sin(radians(self.angle))
        elif self.direction == Directions.SOUTH:
            if self.turn_direction == Directions.EAST:
                self.x += radius * (1 - cos(radians(self.angle)))
                self.y += radius * sin(radians(self.angle))
            else:
                self.x -= radius * (1 - cos(radians(self.angle)))
                self.y += radius * sin(radians(self.angle))
        elif self.direction == Directions.EAST:
            if self.turn_direction == Directions.NORTH:
                self.x += radius * (1 - cos(radians(self.angle)))
                self.y -= radius * sin(radians(self.angle))
            else:
                self.x += radius * (1 - cos(radians(self.angle)))
                self.y += radius * sin(radians(self.angle))
        elif self.direction == Directions.WEST:
            if self.turn_direction == Directions.NORTH:
                self.x -= radius * (1 - cos(radians(self.angle)))
                self.y -= radius * sin(radians(self.angle))
            else:
                self.x -= radius * (1 - cos(radians(self.angle)))
                self.y += radius * sin(radians(self.angle))

    def move(self, delta_time, light_state):
        if light_state != Colors.GREEN:
            self.waiting_time += delta_time
            self.waiting = True
            return
        self.waiting = False
        self.total_wait += self.waiting_time
        self.waiting_time = 0.0

        if self.turn == TurnState.TURNING:
            self.update_turn()
        else:
            if self.direction == Directions.NORTH:
                self.y -= Sizes.CAR_SPEED
            elif self.direction == Directions.SOUTH:
                self.y += Sizes.CAR_SPEED
            elif self.direction == Directions.EAST:
                self.x += Sizes.CAR_SPEED
            elif self.direction == Directions.WEST:
                self.x -= Sizes.CAR_SPEED

        if self.should_initiate_turn():
            self.turn = TurnState.TURNING

    def should_initiate_turn(self):
        buffer = 20
        intersection_center = (Sizes.WIDTH // 2, Sizes.HEIGHT // 2)
        return (
            abs(self.x - intersection_center[0]) < buffer and
            abs(self.y - intersection_center[1]) < buffer
        )

    def is_off_screen(self):
        return any([
            self.x < -Sizes.CAR_SIZE * 3,
            self.x > Sizes.WIDTH + Sizes.CAR_SIZE * 3,
            self.y < -Sizes.CAR_SIZE * 3,
            self.y > Sizes.HEIGHT + Sizes.CAR_SIZE * 3
        ])
