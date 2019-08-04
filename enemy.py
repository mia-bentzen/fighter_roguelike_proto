from bearlibterminal import terminal as t

from actor import Actor
from actions import *

import random

class Enemy(Actor):
    char = 'E'
    fg = 'orange'
    
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
        
        delta = random.choices([
            (round(dx), round(dy)),
            (round(-dx), round(-dy)),
            None
        ], [
            8 if dist > 4 else 0.5,
            8 if dist < 2 else 0.5,
            0.1,
        ])[0]
        #if dist > 4:
        #    return ['move', round(dx), round(dy)]
        #if dist < 2:
        #    return ['move', round(-dx), round(-dy)]
        
        if delta:
            return ['move', *delta]
        else:
            ai_actions = [
                'stab',
                'slash',
                'long_slash',
            ]
            
            #ai_actions = list(actions.keys())
            return self.do_action(random.choice(ai_actions), player.x, player.y)
            
        return ['wait', 10]