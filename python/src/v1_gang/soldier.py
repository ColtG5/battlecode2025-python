from battlecode25.stubs import *
from unit import Unit
import random


class Soldier(Unit):
    """Soldier unit class"""

    goal = None
    
    def setup(self):
        Unit.setup(self)
        return self
    
    def run(self):
        if self.goal is None:
            self.goal = MapLocation(random.randint(0, get_map_width() - 1), random.randint(0, get_map_height() - 1))
        
        self.nav.move_to(self.goal)
        
        # Check directly if we reached our goal
        if get_location() == self.goal:
            self.goal = None