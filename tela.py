
import pygame
from config import Config
from level import Level

# Enum usado para diferenciar em qual modo o jogo está
class Tela():    

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.level = ''
        self.keys = None
    
    @property # Getter para as teclas pressionadas
    def keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        return pygame.key.get_pressed()
    
    @keys.setter # Setter para as teclas pressionadas
    def keys(self, value):
        self._keys = value

    def screen_update(self):
        pygame.display.flip()

    
    def menu_inicial(self, **kwargs):
        while not self.keys[pygame.K_SPACE]:
            # Exibo a tela de título
            self.screen.blit(Config.menu1_jpg, (0,0))
            # Exibo a mensagem para pressionar espaço
            pygame.draw.rect(self.screen, Config.CINZA, (359, 432+20, 516, 56))
            pygame.draw.rect(self.screen, Config.PRETO, (362, 435+20, 510, 50))
            Config.draw_text(self.screen, "Pressione ESPAÇO para iniciar", Config.font, Config.CINZA, 410, 450+20)
            # Caso o usuaŕio pressione espaço o programa segue para o menu principal
            self.screen_update()
        return self.menu_principal()

    def menu_principal(self, **kwargs):
        # Exibo o plano de fundo
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            self.screen.blit(Config.menu2_jpg, (0,0))
            # Botões exibidos na tela 
            if Config.botao_campanha.draw(self.screen):
                return self.campanha()
            elif Config.botao_arcade.draw(self.screen):
                Config.nomeJogador = ""
                return self.inserirNome()
            elif Config.botao_leaderboard.draw(self.screen):
                return self.leaderboardTela()
            elif Config.botao_sair.draw(self.screen):
                pygame.quit()
                raise SystemExit
            self.screen_update()

    '''
    TODO AQUI FICA O MODO INFINITO
    '''

    def arcade(self,**kwargs):
        level = Level('data/levels/ARCADE.txt')
        level.run_arcade(self)
        return self.menu_principal()

    '''
    TODO AQUI FICA O MODO ONDE TEM AS FASES
    '''
    def morte(self,**kwargs):
        while not self.keys[pygame.K_SPACE]:
            pygame.draw.rect(self.screen, Config.BRANCO, (359, 432, 516, 56))
            pygame.draw.rect(self.screen, Config.PRETO, (362, 435, 510, 50))
            Config.draw_text(self.screen, "Pressione ESPAÇO para reiniciar", Config.font, Config.CINZA, 362, 435+20)     
            self.screen_update()   
        return self.campanha()


    def campanha(self, **kwargs):
        level = Level('data/levels/1.txt')
        level.run_campanha(self)
        return self.morte()
    
    def leaderboardTela(self,**kwargs):
        while not self.keys[pygame.K_ESCAPE]:
            self.screen.blit(Config.leaderboardFUNDO_jpg, (0,0))# Exibo o plano de fundo
            # Caso seja pressionado a tecla ESC ou clicado o botão de volar na tela
            # a tela é direcionada para o menu principal
            if Config.botao_back.draw(self.screen): break
            self.leaderboard.draw(self.screen) 
            self.screen_update()   
        return self.menu_principal()
    
    def inserirNome(self,**kwargs):
        while True:
            charLido = ''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN:
                        charLido = event.unicode
                    else:
                        charLido = '$'
            if any(self.keys):
                # Caso seja pressionada a tecla ENTER com algum input escrito a tela é
                # transferida para o modo arcade
                if self.keys[pygame.K_RETURN] and len(Config.nomeJogador) > 0:
                    Config.pontosJogador = 0
                    return self.arcade()
                # Caso seja pressionada a tecla de BACKSPACE é retirado um caratere do input
                elif self.keys[pygame.K_BACKSPACE] and len(Config.nomeJogador) > 0:
                    Config.nomeJogador = Config.nomeJogador[:-1]
                elif charLido != '$' and len(Config.nomeJogador) < 7:
                    Config.nomeJogador += charLido

            # Preencho tela de preto
            self.screen.fill(Config.PRETO)

            # Fazer o texto que pede para inserir o nome
            text_surface = pygame.font.Font(None, 60).render("Insira seu nome:", True, Config.BRANCO)
            self.screen.blit(text_surface, (340, 250))

            # Fazer a caixa de texto
            pygame.draw.rect(self.screen, Config.BRANCO, Config.input_box, 2)

            # Inserir dentro da caixa de texto o input do nome do jogador
            input_text = pygame.font.Font(None, 60).render(Config.nomeJogador, True, Config.BRANCO)
            self.screen.blit(input_text, (Config.input_box.x + 10, Config.input_box.y + 10))

            # Caso clicado o botão enter da tela o nome é lido e a tela é 
            # transferida para o modo arcade
            if Config.botao_enter.draw(self.screen) and len(Config.nomeJogador) > 0:
                Config.pontosJogador = 0
                return self.arcade()
            self.screen_update()
        