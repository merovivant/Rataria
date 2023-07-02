import pygame
from config import Config
from rat import Rat
from player import Player
from cheese import Cheese
from tile import Tile
from tilemap import Tilemap
from camera import Camera
from random import random
from leaderboard import Leaderboard

class Level:
    """
    Classe responsável por ler e interpretar os dados de um nível do jogo.
    """
    def __init__(self, filepath):
        self.tilemap = []
        self.player = None
        self.bodies = []
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.camera = Camera(pygame.Vector2(0, 0))
        self.leaderboard = Leaderboard("data/leaderboardPlacar.txt")
        self.read(filepath)

    def read(self, filename: str):
        # Abrir o arquivo para leitura, ler as linhas do arquivo e separá-las em uma lista
        f = open(filename, 'r')
        lines = f.read().split('\n')
        # Extrair as dimensões do nível (número de linhas e colunas)
        n, m = [int(x) for x in lines[0].split()]
        lines.pop(0)
        grid = [] # Inicializar listas vazias para armazenar os corpos e a grade do nível

        for i in range(n): # Percorrer cada linha do nível
            grid.append([])
            for j in range(m): # Percorrer cada caractere da linha
                ch = lines[i][j]
                # Verificar o caractere e adicionar o tipo correspondente à grade
                if ch == '#':
                    grid[i].append(Tile.GROUND)
                else:
                    grid[i].append(Tile.NONE)
                # Verificar o caractere e adicionar um corpo correspondente
                if ch == 'E':
                    self.bodies.append(Rat(Config.RAT_COLOR, pygame.Vector2(j * Config.BLOCK_SIZE, Config.SCREEN_HEIGHT - (n - i) * Config.BLOCK_SIZE)))
                elif ch == 'S':
                    self.player = Player(pygame.Vector2(j * Config.BLOCK_SIZE, Config.SCREEN_HEIGHT - (n - i) * Config.BLOCK_SIZE))
                elif ch == 'C':
                    self.bodies.append(Cheese(pygame.Vector2(j * Config.BLOCK_SIZE+ 0.1118*Config.BLOCK_SIZE , Config.SCREEN_HEIGHT - (n - i) * Config.BLOCK_SIZE+0.5*Config.BLOCK_SIZE )))
        # Criar um objeto Tilemap a partir da grade lida
        self.tilemap = Tilemap(grid)

        # Adicionar o corpo do jogador e o tilemap à lista de corpos
        self.bodies.append(self.player)
        self.bodies.append(self.tilemap)
        Cheese.many_collected = 0  

    def run_arcade(self, tela):
        while not self.player.dead:
            cooldownLeft = 0
            cooldownRight = 0
            tela.screen.fill(Config.SCREEN_COLOR) # Preenchimento da tela com uma cor de fundo    

            # Gera os inimigos na esquerda e na direta em tempo aleatorio respeitando o cooldown
            
            if random() < ((1.0/60.0)*0.6) and cooldownLeft >= 0:
                self.bodies.insert(0,Rat(Config.RAT_COLOR, pygame.Vector2(0, 480), True))   
            if random() < ((1.0/60.0)*0.6)and cooldownRight >= 0:
                cooldownRight = 240
                self.bodies.insert(0,Rat(Config.RAT_COLOR, pygame.Vector2(5040, 480), False))
            # Diminuiu em um frame o tempo de cooldown
            cooldownLeft -= 1
            cooldownRight -= 1

            if tela.keys[pygame.K_ESCAPE]:
                return tela.menu_principal()
            # Captura do input do jogador
            if tela.keys[pygame.K_w]:
                self.player.jump()
            if tela.keys[pygame.K_a] and not tela.keys[pygame.K_d]:
                self.player.move_left()
            elif tela.keys[pygame.K_d] and not tela.keys[pygame.K_a]:
                self.player.move_right()
            self.tilemap.draw(tela.screen, self.camera) # Desenho do tilemap na tela, levando em consideração a câmera
            
            # Atualização e desenho de todos os corpos presentes no jogo
            for body in self.bodies:
                body.update(self.dt, self.bodies)
                body.draw(tela.screen, self.camera)
            
            # Atualização da posição da câmera para seguir o jogador
            self.camera.pos.x = min(max(0, self.player.pos.x - Config.SCREEN_WIDTH / 2), self.tilemap.m * Config.BLOCK_SIZE - Config.SCREEN_WIDTH)
            # Desenha o contador de vidas
            tela.screen.blit(Config.LIFE(self.player.lives), (15,10))
            
            # Desenha os pontos do jogador 
            Config.draw_text(tela.screen, Leaderboard.alinhado(Config.pontosJogador), Config.font2, Config.AMARELO, 1000, 40)

            tela.screen_update()
            self.dt = self.clock.tick(60)
        

        self.leaderboard.adicionarJogador(Config.nomeJogador, Config.pontosJogador)
        self.leaderboard.gravar("data/leaderboardPlacar.txt")

    def run_campanha(self, tela):
        while not self.player.dead:
            tela.screen.fill(Config.SCREEN_COLOR) # Preenchimento da tela com uma cor de fundo 

            if tela.keys[pygame.K_ESCAPE]:  # Caso seja pressionado a telca ESC, a tela volta ao menu
                return tela.menu_principal()

            # Captura do input do jogador
            if tela.keys[pygame.K_w]:
                self.player.jump()
            if tela.keys[pygame.K_a] and not tela.keys[pygame.K_d]:
                self.player.move_left()
            elif tela.keys[pygame.K_d] and not tela.keys[pygame.K_a]:
                self.player.move_right()

            self.tilemap.draw(tela.screen, self.camera) # Desenho do tilemap na tela, levando em consideração a câmera
            
            # Atualização e desenho de todos os corpos presentes no jogo
            for body in self.bodies:
                body.update(self.dt,self.bodies)
                body.draw(tela.screen, self.camera)
            
            # Atualização da posição da câmera para seguir o jogador
            self.camera.pos.x = min(max(0, self.player.pos.x - Config.SCREEN_WIDTH / 2), self.tilemap.m * Config.BLOCK_SIZE - Config.SCREEN_WIDTH)

            # Desenha o contador de vidas
            tela.screen.blit(Config.LIFE(self.player.lives), (15,10))

            #Desenha o contador de queijos
            from cheese import Cheese
            tela.screen.blit(Config.CHEESE_COUNTER, (15, 20+Config.LIFE_HEIGTH))
            Config.draw_text(tela.screen, f"{Cheese.many_collected}", Config.font, Config.BRANCO, 15+0.7*Config.CHEESE_WIDTH+10, 20+Config.LIFE_HEIGTH)

            tela.screen_update()
            self.dt = self.clock.tick(60)