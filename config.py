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
    RAT_LEFT = pygame.transform.scale(pygame.image.load('imgs/ratin_left.png'), (BLOCK_SIZE,BLOCK_SIZE))
    RAT_RIGHT = pygame.transform.scale(pygame.image.load('imgs/ratin_right.png'), (BLOCK_SIZE,BLOCK_SIZE))

    # Configuração da fonte
    font = pygame.font.SysFont("arialblacomicck", 40)
    COR_FONTE = (255, 255, 255)
    COR_FUNDO_TEXTO = (0, 0, 0)