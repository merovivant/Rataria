from pygame import Vector2 as Vector
from collision import Collision

class Hitbox():
        def __init__(self, pos, width, height):
            self.SE = Vector(pos.x, pos.y)
            self.SD = Vector(pos.x+width, pos.y)
            self.ID = Vector(pos.x+width, pos.y+height)
            self.IE = Vector(pos.x, pos.y+height)

        def __contains__(self, hitbox):
            SE = hitbox.SE.x >= self.SE.x and hitbox.SE.x <= self.SD.x and hitbox.SE.y >= self.SE.y and hitbox.SE.y < self.IE.y
            SD = hitbox.SD.x >= self.SE.x and hitbox.SD.x <= self.SD.x and hitbox.SD.y >= self.SE.y and hitbox.SD.y < self.IE.y
            IE = hitbox.IE.x >= self.SE.x and hitbox.IE.x <= self.SD.x and hitbox.IE.y > self.SE.y and hitbox.IE.y <= self.IE.y
            ID = hitbox.ID.x >= self.SE.x and hitbox.ID.x <= self.SD.x and hitbox.ID.y > self.SE.y and hitbox.ID.y <= self.IE.y
            if((IE or ID) and not (SE or SD)):
                raise Collision(Collision.BELLOW)
            if(SE or SD):
                raise Collision(Collision.SIDE)
            if((SE or SD) and not (IE or ID)):
                raise Collision(Collision.TOP)
            else:
                return False
            

              
