from pygame import Vector2 as Vector
import pygame
from config import Config
from rat import Rat
from player import Player
from cheese import Cheese
from bodies import Bodies
from camera import Camera
from tile import Tile

class Level:
    """
    Classe responsável por ler e interpretar os dados de um nível do jogo.
    """
    def __init__(self, filename: str, screen):
        self.screen = screen
        self.camera = Camera(Vector(0, 0))
        self.dt = 0
        self.bodies = Bodies()
        self.tilemap = []
        self.clock = pygame.time.Clock()
        self.read(filename)
        self.run()

    def read(self, filename: str):
        # Abrir o arquivo para leitura, ler as linhas do arquivo e separá-las em uma lista
        f = open(filename, 'r')
        lines = f.read().split('\n')

        # Extrair as dimensões do nível (número de linhas e colunas)
        n, m = [int(x) for x in lines[0].split()]
        lines.pop(0)

        for i in range(n): # Percorrer cada linha do nível
            self.tilemap.append([])
            for j in range(m): # Percorrer cada caractere da linha
                ch = lines[i][j]

                # Verificar o caractere e adicionar o tipo correspondente à grade
                if ch == '#':
                    pos = Vector(j * Config.BLOCK_SIZE, Config.SCREEN_HEIGHT - (n - i) * Config.BLOCK_SIZE)
                    self.bodies.append(Tile(pos, self.camera, j))
                    self.tilemap[i].append(1)
                else:
                    self.tilemap[i].append(0)

                # Verificar o caractere e adicionar um corpo correspondente
                if ch == 'E':
                    pos = Vector(j * Config.BLOCK_SIZE, Config.SCREEN_HEIGHT - (n - i) * Config.BLOCK_SIZE)
                    self.bodies.append(Rat(pos, Rat.COLOR))
                elif ch == 'S':
                    pos = Vector(j * Config.BLOCK_SIZE, Config.SCREEN_HEIGHT - (n - i) * Config.BLOCK_SIZE)
                    player = Player(pos)
                elif ch == 'C':
                    pos = Vector(j * Config.BLOCK_SIZE+(Config.BLOCK_SIZE-Cheese.WIDTH)/2, Config.SCREEN_HEIGHT - (n - i) * Config.BLOCK_SIZE+Config.BLOCK_SIZE-Cheese.HEIGHT)
                    self.bodies.append(Cheese(pos))

        # Adicionar o corpo do jogador à lista de corpos
        self.bodies.append(player)
        self.player = player
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.screen.fill(Config.SCREEN_COLOR)
            keys = pygame.key.get_pressed() # Captura das teclas pressionadas pelo jogador
        
            # Verificação das teclas de movimentação do jogador
            if keys[pygame.K_w]:
                self.player.jump()
            if keys[pygame.K_a] and not keys[pygame.K_d]:
                self.player.move_left()
            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                self.player.move_right()

            # Atualização e desenho de todos os corpos presentes no jogo
            self.bodies.update(self.dt)
            self.bodies.draw(self.screen, self.camera)

            # Atualização da posição da câmera para seguir o jogador
            self.camera.pos.x = min(max(0, self.player.pos.x - Config.SCREEN_WIDTH / 2), len(self.tilemap[0]) * Config.BLOCK_SIZE - Config.SCREEN_WIDTH)

            # Atualização da tela e controle de FPS
            pygame.display.flip()
            self.dt = self.clock.tick(60)

