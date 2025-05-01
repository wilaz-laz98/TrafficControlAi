import pygame

class Crosswalk:
    def __init__(self, direction, image):
        self.direction = direction
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()


    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
