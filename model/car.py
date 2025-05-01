import random
import pygame
import math
from utils.colors import Colors
from utils.sizes import Sizes
from utils.directions import Directions
from utils.turn_state import TurnState


class Car:
    def __init__(self, road, lane):
        self.road = road
        self.target_road = self.get_target_road()

        self.lane = lane

        self.image = pygame.image.load("assets/images/car.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.get_initial_position())
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

        self.waiting_time = 0.0
        self.total_wait = 0.0
        self.waiting = False

        self.turn_progress = 0
        self.speed = random.uniform(100, 200)
        self.angle = self.calculate_rotation()

    def calculate_rotation(self):
        return {
            Directions.NORTH: 90,
            Directions.EAST: 0,
            Directions.SOUTH: 270,
            Directions.WEST: 180
        }[self.road.direction]

    def get_initial_position(self):
        return self.road.spawn_positions[self.lane]

    def get_opposite_direction(self):
        return {
            Directions.NORTH: Directions.SOUTH,
            Directions.SOUTH: Directions.NORTH,
            Directions.EAST: Directions.WEST,
            Directions.WEST: Directions.EAST
        }[self.road.direction]

    def get_target_road(self):
        # 70% straight, 30% turn right
        if random.random() < 0.7:
            return self.get_opposite_direction()
        return random.choice([d for d in Directions if d not in
                            (self.road.direction, self.get_opposite_direction())])

    def update_position(self, dt, light_state, cars):
        # store normal speed if not already set
        if not hasattr(self, 'normal_speed'):
            self.normal_speed = self.speed

        # find relevant car ahead information
        car_ahead, axial_distance = self.get_closest_car_ahead(cars)
        stop_at_light = self.need_to_stop_at_light(light_state)

        # initialize default speed
        self.speed = self.normal_speed

        # decision logic
        if stop_at_light:
            self.speed = 0
            self.waiting = True
            self.waiting_time += dt
        elif car_ahead:
            # dynamic speed adjustment for moving car
            safe_distance = 30
            if axial_distance < safe_distance:
                # reduce speed proportionally to distance
                speed_reduction = (safe_distance - axial_distance)/ safe_distance
                self.speed = max(0,self.normal_speed * (1-speed_reduction))
                self.speed = min(self.speed, car_ahead.speed)

        # movement handeling
        self.waiting = False
        self.waiting_time = 0.0

        if self.speed > 0 :
            # update position based on direction using current speed
            if self.road.direction == Directions.NORTH:
                self.rect.y += self.speed * dt
            elif self.road.direction == Directions.SOUTH:
                self.rect.y -= self.speed * dt
            elif self.road.direction == Directions.EAST:
                self.rect.x -= self.speed * dt
            else: #west
                self.rect.x += self.speed * dt

    def get_closest_car_ahead(self, cars):
        closest_car = None
        min_distance = float('inf')

        for car in cars:
            if (car is self or
                car.road != self.road or
                car.lane != self.lane or
                not self.is_ahead(car)):
                continue

            distance = self.calculate_axial_distance_to(car)
            if distance < min_distance:
                min_distance = distance
                closest_car = car
        return closest_car, min_distance

    def is_ahead(self, other_car):
        if self.road.direction == Directions.NORTH:
            return other_car.rect.centery > self.rect.centery
        elif self.road.direction == Directions.SOUTH:
            return other_car.rect.centery < self.rect.centery
        elif self.road.direction == Directions.EAST:
            return other_car.rect.centerx < self.rect.centerx
        elif self.road.direction == Directions.WEST:
            return other_car.rect.centerx > self.rect.centerx

    def calculate_axial_distance_to(self, other_car):
        if self.road.direction in [Directions.NORTH, Directions.SOUTH]:
            return abs(self.rect.centery - other_car.rect.centery)
        else:
            return abs(self.rect.centerx - other_car.rect.centerx)

    def need_to_stop_at_light(self, light_state):
        if light_state != Colors.RED or not self.rect.colliderect(self.road.rect):
            return False

        stop_distance = 10
        if self.road.direction == Directions.NORTH:
            return self.rect.bottom > (self.road.stop_line - stop_distance)
        elif self.road.direction == Directions.SOUTH:
            return self.rect.top < (self.road.stop_line + stop_distance)
        elif self.road.direction == Directions.EAST:
            return self.rect.left < (self.road.stop_line + stop_distance)
        elif self.road.direction == Directions.WEST:
            return self.rect.right > (self.road.stop_line - stop_distance)

    def out_of_bounds(self):
        return not self.rect.colliderect(0, 0, Sizes.WIDTH, Sizes.HEIGHT)

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=self.rect.center)
        screen.blit(rotated, rect.topleft)
