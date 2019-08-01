from bearlibterminal import terminal as t

from entity import Entity
from actor import Actor
from player import Player
from enemy import Enemy

from typing import List

_world : 'World' = None

class World:
    def __init__(self):
        self.entities : List[Entity] = []
        
        self.act_index = 0
        
        self.player = self.add(Player(16, 8))
        
        self.add(Enemy(64, 4))
        self.add(Enemy(64, 8))
        self.add(Enemy(64, 12))
        
        self.turn = 0
    
    @staticmethod
    def set(world : 'World'):
        global _world
        _world = world
    
    @staticmethod
    def get() -> 'World':
        global _world
        return _world
    
    def add(self, e):
        self.entities.append(e)
        return e
    
    def get_at(self, x, y):
        return [e for e in self.entities if e.x == x and e.y == y]
    
    def draw(self, delay=False):
        t.clear()
        
        draw_list = sorted([e for e in self.entities if not e.destroyed], key = lambda x: x.level)
        
        t.composition(t.TK_ON)
        for e in draw_list:
            e.draw()
            
            t.bkcolor('transparent')
            t.color('white')
        t.composition(t.TK_OFF)
        
        t.puts(0, 0, f"HP: {self.player.hp:>3}/{self.player.max_hp:<3}")
        t.puts(0, 1, f"HP: {self.player.hp:>3}/{self.player.max_hp:<3}")
        t.puts(0, 2, f"T: {self.turn/1000:.2f} seconds")
        t.puts(0, 4, f"E: {len(self.entities)}")
        
        w = t.state(t.TK_WIDTH)
        h = t.state(t.TK_HEIGHT)
        
        t.bkcolor('transparent')
        t.color('white')
        
        for e in draw_list:
            e.hud(self.entities[self.act_index] == e)
        
        t.bkcolor('transparent')
        t.color('white')
        
        if self.player not in self.entities:
            t.puts(w//2-len("YOU DIED")//2, h//2, "YOU DIED")
        
        t.refresh()
        if delay:
            t.delay(25)
    
    def update(self, key):
        self.key = key
        
        for e in self.entities:
            e.update()
        
        for e in self.entities:
            if e.destroyed:
                self.entities.remove(e)
        
        self.tick()
    
    def tick(self):
        start_actor = None
        
        while True:
            if self.player not in self.entities:
                self.draw()
                break
            
            actor = self.entities[self.act_index]
            if actor == start_actor:
                self.key = None
                self.turn+=1
                self.draw(True)
            elif not start_actor:
                start_actor = actor
            
            if hasattr(actor, 'act'):
                if actor.startup > 0:
                    actor.startup -= 1
                    if actor.startup <= 0:
                        actor.action.execute(actor, *actor.action_args)
                        
                        actor.action = None
                    
                    actor.tick()
                    self.act_index += 1
                elif actor.recovery > 0:
                    actor.recovery -= 1
                    
                    actor.tick()
                    self.act_index += 1
                else:
                    action_array = actor.act(self.key)
                    if not action_array:
                        break
                    else:
                        name = action_array[0]
                        if name == 'wait':
                            actor.recovery = action_array[1]
                        if name == 'move':
                            actor.x += action_array[1]
                            actor.y += action_array[2]
                            import random
                            actor.recovery = 5
                        if name == 'action':
                            actor.action_args = action_array[2:]
                            actor.action = action_array[1]
                            actor.startup = actor.action.startup
                            actor.recovery = actor.action.recovery
                        actor.recovery -= 1
                        
                        actor.tick()
                        self.act_index += 1
            else:
                actor.tick()
                self.act_index += 1
            
            self.act_index %= len(self.entities)
    
    def end(self):
        from main import end
        end()