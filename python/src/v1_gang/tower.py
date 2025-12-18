from battlecode25.stubs import *
from base import Robot

spawnable_units = [UnitType.SOLDIER, UnitType.MOPPER, UnitType.SPLASHER]
spawn_order = [0, 0]
current_spawn_index = 0


class Tower(Robot):
    def setup(self):
        Robot.setup(self)
        return self
    
    def before_turn(self):
        pass
    
    def after_turn(self):
        pass

    def can_spawn_next_unit(self):
        global current_spawn_index
        unit_type = spawnable_units[spawn_order[current_spawn_index]]
        return get_chips() >= unit_type.money_cost and get_paint() >= unit_type.paint_cost

    def spawn_next_unit(self):
        global current_spawn_index
        unit_type = spawnable_units[spawn_order[current_spawn_index]]
        
        for d in self.directions:
            spawn_loc = get_location().add(d)
            if can_build_robot(unit_type, spawn_loc):
                build_robot(unit_type, spawn_loc)
                current_spawn_index = (current_spawn_index + 1) % len(spawn_order)
                return True
        
        return False
