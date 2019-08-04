from action import Action, action, actions, ILOCATION, IDIRECTION

@action("Stab",
        "Stab at enemy, deals more damage at range",
        startup = 50,
        recovery = 50,
        input = IDIRECTION)
def stab(actor, dx, dy):
    from world import World
    from fire import Damage
    
    x = actor.x + dx * 1
    y = actor.y + dy * 1
    
    world = World.get()
    world.add(Damage(actor, 25, x, y))
    world.add(Damage(actor, 50, x+dx, y+dy))
    world.add(Damage(actor, 75, x+dx*2, y+dy*2))
    world.add(Damage(actor, 25, x+dy, y+dx))
    world.add(Damage(actor, 25, x-dy, y-dx))

@action("Slash",
        "Slash at enemy, deals more damage in center",
        startup = 150,
        recovery = 50,
        input = IDIRECTION)
def slash(actor, dx, dy):
    from world import World
    from fire import Damage
    
    x = actor.x + dx * 2
    y = actor.y + dy * 2
    
    world = World.get()
    world.add(Damage(actor, 100, x, y))
    world.add(Damage(actor, 60, x+1, y))
    world.add(Damage(actor, 60, x-1, y))
    world.add(Damage(actor, 60, x, y+1))
    world.add(Damage(actor, 60, x, y-1))

@action("Long Slash",
        "Slash at enemy, deals more damage in center",
        startup = 200,
        recovery = 120,
        input = IDIRECTION)
def long_slash(actor, dx, dy):
    from world import World
    from fire import Damage
    
    x = actor.x + dx * 4
    y = actor.y + dy * 4
    
    world = World.get()
    world.add(Damage(actor, 40, actor.x+dx, actor.y+dy))
    world.add(Damage(actor, 60, actor.x+dx*2, actor.y+dy*2))
    world.add(Damage(actor, 100, x, y))
    world.add(Damage(actor, 80, x+1, y))
    world.add(Damage(actor, 80, x-1, y))
    world.add(Damage(actor, 80, x, y+1))
    world.add(Damage(actor, 80, x, y-1))

@action("Dash",
        "Dash through enemies while dealing damage",
        startup = 150,
        recovery = 350,
        input = IDIRECTION)
def dash(actor, dx, dy):
    from world import World
    from fire import Damage
    
    tx = actor.x + dx * 10
    ty = actor.y + dy * 10
    x = actor.x
    y = actor.y
    actor.x = tx
    actor.y = ty
    
    world = World.get()
    for i in range(8):
        x += dx
        y += dy
        world.add(Damage(actor, 5, x, y))

@action("Slam",
        "Slam down into the ground at target location",
        startup = 350,
        recovery = 750,
        input = ILOCATION)
def slam(actor, x, y):
    from world import World
    from fire import Damage
    
    actor.x = x
    actor.y = y
    
    world = World.get()
    #world.add(Damage(actor, 75, x, y))
    world.add(Damage(actor, 75, x+1, y))
    world.add(Damage(actor, 75, x-1, y))
    world.add(Damage(actor, 75, x, y+1))
    world.add(Damage(actor, 75, x, y-1))

@action("Spit Fire",
        "...",
        startup = 150,
        recovery = 350,
        input = IDIRECTION)
def spit_fire(actor, dx, dy):
    from world import World
    from fire import Fire
    
    tx = actor.x + dx * 4
    ty = actor.y + dy * 4
    x = actor.x
    y = actor.y
    
    world = World.get()
    for i in range(8):
        x += dx
        y += dy
        if i > 1:
            world.add(Fire(x, y))