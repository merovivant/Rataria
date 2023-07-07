from pygame import Vector2 as Vector
class Collision(Exception): 
    SIDE = 0
    TOP = 1
    BELLOW = -1

    def __init__(self, direction):
        super().__init__()
        self.direction = direction

    @property
    def bodies(self):
        return (self._producer, self._receiver)
    
    @bodies.setter
    def bodies(self, bodies):
        self._producer = bodies[0]
        self._receiver = bodies[1]
        damage = self._producer.damage(self._receiver, self.direction)
        rebound = self._producer.rebound(self._receiver, self.direction)
        x = self._receiver.hitbox.SD.x - self._producer.hitbox.SD.x
        x /= abs(self._receiver.hitbox.SD.x - self._producer.hitbox.SD.x) if x!=0 else 1
        y = self._receiver.hitbox.SD.y - self._producer.hitbox.SD.y
        y /= abs(self._receiver.hitbox.SD.y - self._producer.hitbox.SD.y) if y!=0 else 1
        rebound *= Vector(x, y)
        self._receiver.collide(damage, rebound)
        direction = self.direction if self.direction == Collision.SIDE else -1*self.direction
        damage = self._receiver.damage(self._producer, direction)
        rebound = self._receiver.rebound(self._producer, direction)
        x = self._producer.hitbox.SD.x - self._receiver.hitbox.SD.x
        x /= abs(self._producer.hitbox.SD.x - self._receiver.hitbox.SD.x) if x!=0 else 1
        y = self._producer.hitbox.SD.y - self._receiver.hitbox.SD.y
        y /= abs(self._producer.hitbox.SD.y - self._receiver.hitbox.SD.y) if y!=0 else 1
        rebound *= Vector(x, y)
        self._producer.collide(damage, rebound)
