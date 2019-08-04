from bearlibterminal import terminal as t

from actor import Actor
from actions import *

NORMAL = 0
TARGET_DIRECTION = 1
TARGET_LOCATION = 2

class Player(Actor):
    char = '@'
    fg = 'yellow'
    
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.state = NORMAL
        self.tx = 0
        self.ty = 0
        self._action = None
        
        self.specials = [
            actions['stab'],
            actions['slash'],
            actions['long_slash'],
            actions['dash'],
            actions['slam'],
            actions['spit_fire'],
        ]
        
        self.hover_action = None
    
    def act(self, key):
        self.tx = t.state(t.TK_MOUSE_X)
        self.ty = t.state(t.TK_MOUSE_Y)
        
        if self.state == NORMAL:
            if key == t.TK_Z: return ['wait', 50]
            
            if key == t.TK_KP_6: return ['move',  1,  0]
            if key == t.TK_KP_3: return ['move',  1,  1]
            if key == t.TK_KP_2: return ['move',  0,  1]
            if key == t.TK_KP_1: return ['move', -1,  1]
            if key == t.TK_KP_4: return ['move', -1,  0]
            if key == t.TK_KP_7: return ['move', -1, -1]
            if key == t.TK_KP_8: return ['move',  0, -1]
            if key == t.TK_KP_9: return ['move',  1, -1]
            
            for n in range(1, 9):
                if key == getattr(t, f"TK_{n}") and n-1 < len(self.specials):
                    print(n, n-1, [x.name for x in self.specials], self.specials[n-1].name)
                    ac = self.specials[n-1]
                    self.state = TARGET_DIRECTION if ac.input == IDIRECTION else TARGET_LOCATION
                    self._action = [ac.id]
                    return None
            
            if key == t.TK_MOUSE_LEFT and self.hover_action:
                self.state = TARGET_DIRECTION if self.hover_action.input == IDIRECTION else TARGET_LOCATION
                self._action = [self.hover_action.id]
                return None
        
        elif self.state == TARGET_DIRECTION:
            if key == t.TK_ESCAPE:
                self.state = NORMAL
            
            if key == t.TK_KP_6:
                self.state = NORMAL
                return self.do_action(*self._action,  1,  0, modify=False)
            if key == t.TK_KP_3:
                self.state = NORMAL
                return self.do_action(*self._action,  1,  1, modify=False)
            if key == t.TK_KP_2:
                self.state = NORMAL
                return self.do_action(*self._action,  0,  1, modify=False)
            if key == t.TK_KP_1:
                self.state = NORMAL
                return self.do_action(*self._action, -1,  1, modify=False)
            if key == t.TK_KP_4:
                self.state = NORMAL
                return self.do_action(*self._action, -1,  0, modify=False)
            if key == t.TK_KP_7:
                self.state = NORMAL
                return self.do_action(*self._action, -1, -1, modify=False)
            if key == t.TK_KP_8:
                self.state = NORMAL
                return self.do_action(*self._action,  0, -1, modify=False)
            if key == t.TK_KP_9:
                self.state = NORMAL
                return self.do_action(*self._action,  1, -1, modify=False)
        
        elif self.state == TARGET_LOCATION:
            if key == t.TK_ESCAPE:
                self.state = NORMAL
            
            if key == t.TK_MOUSE_LEFT:
                self.state = NORMAL
                return self.do_action(*self._action, self.tx, self.ty, modify=False)
        
        from world import World
        World.get().draw()
    
    def hud(self, current):
        w = t.state(t.TK_WIDTH)
        h = t.state(t.TK_HEIGHT)
        mx = t.state(t.TK_MOUSE_X)
        my = t.state(t.TK_MOUSE_Y)
        
        from world import World
        entitiess_at = World.get().get_at(mx, my)
        i = 0
        for e in entitiess_at:
            info = ""
            
            if issubclass(e.__class__, Actor):
                info = f"{e.hp}/{e.max_hp}"
                
                if e.action and e.startup > 0:
                    info += f", is preparing to {e.action.name}"
                elif e.recovery > 0 and e.action:
                    info += f", is recovering from {e.action.name}"
            
            if info: info = ": "+info
            t.puts(0, h-1-i, f"{e.__class__.__name__}{info}")
            
            i+=1
        
        if self.state == 1:
            t.put(self.x+2, self.y, '>')
            t.put(self.x-2, self.y, '<')
            t.put(self.x, self.y+2, 'v')
            t.put(self.x, self.y-2, '^')
            t.puts(0, h-1, "Input a direction")
        if self.state == 2:
            t.put(self.tx, self.ty, 'X')
            t.puts(0, h-1, "Input a location")
        
        i = 0
        def md(s):
            nonlocal i
            l = t.measure(s)[0]
            t.puts(w-l, i, s)
            i+=1
        
        tooltip = ""
        
        t.bkcolor('darkest gray')
        t.color('white')
        t.clear_area(w-16, 0, 16, h)
        
        md(" ** SPECIALS ** ")
        md('')
        j = 1
        for ac in self.specials:
            name = f"{ac.name} : {j}"
            
            t.bkcolor('transparent')
            t.color('white')
            
            if self.state == NORMAL and current and my == i and mx >= w-len(name):
                
                t.bkcolor('white')
                t.color('black')
                
                tooltip = f"- {ac.name} -\n{ac.description}\nstartup: {ac.startup/1000} seconds\nrecovery: {ac.recovery/1000} seconds"
                self.hover_action = ac
            
            elif self.state != NORMAL:
                t.color('cyan' if actions[self._action[0]] == ac else 'gray')
            
            md(name)
            j+=1
        
        t.bkcolor('transparent')
        t.color('white')
        t.puts(w//2, h-6, tooltip, align=t.TK_ALIGN_CENTER)