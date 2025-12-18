from battlecode25.stubs import *
from base import Robot


class Unit(Robot):
    """Base class for all units (soldier, mopper, splasher)"""
    
    def setup(self):
        Robot.setup(self)
        return self
    
    def before_turn(self):
        """Called before run() each turn - setup logic for units"""
        pass
    
    def after_turn(self):
        """Called after run() each turn - cleanup logic for units"""
        pass
