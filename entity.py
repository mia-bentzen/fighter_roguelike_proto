from bearlibterminal import terminal as t

class Entity:
    char = ''
    fg : str = None
    bg : str = None
    
    level = 1
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.destroyed = False
        
        self.__exclamation_timer = 0
    
    def draw(self):
        char = self.char
        
        if self.bg:
            t.bkcolor(self.bg)
        if self.fg:
            t.color(self.fg)
        
        if hasattr(self, 'startup') and self.startup > 0:
            t.bkcolor('darkest red')
            t.color('red')
            
            self.__exclamation_timer += 0.0025
            self.__exclamation_timer %= 1
            if self.__exclamation_timer > 0.5:
                char = '!'
            
        elif hasattr(self, 'recovery') and self.recovery > 0 and self.action:
            t.bkcolor('darkest orange')
        
        t.put(self.x, self.y, char)
        
        if False:
            t.puts(self.x,self.y+1, f"{self.__class__.__name__}")
            i = 0
            for k, v in vars(self).items():
                t.puts(self.x, self.y+2+i, f"  {k:<16}: {v}")
                i+=1
    
    def update(self):
        pass
    
    def tick(self):
        pass
    
    def hud(self, current):
        pass
    
    def destroy(self):
        from world import World
        world = World.get()
        if self in world.entities:
            world.entities.remove(self)
        self.destroyed = True
    
    def move(self, dx, dy):
        from world import World
        from actor import Actor
        world = World.get()
        
        x = self.x+dx
        y = self.y+dy
        
        if not any([e for e in world.get_at(x, y) if issubclass(e.__class__, Actor)]):
            self.x = x
            self.y = y
    
    def __str__(self):
        return self.__class__.__name__
    def __repr__(self):
        return self.__class__.__name__