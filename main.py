import pygame
import random
from model.crosswalk import Crosswalk
from utils.colors import Colors
from utils.sizes import Sizes
from utils.directions import Directions
from model.car import Car
from model.traffic_light import TrafficLight
from model.road import Road


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
    pygame.init()
    screen = pygame.display.set_mode((Sizes.WIDTH, Sizes.HEIGHT))
    pygame.display.set_caption("Traffic Simulation")
    clock = pygame.time.Clock()

    Roads = {
        Directions.NORTH: Road(Directions.NORTH, TrafficLight(Directions.NORTH, "assets/images/light_north.png"), Crosswalk(Directions.NORTH, "assets/images/crosswalk_north.png"), "assets/images/road_north.png"),
        Directions.SOUTH: Road(Directions.SOUTH, TrafficLight(Directions.SOUTH, "assets/images/light_south.png"), Crosswalk(Directions.SOUTH, "assets/images/crosswalk_south.png"), "assets/images/road_south.png"),
        Directions.EAST: Road(Directions.EAST, TrafficLight(Directions.EAST, "assets/images/light_east.png"), Crosswalk(Directions.EAST, "assets/images/crosswalk_east.png"), "assets/images/road_east.png"),
        Directions.WEST: Road(Directions.WEST, TrafficLight(Directions.WEST, "assets/images/light_west.png"), Crosswalk(Directions.WEST, "assets/images/crosswalk_west.png"), "assets/images/road_west.png")
    }
    car_spawn_prob_distributions = {
        Directions.NORTH: lambda: random.random() < 0.02,
        Directions.SOUTH: lambda: random.random() < 0.015,
        Directions.EAST: lambda: random.random() < 0.01,
        Directions.WEST: lambda: random.random() < 0.005,
    }

    # # Intersection blocks rects
    # block_width = Sizes.ROAD_WIDTH // 2
    # block_north_west = pygame.Rect(
    #     road_west_rect.right, road_north_rect.bottom, block_width, block_width)
    # block_north_east = pygame.Rect(
    #     road_east_rect.left - block_width, road_north_rect.bottom, block_width, block_width)
    # block_south_west = pygame.Rect(
    #     road_west_rect.right, road_south_rect.top - block_width, block_width, block_width)
    # block_south_east = pygame.Rect(
    #     road_east_rect.left - block_width, road_south_rect.top - block_width, block_width, block_width)

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

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


        current_time = pygame.time.get_ticks()
        delta_time = clock.tick(Sizes.FPS) / 1000

        # Handle traffic light changes
        if current_time - last_phase_change > phases[current_phase][2]:
            last_phase_change = current_time # Reset timer
            current_phase = (current_phase + 1) % len(phases)
            # Update traffic light states
            for road in Roads.values():
                if road.direction in [Directions.NORTH, Directions.SOUTH]:
                    road.traffic_light.state = phases[current_phase][0]
                else:
                    road.traffic_light.state = phases[current_phase][1]

        # Spawn cars
        for road in Roads.values():
            if car_spawn_prob_distributions[road.direction]():
                available_lanes = road.get_available_lanes(cars)
                if available_lanes:
                    chosen_lane = random.choice(available_lanes)
                    new_car = Car(road, chosen_lane)
                    cars.append(new_car)
                    road.last_spawn = pygame.time.get_ticks()

        # Update cars
        for car in cars:
            light_state = car.road.traffic_light.state
            car.update_position(delta_time, light_state, cars)

            if car.out_of_bounds():
                cars.remove(car)


        # Draw background
        screen.fill(Colors.GRAY)

        # Draw roads and traffic lights
        for road in Roads.values():
            road.draw(screen)
            road.traffic_light.draw(screen)
            road.crosswalk.draw(screen)

        # Draw cars
        for car in cars:
            car.draw(screen)



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
