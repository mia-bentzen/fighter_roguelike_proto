from typing import Dict

ILOCATION = 0
IDIRECTION = 1

class Action:
    name = ""
    description = ""
    startup = 0
    recovery = 0
    input = -1
    __name = ""
    
    @staticmethod
    def execute(actor, *args, **kwargs):
        pass

actions : Dict[str, Action] = {}
def action(name, description, *, startup, recovery, input, **kwargs):
    def wrapper(func):
        _name = name
        _description = description
        _startup = startup
        _recovery = recovery
        _input = input
        _id = func.__name__
        print(func.__name__)
        class _tmp(Action):
            name = _name
            description = _description
            startup = _startup
            recovery = _recovery
            input = _input
            id = _id
            
            @staticmethod
            def execute(actor, *args, **kwargs):
                func(actor, *args, **kwargs)
        
        actions[func.__name__] = _tmp
        return _tmp
    return wrapper