from action import Action, action, actions, ILOCATION, IDIRECTION

@action("Stab",
        "Stab at enemy",
        startup = 5,
        recovery = 5,
        input = IDIRECTION)
def stab(actor, dx, dy):
    from world import World
    from fire import Damage
    
    x = actor.x + dx * 1
    y = actor.y + dy * 1
    
    world = World.get()
    world.add(Damage(actor, 25, x, y))
    world.add(Damage(actor, 25, x+dx, y+dy))
    world.add(Damage(actor, 25, x+dx*2, y+dy*2))
    world.add(Damage(actor, 25, x+dy, y+dx))
    world.add(Damage(actor, 25, x-dy, y-dx))

@action("Slash",
        "Slash at enemy",
        startup = 15,
        recovery = 5,
        input = IDIRECTION)
def slash(actor, dx, dy):
    from world import World
    from fire import Damage
    
    x = actor.x + dx * 2
    y = actor.y + dy * 2
    
    world = World.get()
    world.add(Damage(actor, 60, x, y))
    world.add(Damage(actor, 60, x+1, y))
    world.add(Damage(actor, 60, x-1, y))
    world.add(Damage(actor, 60, x, y+1))
    world.add(Damage(actor, 60, x, y-1))

@action("Dash",
        "Dash through enemies while dealing damage",
        startup = 15,
        recovery = 35,
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
        startup = 35,
        recovery = 75,
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
        startup = 15,
        recovery = 35,
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