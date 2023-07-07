from body import Body, Collision, Hitbox
from pygame.transform import scale
from pygame.image import load
from rat import Rat
class Tile(Body):
    """
    Classe que representa os tijolos no jogo.
    É uma classe concreta que herda da classe Body.
    """
    SIZE = 80
    NONE = 0  # Constante para representar a ausência de bloco
    TILE = 1  # Constante para representar um bloco de chão

    def __init__(self, pos, camera, num):
        super().__init__(pos, Tile.SIZE, Tile.SIZE)
        self.block_texture = scale(load(f'imgs/tile.jpeg'), (Tile.SIZE,Tile.SIZE))
        self.camera = camera
        self.num = num

    @property
    def pos(self):
        #self._pos.x = self.num * Tile.SIZE - self.camera.pos.x
        return self._pos
    
    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self.hitbox = Hitbox(pos, self.width, self.height)

    @property
    def falling(self):
        return False
    
    @falling.setter
    def falling(self, falling):
        pass

    def draw(self, screen, camera):
        pos_x = self.num * Tile.SIZE - camera.pos.x
        if pos_x <= - Tile.SIZE: return    
        screen.blit(self.block_texture, (pos_x, self.pos.y))
        from pygame.draw import rect
        rect(screen, (255,0,0), (self.hitbox.SE.x, self.hitbox.SE.y, self.width, self.height), 1)

    def damage(self, body, direction):
        if direction == Collision.TOP and isinstance(body, Rat):
            body.pos.y = self.pos.y - body.height
        return 0
    
    def rebound(self, body, direction): 
        return 0

    def collide(self, *args):
        pass

    def update(self, dt, bodies):
        # if self.pos.x <= - Tile.SIZE:
        #     self.kill = True
        # else:
        #     self.kill = False
        pass