from pygame.transform import scale
from pygame.image import load
from config import Config
from body import Body, Hitbox, Vector, Collision
from leitor import Leitor

class Rat(Body):
    """
    Classe que representa todos ratos no jogo.
    É uma classe concreta que herda da classe Body.
    """
    COLOR = "purple"
    SIZE = 80

    def __init__(self, pos, color):
        super().__init__(pos, Rat.SIZE, Rat.SIZE)
        self.color = color
        self.indice = 0
        self.last_direction = 'right'

    @property
    def image(self):
        if self.last_direction == 'right':
            image = load(f'imgs/ratos/{self.color}/right.png')
            image = Leitor.get_image_by_gid(image, self.indice, 2, 65, 72)
            self.last_direction = 'right'
            return scale(image, (self.width, self.height))
        elif self.last_direction == 'left':
            image = load(f'imgs/ratos/{self.color}/left.png')
            image = Leitor.get_image_by_gid(image, self.indice, 2, 65, 72)
            self.last_direction = 'left'
            return scale(image, (self.width, self.height))
        
    @image.setter
    def image(self, image):
        self._image = image

    @property
    def indice(self):
        self.indice = self._indice + 0.0625
        return self._indice
    
    @indice.setter
    def indice(self, indice):
        if indice >= 2:
            self._indice = 0
        else: 
            self._indice = indice

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, pos):
        self._pos = pos
        # Atualiza a hitbox do objeto
        self.hitbox = Hitbox(pos, self.width, self.height)
        # Verifica se a velocidade horizontal é maior que zero
        if self.velocity.x > 0:
            # Reduz gradualmente a velocidade horizontal com um limite mínimo de 0)
            self.velocity.x = max(self.velocity.x - 0.1, 0) 
        elif self.velocity.x < 0:
            self.velocity.x = min(self.velocity.x + 0.1, 0)

    def draw(self, screen, camera):
        pos_x = self.pos.x - camera.pos.x #Calcula a posição inicial
        if pos_x < -40 or pos_x > Config.SCREEN_WIDTH + 40: return #Verifica se o rato está fora da tela
        
        pos = Vector(pos_x, self.pos.y)
        screen.blit(self.image, (pos.x, pos.y))

    def move_left(self): # Move o rato para a esquerda com base na sua velocidade atual.
        self.last_direction = 'left'
        if self.falling:
            self.velocity.x = max(self.velocity.x - 0.2, -1)
        else:
            self.velocity.x = max(self.velocity.x - 0.3, -1) 

    def move_right(self): # Move o rato para a direita com base na sua velocidade atual.
        self.last_direction = 'right'
        if self.falling:
            self.velocity.x = min(self.velocity.x + 0.2, 1)
        else:
            self.velocity.x = min(self.velocity.x + 0.3, 1)

    def jump(self): # Faz o rato pular se não estiver caindo.
        if not self.falling:
            self.velocity.y += -1.5
            self.falling = True

    def damage(self, body, direction): # Retorna o dano causado ao corpo passado como parâmetro em caso de colisão.
        if direction == Collision.TOP and isinstance(body, Rat):
            body.pos.y = self.pos.y - body.height
        if isinstance(body, Rat.PLAYER) and direction == Collision.SIDE:
            return 1
        return 0
    
    def rebound(self, body, direction): # Retorna o impulso causado ao corpo passado como parâmetro em caso de colisão        
        if isinstance(body, Rat) and direction == Collision.SIDE:
            return 1
        if isinstance(body, Rat) and direction == Collision.TOP:
            return 0.5
        return 0

    def collide(self, damage, rebound): # Trata a colisão com outro corpo.
        if damage > 0:
            self.kill = True
            self.velocity.x *= rebound.x
            self.velocity.y *= rebound.y

    def update(self, dt, bodies):
        """
        Atualiza o estado do objeto Rat com base no tempo decorrido desde a última atualização.
        Args: dt (float): Tempo decorrido desde a última atualização em segundos.
        """
        if self.kill: return
        if self.falling: # Verifica se o rato está caindo   
            self.velocity.y += 0.1 # Aumenta a velocidade vertical para simular a aceleração da gravidade
        x = self.pos.x + self.velocity.x * dt
        y = min(Config.SCREEN_HEIGHT - Config.BLOCK_SIZE, self.pos.y + self.velocity.y * dt)
        self.hitbox = Hitbox(Vector(x, y), self.width, self.height)
        if not self in bodies: #Verifica se há colisão com algum corpo
            self.pos = Vector(x, y)
        else:
            if self.falling:
                self.hitbox = Hitbox(Vector(self.pos.x, y), self.width, self.height)
                if not self in bodies:
                    self.pos = Vector(self.pos.x, y)

        self.hitbox = Hitbox(self.pos, self.width, self.height)
        bodies.verify_bellow(self) # Verifica se há colisão com algum corpo abaixo do rato

        