from battlecode25.stubs import *


class Robot:
    turn_count = 0
    shared_int = 0

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

    def setup(self):
        return self
    
    def init(self):
        self.turn_count = self.turn_count + 1
        self.indicator_string = f"id: {get_id()}, "
    
    def cleanup(self):
        set_indicator_string(self.indicator_string)
    
    def before_turn(self):
        pass
    
    def run(self):
        pass
    
    def after_turn(self):
        pass
