"""Base Robot class and shared constants"""
from battlecode25.stubs import *

turn_count = 0

directions = [
    Direction.NORTH,
    Direction.NORTHEAST,
    Direction.EAST,
    Direction.SOUTHEAST,
    Direction.SOUTH,
    Direction.SOUTHWEST,
    Direction.WEST,
    Direction.NORTHWEST,
]


class Robot:
    """Base class for all robots"""
    
    def setup(self):
        """Initialize the robot - call this instead of __init__"""
        self.indicator_string = ""
        return self
    
    def init(self):
        """Called at the start of each turn - initialization logic"""
        self.indicator_string = ""
    
    def cleanup(self):
        """Called at the end of each turn - final cleanup"""
        set_indicator_string(self.indicator_string)
    
    def before_turn(self):
        """Called before run() each turn - setup logic"""
        pass
    
    def run(self):
        """Main run method - must be implemented by subclasses"""
        pass
    
    def after_turn(self):
        """Called after run() each turn - cleanup logic"""
        pass
