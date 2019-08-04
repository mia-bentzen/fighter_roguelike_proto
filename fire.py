from bearlibterminal import terminal as t

from entity import Entity
from action import Action

class Fire(Entity):
    char = '"'
    fg = 'white'
    bg = 'yellow'
    
    def __init__(self, x, y, life=None):
        super().__init__(x, y)
        
        import random
        self.life_time = 100 + random.randint(-25, 25)
        self.life = self.life_time
        if life:
            self.life_time = life[0]
            self.life = life[1]
        
        from world import World
        for e in (e for e in World.get().get_at(x, y) if e.__class__ == __class__):
            prev_lifetime = self.life_time
            self.life_time = self.life_time
            self.life = self.life + e.life
            #self.destroy()
            e.destroy()
    
    def draw(self):
        ratio = self.life / self.life_time
        if ratio < 1/1.1:
            self.fg = 'yellow'
            self.bg = 'red'
        if ratio < 1/1.25:
            self.fg = 'red'
            self.bg = 'orange'
        if ratio < 1/2:
            self.fg = 'orange'
            self.bg = 'dark orange'
        if ratio < 1/4:
            self.fg = 'darker orange'
            self.bg = 'darker gray'
        if ratio < 1/5:
            self.fg = 'darker gray'
            self.bg = None
        
        super().draw()
    
    def hud(self, current):
        mx = t.state(t.TK_MOUSE_X)
        my = t.state(t.TK_MOUSE_Y)
        
        t.bkcolor('black')
        if mx == self.x and my == self.y:
            t.puts(0, 6, f"fire: {self.life:>2}/{self.life_time:<2} ({self.life/self.life_time:.2f})")
    
    def tick(self):
        from world import World
        
        ratio = self.life / self.life_time
        if ratio > 1/4:
            for e in World.get().get_at(self.x, self.y):
                if e != self and hasattr(e, 'damage'):
                    e.damage(1)        
        
        self.life -= 1
        if self.life <= 0:
            self.destroy()
            return
        
        import random
        if random.random()*100 < 0.05:
            self.life//=2
            for i in range(1):
                offset = random.choice([
                    (-1,  0),
                    ( 0,  0),
                    ( 1,  0),
                    (-1,  1),
                    ( 0,  1),
                    ( 1,  1),
                    (-1, -1),
                    ( 0, -1),
                    ( 1, -1),
                ])
                f = World.get().add(Fire(self.x+offset[0], self.y+offset[1], (self.life_time, self.life)))
            return



class Damage(Entity):
    char = '+'
    fg = 'cyan'
    bg = 'dark cyan'
    
    def __init__(self, owner, amount, x, y):
        super().__init__(x, y)
        
        self.owner = owner
        
        from world import World
        for e in (e for e in World.get().get_at(x, y) if e.__class__ == __class__):
            e.destroy()
        
        import random
        
        self.life_time = amount/100# + random.randint(-5, 5)
        self.life_time = 75
        self.life = self.life_time
        
        for e in World.get().get_at(x, y):
            if e != self and e != self.owner and hasattr(e, 'damage'):
                e.damage(amount)
    
    def draw(self):
        self.life -= 1
        if self.life <= 0:
            self.destroy()
        
        return super().draw()
        
        ratio = self.life / self.life_time
        if ratio < 1/1.1:
            self.fg = 'cyan'
            self.bg = 'blue'
        if ratio < 1/1.25:
            self.fg = 'blue'
            self.bg = 'dark blue'
        if ratio < 1/2:
            self.fg = 'dark blue'
            self.bg = 'darker blue'
        if ratio < 1/4:
            self.fg = 'darker blue'
            self.bg = 'darker gray'
        if ratio < 1/5:
            self.fg = 'darker gray'
            self.bg = None
        
        super().draw()



class Bomb(Entity):
    char = 'O'
    fg = 'gray'
    bg = 'darker gray'
    
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y)
        
        self.vx = vx * 4
        self.vy = vy * 4
        self._x = x
        self._y = y
        
        import random
        
        self.life_time = 1000 + random.randint(-250, 250)
        self.life = self.life_time
    
    def draw(self):
        ratio = self.life / self.life_time
        if ratio < 1/2:
            self.fg = 'gray'
            self.bg = 'darker gray'
        if ratio < 1/4:
            self.fg = 'darker gray'
            self.bg = 'darkest gray'
        if ratio < 1/5:
            self.fg = 'yellow'
            self.bg = 'red'
        
        super().draw()
    
    def tick(self):
        dt = 1/100
        self.vx -= self.vx * dt * 0.1
        self.vy -= self.vy * dt * 0.1
        self._x += self.vx * dt
        self._y += self.vy * dt
        self.x = round(self._x)
        self.y = round(self._y)
        
        self.life -= 1
        if self.life <= 0:
            from world import World
            world = World.get()
            
            world.add(Fire(self.x, self.y))
            world.add(Fire(self.x-1, self.y))
            world.add(Fire(self.x+1, self.y))
            world.add(Fire(self.x, self.y-1))
            world.add(Fire(self.x, self.y+1))
            
            world.add(Fire(self.x-2, self.y))
            world.add(Fire(self.x+2, self.y))
            world.add(Fire(self.x, self.y-2))
            world.add(Fire(self.x, self.y+2))
            
            world.add(Fire(self.x-1, self.y+1))
            world.add(Fire(self.x+1, self.y-1))
            world.add(Fire(self.x+1, self.y+1))
            world.add(Fire(self.x-1, self.y-1))
            
            self.destroy()