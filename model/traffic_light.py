import pygame
from utils.colors import Colors
from utils.sizes import Sizes
from utils.directions import Directions


class TrafficLight:
    def __init__(self, direction, image):
        self.direction = direction
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

        if self.direction in [Directions.NORTH, Directions.SOUTH]:
            self.state = Colors.RED
        elif self.direction in [Directions.EAST, Directions.WEST]:
            self.state = Colors.GREEN


    # def set_position(self):
    #     # Set the position of the traffic light based on its direction
    #     if self.direction == Directions.NORTH:
    #         self.rect.topleft = (Sizes.WIDTH // 2 - Sizes.ROAD_WIDTH // 2 - Sizes.TRAFFIC_LIGHT_WIDTH - 30, Sizes.ROAD_HEIGHT - Sizes.TRAFFIC_LIGHT_HEIGHT - 30)
    #     elif self.direction == Directions.SOUTH:
    #         self.rect.topleft = (Sizes.WIDTH // 2 + Sizes.ROAD_WIDTH // 2 + 30, Sizes.HEIGHT // 2 + Sizes.ROAD_WIDTH // 2 + 30)
    #     elif self.direction == Directions.EAST:
    #         self.rect.topleft = (Sizes.WIDTH // 2 + Sizes.ROAD_WIDTH // 2 + 30, Sizes.HEIGHT // 2 - Sizes.ROAD_WIDTH // 2 - Sizes.TRAFFIC_LIGHT_WIDTH - 30)
    #     elif self.direction == Directions.WEST:
    #         self.rect.topleft = (Sizes.WIDTH // 2 - Sizes.ROAD_WIDTH // 2 - Sizes.TRAFFIC_LIGHT_HEIGHT - 30, Sizes.HEIGHT // 2 + Sizes.ROAD_WIDTH // 2 + Sizes.TRAFFIC_LIGHT_WIDTH)

    def draw(self, screen):
        # Update traffic color based on state
        screen.blit(self.image, self.rect)
        if self.direction == Directions.NORTH:
            # Define circle positions relative to the traffic light
            positions = [(11, 65), (11, 40), (11, 15)]
            # Draw circles based on state
            if self.direction == Directions.NORTH:
                colors = [Colors.GREEN, Colors.YELLOW, Colors.RED]
                for i, color in enumerate(colors):
                    pygame.draw.circle(self.image, color if self.state == color else (
                        50, 50, 50), positions[i], 8)  # Gray when inactive

        elif self.direction == Directions.SOUTH:
            # Define circle positions relative to the traffic light
            positions = [(11, 15), (11, 40), (11, 65)]
            # Draw circles based on state
            if self.direction == Directions.SOUTH:
                colors = [Colors.GREEN, Colors.YELLOW, Colors.RED]
                for i, color in enumerate(colors):
                    pygame.draw.circle(self.image, color if self.state == color else (
                        50, 50, 50), positions[i], 8)
        elif self.direction == Directions.EAST:
            # Define circle positions relative to the traffic light
            positions = [(15, 11), (40, 11), (65, 11)]
            # Draw circles based on state
            if self.direction == Directions.EAST:
                colors = [Colors.GREEN, Colors.YELLOW, Colors.RED]
                for i, color in enumerate(colors):
                    pygame.draw.circle(self.image, color if self.state == color else (
                        50, 50, 50), positions[i], 8)
        elif self.direction == Directions.WEST:
            # Define circle positions relative to the traffic light
            positions = [(65, 11), (40, 11), (15, 11)]
            # Draw circles based on state
            if self.direction == Directions.WEST:
                colors = [Colors.GREEN, Colors.YELLOW, Colors.RED]
                for i, color in enumerate(colors):
                    pygame.draw.circle(self.image, color if self.state == color else (
                        50, 50, 50), positions[i], 8)
