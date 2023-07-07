import pygame
from pygame.locals import *
from math import floor

class Leitor():
    """
    Interface para leitura e processamento de imagens contidas em jpg's
    """
    
    # Processamento de spritesheet.
    
    @staticmethod
    def get_image_by_gid(spritesheet, gid, columns, largura, altura, 
                         spc_h=0, spc_v=0, margem_left=0, margem_top=0):
        gid = floor(gid)
        linha = gid // columns
        coluna = gid % columns
        x = margem_left + (coluna * (largura + spc_h))
        y = margem_top + (linha * (altura + spc_v))
        return pygame.Surface.subsurface(spritesheet, (x, y), (largura, altura))