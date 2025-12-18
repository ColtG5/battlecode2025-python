from battlecode25.stubs import *


class Nav:
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
        self.target = None
        self.is_tracing = False
        self.tracing_dir = None
        self.closest_dist_while_tracing = 999999999
        self.trace_start_loc = None
        self.stuck_turns = 0
        self.last_loc = None
    
    def get_tile_score(self, loc, can_paint, has_enough_paint):
        if not can_sense_location(loc):
            return 1
        info = sense_map_info(loc)
        paint = info.get_paint()
        if paint.is_ally():
            return 3
        elif paint == PaintType.EMPTY:
            if can_paint and has_enough_paint:
                return 2
            return 1
        else:
            return 0
    
    def paint_below_if_needed(self, can_paint, has_enough_paint):
        if not can_paint or not has_enough_paint:
            return
        if not is_action_ready():
            return
        loc = get_location()
        if not can_sense_location(loc):
            return
        info = sense_map_info(loc)
        if info.get_paint() == PaintType.EMPTY:
            if can_attack(loc):
                attack(loc, False)
    
    def move_towards(self, direction):
        if direction is None or direction == Direction.CENTER:
            return False
        if not is_movement_ready():
            return False
        
        directions_to_try = [
            direction,
            direction.rotate_left(),
            direction.rotate_right(),
            direction.rotate_left().rotate_left(),
            direction.rotate_right().rotate_right(),
        ]
        
        for d in directions_to_try:
            if can_move(d):
                move(d)
                return True
        
        return False
    
    def bugnav_move_to(self, target, can_paint=False, paint_threshold=0.75):
        if target is None:
            return False
        
        current_loc = get_location()
        
        if current_loc == target:
            self.reset()
            return False
        
        if not is_movement_ready():
            return False
        
        has_enough_paint = False
        if can_paint:
            unit_type = get_type()
            max_paint = unit_type.paint_capacity
            current_paint = get_paint()
            has_enough_paint = current_paint >= max_paint * paint_threshold
        
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
            best_dir = None
            best_score = -1
            best_dist = 999999999
            
            for rotation in [0, 1, -1, 2, -2]:
                d = dir_to_target
                for i in range(abs(rotation)):
                    if rotation > 0:
                        d = d.rotate_left()
                    else:
                        d = d.rotate_right()
                if can_move(d):
                    new_loc = current_loc.add(d)
                    new_dist = new_loc.distance_squared_to(target)
                    if new_dist < current_dist:
                        score = self.get_tile_score(new_loc, can_paint, has_enough_paint)
                        if new_dist < best_dist:
                            best_dir = d
                            best_score = score
                            best_dist = new_dist
                        elif new_dist == best_dist and score > best_score:
                            best_dir = d
                            best_score = score
            
            if best_dir is not None:
                move(best_dir)
                self.paint_below_if_needed(can_paint, has_enough_paint)
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
                    self.paint_below_if_needed(can_paint, has_enough_paint)
                    return True
                self.closest_dist_while_tracing = current_dist
            
            d = self.tracing_dir
            
            best_wall_dir = None
            best_wall_score = -1
            rotations_checked = 0
            
            for i in range(8):
                if can_move(d):
                    new_loc = current_loc.add(d)
                    score = self.get_tile_score(new_loc, can_paint, has_enough_paint)
                    if best_wall_dir is None:
                        best_wall_dir = d
                        best_wall_score = score
                        rotations_checked = i
                    elif score > best_wall_score and i <= rotations_checked + 2:
                        best_wall_dir = d
                        best_wall_score = score
                        rotations_checked = i
                    else:
                        break
                if self.rotate_left:
                    d = d.rotate_left()
                else:
                    d = d.rotate_right()
            
            if best_wall_dir is not None:
                move(best_wall_dir)
                if self.rotate_left:
                    self.tracing_dir = best_wall_dir.rotate_right().rotate_right()
                else:
                    self.tracing_dir = best_wall_dir.rotate_left().rotate_left()
                self.paint_below_if_needed(can_paint, has_enough_paint)
                return True
            
            self.is_tracing = False
            return False
        
        return False
    
    def is_at_target(self, target=None):
        if target is not None:
            return get_location() == target
        if self.target is None:
            return False
        return get_location() == self.target
    
    def get_distance_to_target(self):
        if self.target is None:
            return 0
        return get_location().distance_squared_to(self.target)
