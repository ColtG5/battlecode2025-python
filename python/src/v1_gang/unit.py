from battlecode25.stubs import *
from base import Robot
from pathfinding import BugNav

class Unit(Robot):
    """Base class for all units (soldier, mopper, splasher)"""
    
    def setup(self):
        Robot.setup(self)
        self.nav = BugNav()  # Create pathfinding instance

        return self
    
    def before_turn(self):
        """Called before run() each turn - setup logic for units"""
        pass
    
    def after_turn(self):
        """Called after run() each turn - cleanup logic for units"""
        pass
