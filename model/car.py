import random
import pygame
import math
from utils.colors import Colors
from utils.sizes import Sizes
from utils.directions import Directions


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

        self.speed = random.uniform(25, 60)
        self.deceleration_rate = random.uniform(10, 15)
        self.acceleration_rate = random.uniform(0.5, 1.5)
        self.angle = self.calculate_rotation()
        self.awareness_rect_image = pygame.image.load(
            "assets/images/awareness_rect.png").convert_alpha()
        self.awareness_rect = self.get_awareness_rect()

    def calculate_rotation(self):
        return {
            Directions.NORTH: 90,
            Directions.EAST: 0,
            Directions.SOUTH: 270,
            Directions.WEST: 180
        }[self.road.direction]

    def get_awareness_rect(self):
        self.awareness_rect_image = pygame.transform.rotate(self.awareness_rect_image, self.angle)
        return self.awareness_rect_image.get_rect(center = self.rect.center)

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

        # find relevant car information
        stop_at_light = self.need_to_stop_at_light(light_state)
        stop_car_ahead = self.need_to_stop_car_ahead(cars)
        stop_for_priority = self.need_to_stop_priority(cars)
        car_across = self.car_across(cars)
        # stop_for_turn = self.need_to_stop_for_turn()

        # initialize default speed
        # self.speed = self.normal_speed

        # decision logic
        if stop_at_light or stop_car_ahead or stop_for_priority:
            self.hit_breaks(dt)

        # movement handeling
        else:
            self.speed += self.acceleration_rate
            self.waiting = False
            self.waiting_time = 0.0

        if car_across:
            # self.hit_breaks(dt)
            self.maneuver(dt)

        if self.speed > 0 :
            # update position based on direction using current speed
            if self.road.direction == Directions.NORTH:
                self.rect.y += self.speed * dt
            elif self.road.direction == Directions.SOUTH:
                self.rect.y -= self.speed * dt
            elif self.road.direction == Directions.EAST:
                self.rect.x -= self.speed * dt
            else: # west
                self.rect.x += self.speed * dt

    def maneuver(self, dt):
        # self.hit_breaks(dt)
        if self.road.direction == Directions.NORTH:
            turn_amount = 45
            self.angle = self.angle - turn_amount
            angle_rad = math.radians(self.angle)
            self.rect.x += math.sin(angle_rad) * self.speed * dt
            self.rect.y -= math.cos(angle_rad) * self.speed * dt

    def car_across(self, cars):
        for car in cars:
            if car is not self and self.road is not car.road:
                if self.awareness_rect.colliderect(car.rect):
                    return True


    def hit_breaks(self, dt):
        if self.speed > 0:
            self.speed -= self.deceleration_rate
        else:
            self.speed = 0
            self.waiting = True
            self.waiting_time += dt

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

    def need_to_stop_car_ahead(self, cars):
        for car in cars:
            if car.road == self.road and car.lane == self.lane and car is not self:
                if self.road.direction == Directions.NORTH:
                    if self.awareness_rect.collidepoint(car.awareness_rect.midtop):
                        return True
                elif self.road.direction == Directions.SOUTH:
                    if self.awareness_rect.collidepoint(car.awareness_rect.midbottom):
                        return True
                elif self.road.direction == Directions.EAST:
                    if self.awareness_rect.collidepoint(car.awareness_rect.midright):
                        return True
                elif self.road.direction == Directions.WEST:
                    if self.awareness_rect.collidepoint(car.awareness_rect.midleft):
                        return True

    def need_to_stop_priority(self, cars):
        if self.rect.colliderect(self.road.after_immediate):
            # if self.road.traffic_light.state == Colors.RED:
                if self.car_across(cars):
                    return True

    def out_of_bounds(self):
        return not self.rect.colliderect(0, 0, Sizes.WIDTH, Sizes.HEIGHT)

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=self.rect.center)
        self.awareness_rect = self.awareness_rect_image.get_rect(center=self.rect.center)
        screen.blit(rotated, rect.topleft)
        screen.blit(self.awareness_rect_image, self.awareness_rect)
