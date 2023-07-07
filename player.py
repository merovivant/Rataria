from rat import Rat, Collision

class Player(Rat):
    """
    Classe que representa o jogador no jogo.

    É uma classe concreta que herda da classe Rat, que por sua vez herda da classe Body.
    """
    COLOR = "blue"

    def __init__(self, pos):
        super().__init__(pos, Player.COLOR)
        self.lives = 3
        self.cheese = 0
        self.score = 0
        Rat.PLAYER = type(self)

    def damage(self, body, direction):
        if isinstance(body, Rat) and direction == Collision.BELLOW:
            return 1
        return 0
    
    def rebound(self, body, direction):
        if isinstance(body, Rat) and direction == Collision.SIDE:
            return 0.5
        return 0

    def collide(self, damage, rebound):
        self.lives -= damage
        self.velocity.x *= rebound.x
        self.velocity.y *= rebound.y

    
    