from player import Player, Rat
from body import Body, Hitbox, Vector
from collision import Collision
from tile import Tile
from config import Config


class Bodies(list):
    """
    Classe que representa uma lista de corpos no jogo.
    A maioria das funções de lista são suportadas.
    Adiciona novas funções específicas para o jogo.
    """    
    def __contains__(self, body: Body) -> bool: # Verifica se um corpo está dentro de outro, analisando suas hitboxes        
        for b in self:
            if b == body or b.kill: continue
            try: assert not body.hitbox in b.hitbox # Verifica se a hitbox do corpo está dentro de outro corpo   
            except Collision as collision:
                collision.bodies = (body, b)
                if collision.direction == Collision.SIDE:
                    print(f"Colisão lateral entre {type(body).__name__} e {type(b).__name__}")
                elif collision.direction == Collision.TOP:
                    print(f"Colisão superior entre {type(body).__name__} e {type(b).__name__}")
                elif collision.direction == Collision.BELLOW:
                    print(f"Colisão inferior entre {type(body).__name__} e {type(b).__name__}")
                return True
            except AssertionError:
                print("Erro no tratamento de colisão!")
                return True
        
        hitbox_bellow = Hitbox(body.hitbox.SE, body.width, 81)
        for b in self:
            if b == body or b.kill: continue
            try: assert not hitbox_bellow in b.hitbox # Verifica se a posição abaixo do corpo está dentro de outro corpo
            except Collision as collision:
                body.falling = False
                if isinstance(body, Player) and isinstance(b, Rat):
                    collision.bodies = (body, b)
                return False
            except AssertionError:
                print("Erro no tratamento de colisão!")
        body.falling = True
        return False
    
    def update(self, dt): # Atualiza todos os corpos da lista
        for body in self:
            body.update(dt, self)

    def draw(self, screen, camera):
        for body in self:
            if body.kill: continue
            body.draw(screen, camera)

    def player(self) -> Player: # Retorna o player da lista
        for body in self:
            if isinstance(body, Player):
                return body
            
    def tiles(self, tilemap, camera):
        for i, row in enumerate(tilemap):
            for j, tile in enumerate(row):
                if tile == 1:
                    pos_x = j * Tile.SIZE - camera.pos.x
                    if pos_x <= - Tile.SIZE: continue
                    pos = Vector(pos_x, Config.SCREEN_HEIGHT - Tile.SIZE * (len(tilemap) - i))
                    self.append(Tile(pos))

    
