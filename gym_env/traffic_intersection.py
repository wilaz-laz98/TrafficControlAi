import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
# window title
pygame.display.set_caption('Traffic control')
# running speed
clock = pygame.time.Clock()

#generic square surface
car = pygame.Surface((20,30))
car.fill('Grey')
car_x_pos = 600
car_y_pos = 200

# image surface
# surface = pygame.image.load('path')

# text surface
# font = pygame.font.Font(fonttype, size)
# surface = font.render('text', antialais(true or flase), 'color')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draw all elements
    car_x_pos -= 1
    # car_y_pos -= 1
    screen.blit(car, (car_x_pos, car_y_pos))

    # update everything
    pygame.display.update()
    clock.tick(60) # 60fps
