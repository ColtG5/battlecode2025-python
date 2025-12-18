import random
from battlecode25.stubs import *
from base import Robot, directions

spawnable_units = [UnitType.SOLDIER, UnitType.MOPPER, UnitType.SPLASHER]
spawn_order = [0, 0, 1, 2]
current_spawn_index = 0


class Tower(Robot):
    """Base class for all towers (money, defense, paint)"""
    
    def setup(self):
        Robot.setup(self)
        return self
    
    def before_turn(self):
        """Called before run() each turn - setup logic for towers"""
        pass
    
    def after_turn(self):
        """Called after run() each turn - cleanup logic for towers"""
        pass

    def can_spawn_next_unit(self):
        global current_spawn_index
        unit_type = spawnable_units[spawn_order[current_spawn_index]]
        
        curr_money = get_chips()
        curr_paint = get_paint()
        
        paint_cost = unit_type.paint_cost
        money_cost = unit_type.money_cost
        
        return curr_money >= money_cost and curr_paint >= paint_cost

    def spawn_next_unit(self):
        global current_spawn_index
        unit_type = spawnable_units[spawn_order[current_spawn_index]]
        
        for d in directions:
            spawn_loc = get_location().add(d)
            if can_build_robot(unit_type, spawn_loc):
                build_robot(unit_type, spawn_loc)
                current_spawn_index = (current_spawn_index + 1) % len(spawn_order)
                return True
        
        return False
