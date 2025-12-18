from battlecode25.stubs import *
from base import Robot
from pathfinding import Nav


class State:
    def __init__(self, unit):
        self.unit = unit
    
    def enter(self):
        pass
    
    def run(self):
        return None
    
    def exit(self):
        pass


class Unit(Robot):
    def setup(self):
        Robot.setup(self)
        self.nav = Nav()
        self.state = None
        return self
    
    def set_state(self, state_class):
        if self.state is not None:
            self.state.exit()
        self.state = state_class(self)
        self.state.enter()
    
    def run(self):
        if self.state is None:
            return
        
        next_state = self.state.run()
        
        while next_state is not None:
            self.set_state(next_state)
            next_state = self.state.run()
    
    def before_turn(self):
        pass
    
    def after_turn(self):
        pass
