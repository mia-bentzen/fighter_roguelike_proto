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
    
    def draw(self):
        if self.bg:
            t.bkcolor(self.bg)
        if self.fg:
            t.color(self.fg)
        
        if hasattr(self, 'startup') and self.startup > 0:
            t.bkcolor('orange')
        
        t.put(self.x, self.y, self.char)
        
        if False:
            t.puts(self.x, self.y+1, f"{self.__class__.__name__}")
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