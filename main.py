import pygame
import random
from utils.colors import Colors
from utils.sizes import Sizes
from utils.directions import Directions
from model.car import Car
from model.traffic_light import TrafficLight


def draw_metrics(screen, cars):
    font = pygame.font.SysFont('Arial', 20)
    waiting_cars = sum(1 for car in cars if car.waiting)
    total_wait = sum(car.total_wait for car in cars)
    avg_wait = total_wait / len(cars) if cars else 0

    texts = [
        f"Cars waiting: {waiting_cars}",
        f"Avg wait time: {avg_wait:.1f}s",
        f"Total cars: {len(cars)}"
    ]

    y_offset = 10
    for text in texts:
        surface = font.render(text, True, (255, 255, 255))
        screen.blit(surface, (10, y_offset))
        y_offset += 25

def main():
    screen = pygame.display.set_mode((Sizes.WIDTH, Sizes.HEIGHT))
    clock = pygame.time.Clock()

    # Load road image surfaces
    road_north = pygame.image.load(
        "assets/images/road_north.png").convert_alpha()
    road_south = pygame.image.load(
        "assets/images/road_south.png").convert_alpha()
    road_east = pygame.image.load(
        "assets/images/road_east.png").convert_alpha()
    road_west = pygame.image.load(
        "assets/images/road_west.png").convert_alpha()
    # Getting roads rects
    road_north_rect = road_north.get_rect(midtop=(Sizes.WIDTH // 2, 0))
    road_south_rect = road_south.get_rect(midbottom=(Sizes.WIDTH // 2, Sizes.HEIGHT))
    road_east_rect = road_east.get_rect(midright=(Sizes.WIDTH, Sizes.HEIGHT // 2))
    road_west_rect = road_west.get_rect(midleft=(0, Sizes.HEIGHT // 2))

    # Load crosswalk images
    crosswalk_north = pygame.image.load(
        "assets/images/crosswalk_north.png").convert_alpha()
    crosswalk_south = pygame.image.load(
        "assets/images/crosswalk_south.png").convert_alpha()
    crosswalk_east = pygame.image.load(
        "assets/images/crosswalk_east.png").convert_alpha()
    crosswalk_west = pygame.image.load(
        "assets/images/crosswalk_west.png").convert_alpha()

    # Getting crosswalk rects
    crosswalk_north_rect = crosswalk_north.get_rect(midbottom=(Sizes.WIDTH // 2, Sizes.ROAD_HEIGHT))
    crosswalk_south_rect = crosswalk_south.get_rect(midtop=(Sizes.WIDTH // 2, Sizes.HEIGHT - Sizes.ROAD_HEIGHT))
    crosswalk_east_rect = crosswalk_east.get_rect(midleft=(Sizes.WIDTH - Sizes.ROAD_HEIGHT, Sizes.HEIGHT // 2))
    crosswalk_west_rect = crosswalk_west.get_rect(midright=(Sizes.ROAD_HEIGHT, Sizes.HEIGHT // 2))

    # Intersection blocks rects
    block_width = Sizes.ROAD_WIDTH // 2
    block_north_west = pygame.Rect(
        road_west_rect.right, road_north_rect.bottom, block_width, block_width)
    block_north_east = pygame.Rect(
        road_east_rect.left - block_width, road_north_rect.bottom, block_width, block_width)
    block_south_west = pygame.Rect(
        road_west_rect.right, road_south_rect.top - block_width, block_width, block_width)
    block_south_east = pygame.Rect(
        road_east_rect.left - block_width, road_south_rect.top - block_width, block_width, block_width)

    # Load traffic light images
    lights = [
        TrafficLight(Directions.NORTH, "assets/images/light_north.png"),
        TrafficLight(Directions.SOUTH, "assets/images/light_south.png"),
        TrafficLight(Directions.EAST, "assets/images/light_east.png"),
        TrafficLight(Directions.WEST, "assets/images/light_west.png")
    ]

    # Phases
    phases = [
        (Colors.RED, Colors.GREEN, 10000),
        (Colors.RED, Colors.YELLOW, 2000),
        (Colors.GREEN, Colors.RED, 10000),
        (Colors.YELLOW, Colors.RED, 2000)
    ]
    current_phase = 0
    last_phase_change = pygame.time.get_ticks()

    # Cars
    cars = []
    last_spawn = pygame.time.get_ticks()
    spawn_delay = random.randint(*Sizes.SPAWN_RANGE)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        delta_time = clock.get_time() / 1000
        current_time = pygame.time.get_ticks()
        # Handle traffic light changes
        if current_time - last_phase_change > phases[current_phase][2]:
            last_phase_change = current_time # Reset timer
            current_phase = (current_phase + 1) % len(phases)
            # Update traffic light states
            for light in lights:
                if light.direction in [Directions.NORTH, Directions.SOUTH]:
                    light.state = phases[current_phase][0]
                else:
                    light.state = phases[current_phase][1]

        # Car spawning
        if current_time - last_spawn > spawn_delay:
            cars.append(Car(random.choice(list(Directions))))
            last_spawn = current_time
            spawn_delay = random.randint(*Sizes.SPAWN_RANGE)

        # Update cars
        for car in cars:
            # Get traffic light state
            if car.direction in [Directions.NORTH, Directions.SOUTH]:
                light_state = phases[current_phase][0]
            else:
                light_state = phases[current_phase][1]

            car.move(delta_time, light_state)
            # Check if car is out of bounds
            if car.is_off_screen():
                cars.remove(car)

        # Draw background
        screen.fill(Colors.GRAY)

        # Draw roads
        screen.blit(road_north, road_north_rect)
        screen.blit(road_south, road_south_rect)
        screen.blit(road_east, road_east_rect)
        screen.blit(road_west, road_west_rect)


        # Draw crosswalks
        screen.blit(crosswalk_north, crosswalk_north_rect)
        screen.blit(crosswalk_south, crosswalk_south_rect)
        screen.blit(crosswalk_east, crosswalk_east_rect)
        screen.blit(crosswalk_west, crosswalk_west_rect)

        # Draw cars
        for car in cars:
            pygame.draw.rect(screen, car.color, (car.x, car.y,
                             Sizes.CAR_SIZE, Sizes.CAR_SIZE))

        # Draw traffic lights
        for light in lights:
            light.draw(screen)

        # Draw metrics
        draw_metrics(screen, cars)


        # # Draw intersection blocks
        # pygame.draw.rect(screen, Colors.BLACK, block_north_west)
        # pygame.draw.rect(screen, Colors.BLACK, block_north_east)
        # pygame.draw.rect(screen, Colors.BLACK, block_south_west)
        # pygame.draw.rect(screen, Colors.BLACK, block_south_east)


        pygame.display.flip()
        clock.tick(Sizes.FPS)


if __name__ == "__main__":
    pygame.init()
    main()
