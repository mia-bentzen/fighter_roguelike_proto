from bearlibterminal import terminal as t

from actor import Actor
from actions import *

import random

class Enemy(Actor):
    char = 'E'
    fg = 'red'
    
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def act(self, key):
        from world import World
        import math
        
        player = World.get().player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx*dx+dy*dy)
        if dist <= 0:
            return ['move', 1, -1]
        dx /= dist
        dy /= dist
        
        if dist > 10:
            return ['move', round(dx), round(dy)]
        if dist < 5:
            return ['move', round(-dx), round(-dy)]
        
        return self.do_action(random.choice(list(actions.keys())), player.x, player.y)
        
        return ['wait', 10]