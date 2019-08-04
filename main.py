from bearlibterminal import terminal as t

from world import World
from entity import Entity
from actor import Actor
from player import Player

world = World()
World.set(world)

def end():
    import sys
    t.close()
    sys.exit(0)

def draw():
    global world
    world.draw()

def update(key):
    global world
    world.update(key)



def main():
    t.open()
    t.set("window.size = 120x40")
    t.set("input.filter = [keyboard, mouse]")
    t.set("input.precise = true")

    while True:
        draw()
        
        key = -1
        if t.has_input():
            while t.has_input():
                key = t.read()
                if key == t.TK_CLOSE:
                    end()
            update(key)
        
        t.delay(1)

if __name__ == "__main__":
    main()