from pygame import Vector2 as Vector
from abc import ABC, abstractmethod
from hitbox import Hitbox
from collision import Collision

class Body(ABC):
    """
    Classe abstrata que representa um objeto com posição e velocidade.
    Essa classe é projetada para ser herdada por outros objetos do jogo.
    """

    def __init__(self, pos: Vector, width, height):
        self.velocity = Vector(0, 0) # Velocidade inicial zero
        self.width = width
        self.height = height
        self.falling = False
        self.pos = pos
        self.kill = False
        
    @property
    def pos(self): # Getter: Retorna a posição atual do objeto.
        return self._pos
    
    @pos.setter
    def pos(self, pos): # Setter: Define a posição do objeto.
        self._pos = pos
        # Atualiza a hitbox do objeto
        self.hitbox = Hitbox(pos, self.width, self.height)
        # Verifica se a velocidade horizontal é maior que zero
        if self.velocity.x > 0:
            # Reduz gradualmente a velocidade horizontal com um limite mínimo de 0)
            self.velocity.x = max(self.velocity.x - 0.1, 0) 
        elif self.velocity.x < 0:
            self.velocity.x = min(self.velocity.x + 0.1, 0)


    
    @abstractmethod
    def draw(self, screen, camera):
        """
        Método responsável por desenhar o objeto na tela.
        Esse método deve ser implementado nas classes filhas.
        """
        pass

    @abstractmethod
    def collide(self, c):
        """
        Método responsável por tratar a colisão do objeto.
        Esse método deve ser implementado nas classes filhas.
        """
        pass

    @abstractmethod
    def update(self, dt, bodies):
        """
        Método responsável por atualizar o objeto na tela.
        Esse método deve ser implementado nas classes filhas.
        """
        pass

    @abstractmethod
    def damage(self, body, direction):
        """
        Método responsável por calcular o dano aplicado dano ao objeto.
        """
        pass

    @abstractmethod
    def rebound(self, body, direction):
        """
        Método responsável por calcular o impulso aplicado ao objeto.
        """
        pass
