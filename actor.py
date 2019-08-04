from bearlibterminal import terminal as t

from entity import Entity
from action import Action, actions, IDIRECTION, ILOCATION

class Actor(Entity):
    
    max_hp = 500
    max_meter = 5
    
    level = 2
    
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.hp = self.max_hp
        self.meter = 0
        
        self.startup = 0
        self.recovery = 0
        self.action : Action = None
        
        self.flash = 0
    
    def draw(self):
        if self.flash > 0:
            t.bkcolor('red')
            t.color('white')
            t.put(self.x, self.y, self.char)
            
            self.flash -= 1
        else:
            super().draw()
    
    def damage(self, amount):
        from world import log
        self.flash = 250
        
        log(f"{self} took {amount} damage!")
        
        self.hp -= amount
        if self.hp <= 0:
            self.destroy()
    
    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def act(self, key):
        return ['wait', 10]
    
    def do_action(self, name, x, y, *args, modify=True):
        ac = actions[name]
        if ac.input == IDIRECTION and modify:
            import math
            x = x - self.x
            y = y - self.y
            d = math.sqrt(x*x+y*y)
            if d != 0:
                x/=d
                y/=d
                x=round(x)
                y=round(y)
        return ['action', ac, x, y, *args]