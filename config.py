import pygame
import math
import leitor
from leitor import Leitor
from math import floor

class Config:
    """
    Classe que armazena configurações e constantes relacionadas ao jogo.
    Contém atributos estáticos com valores específicos.
    """

    # Configurações da tela
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    SCREEN_COLOR = '#444444'

    # Configurações dos blocos
    BLOCK_SIZE = 80
    BLOCK_COLOR = "#222222"

    # Configuração do jogador
    PLAYER_COLOR = "purple"

    # Configuração do rato
    RAT_COLOR = "blue"
    rato_direita = lambda color: pygame.image.load(f'imgs/ratos/{color}/right.png')
    rato_esquerda = lambda color: pygame.image.load(f'imgs/ratos/{color}/left.png')
    RAT_RIGHT = lambda color, indice: pygame.transform.scale(Leitor.get_image_by_gid(Config.rato_direita(color), floor(indice), 2, 65, 72) , (Config.BLOCK_SIZE,Config.BLOCK_SIZE))
    RAT_LEFT = lambda color, indice: pygame.transform.scale(Leitor.get_image_by_gid(Config.rato_esquerda(color), floor(indice), 2, 65, 72) , (Config.BLOCK_SIZE,Config.BLOCK_SIZE))

    # Configuração da fonte
    #font = pygame.font.SysFont("arialblacomicck", 40)
    COR_FONTE = (255, 255, 255)
    COR_FUNDO_TEXTO = (0, 0, 0)
