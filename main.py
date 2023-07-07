import pygame
from config import Config
from camera import Camera
from level import Level

pygame.init()

screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))

level = Level('data/levels/1.txt', screen)

pygame.quit()
