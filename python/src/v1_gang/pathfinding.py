# Pathfinding utilities
from battlecode25.stubs import *


class BugNav:
    """Bug navigation - call move_to(target) once per turn."""
    
    def __init__(self):
        self.target = None
        self.is_tracing = False
        self.tracing_dir = None
        self.closest_dist_while_tracing = 999999999
        self.trace_start_loc = None
        self.stuck_turns = 0
        self.last_loc = None
        self.rotate_left = True
    
    def reset(self):
        """Reset pathfinding state."""
        self.target = None
        self.is_tracing = False
        self.tracing_dir = None
        self.closest_dist_while_tracing = 999999999
        self.trace_start_loc = None
        self.stuck_turns = 0
        self.last_loc = None
    
    def move_to(self, target):
        """Move one step toward target. Returns True if moved."""
        if target is None:
            return False
        
        current_loc = get_location()
        
        if current_loc == target:
            self.reset()
            return False
        
        if not is_movement_ready():
            return False
        
        if self.target is None or self.target != target:
            self.target = target
            self.is_tracing = False
            self.closest_dist_while_tracing = 999999999
            self.trace_start_loc = None
        
        if self.last_loc is not None and current_loc == self.last_loc:
            self.stuck_turns = self.stuck_turns + 1
            if self.stuck_turns > 2:
                self.rotate_left = not self.rotate_left
                self.is_tracing = False
                self.stuck_turns = 0
        else:
            self.stuck_turns = 0
        self.last_loc = current_loc
        
        current_dist = current_loc.distance_squared_to(target)
        dir_to_target = current_loc.direction_to(target)
        
        if not self.is_tracing:
            if can_move(dir_to_target):
                move(dir_to_target)
                return True
            
            for rotation in [1, -1, 2, -2]:
                d = dir_to_target
                for i in range(abs(rotation)):
                    if rotation > 0:
                        d = d.rotate_left()
                    else:
                        d = d.rotate_right()
                if can_move(d):
                    new_loc = current_loc.add(d)
                    if new_loc.distance_squared_to(target) < current_dist:
                        move(d)
                        return True
            
            self.is_tracing = True
            self.tracing_dir = dir_to_target
            self.closest_dist_while_tracing = current_dist
            self.trace_start_loc = current_loc
        
        if self.is_tracing:
            if current_dist < self.closest_dist_while_tracing:
                if can_move(dir_to_target):
                    self.is_tracing = False
                    move(dir_to_target)
                    return True
                self.closest_dist_while_tracing = current_dist
            
            d = self.tracing_dir
            
            for i in range(8):
                if can_move(d):
                    move(d)
                    if self.rotate_left:
                        self.tracing_dir = d.rotate_right().rotate_right()
                    else:
                        self.tracing_dir = d.rotate_left().rotate_left()
                    return True
                if self.rotate_left:
                    d = d.rotate_left()
                else:
                    d = d.rotate_right()
            
            self.is_tracing = False
            return False
        
        return False
    
    def is_at_target(self, target=None):
        """Check if at target. Pass target explicitly for reliability."""
        if target is not None:
            return get_location() == target
        if self.target is None:
            return False
        return get_location() == self.target
    
    def get_distance_to_target(self):
        """Get squared distance to target."""
        if self.target is None:
            return 0
        return get_location().distance_squared_to(self.target)


def move_toward(target):
    """Simple movement toward target (no wall tracing). Returns True if moved."""
    if target is None:
        return False
    
    current_loc = get_location()
    
    if current_loc == target:
        return False
    
    if not is_movement_ready():
        return False
    
    dir_to_target = current_loc.direction_to(target)
    
    if dir_to_target == Direction.CENTER:
        return False
    
    directions_to_try = [
        dir_to_target,
        dir_to_target.rotate_left(),
        dir_to_target.rotate_right(),
        dir_to_target.rotate_left().rotate_left(),
        dir_to_target.rotate_right().rotate_right(),
    ]
    
    for d in directions_to_try:
        if can_move(d):
            move(d)
            return True
    
    return False


def move_random():
    """Move in a random direction. Returns True if moved."""
    import random
    
    if not is_movement_ready():
        return False
    
    directions = [
        Direction.NORTH, Direction.NORTHEAST, Direction.EAST, Direction.SOUTHEAST,
        Direction.SOUTH, Direction.SOUTHWEST, Direction.WEST, Direction.NORTHWEST
    ]
    random.shuffle(directions)
    
    for d in directions:
        if can_move(d):
            move(d)
            return True
    
    return False
