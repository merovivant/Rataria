import pygame
from config import Config
from body import Body
from player import Player


class Cheese(Body):
    WIDTH = 62.1052632
    HEIGHT = 40

    def __init__(self, pos):
        super().__init__(pos, Cheese.WIDTH, Cheese.HEIGHT)
        self.image = pygame.transform.scale(pygame.image.load('imgs/cheese.png'), (self.width,self.height))

    def draw(self, screen, camera):
        pos_x = self.pos.x - camera.pos.x #Calcula a posição inicial
        if pos_x < -40 or pos_x > Config.SCREEN_WIDTH + 40: return #Verifica se o queijo está fora da tela

        pos = pygame.Vector2(pos_x, self.pos.y)
        screen.blit(self.image, (pos.x, pos.y))

        from pygame.draw import rect
        rect(screen, (255,0,0), (self.hitbox.SE.x, self.hitbox.SE.y, self.width, self.height), 1)

    def damage(self, body, *args):
        if isinstance(body, Player):
            body.cheese += 1
        return 0
    
    def rebound(*args):
        return -0.5

    def collide(self, *args):
        self.kill = True

    def update(self, *args): pass       