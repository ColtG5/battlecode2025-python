from battlecode25.stubs import *
from unit import Unit, State
import random


class Soldier(Unit):
    goal = None
    build_target = None
    failed_builds = []
    
    def setup(self):
        Unit.setup(self)
        self.failed_builds = []
        self.set_state(ExploreState)
        return self


class ExploreState(State):
    def enter(self):
        self.unit.goal = None
    
    def run(self):
        self.unit.indicator_string = self.unit.indicator_string + "EXPLORE, "
        
        nearby_ruins = sense_nearby_ruins()
        for ruin_loc in nearby_ruins:
            if sense_robot_at_location(ruin_loc) is not None:
                continue
            if ruin_loc in self.unit.failed_builds:
                continue

            self.unit.build_target = ruin_loc
            return BuildState
        
        if self.unit.goal is None or get_location() == self.unit.goal:
            self.unit.goal = MapLocation(
                random.randint(0, get_map_width() - 1),
                random.randint(0, get_map_height() - 1)
            )
        
        if self.unit.goal is not None:
            set_indicator_dot(self.unit.goal, 0, 255, 0)
            self.unit.indicator_string = self.unit.indicator_string + f"goal: {self.unit.goal}, "
        
        self.unit.nav.bugnav_move_to(self.unit.goal, can_paint=True)
        return None


class BuildState(State):
    def enter(self):
        self.turns_stuck = 0
    
    def run(self):
        target = self.unit.build_target
        tower_type = UnitType.LEVEL_ONE_MONEY_TOWER
        
        if target is None:
            return ExploreState
        
        self.unit.indicator_string = self.unit.indicator_string + f"BUILD target: {target}, "
        set_indicator_dot(target, 255, 0, 0)

        if sense_robot_at_location(target) is not None:
            return ExploreState
        
        if not can_sense_location(target) or get_location().distance_squared_to(target) > UnitType.SOLDIER.action_radius_squared:
            self.unit.nav.bugnav_move_to(target, can_paint=True)
            return None
        
        for tile in sense_nearby_map_infos(target, 8):
            if tile.get_paint().is_enemy():
                self.unit.failed_builds.append(target)
                return ExploreState
        
        had_action = is_action_ready()
        
        map_info_near_ruin = None
        for d in self.unit.directions:
            loc_to_check = target.add(d)
            if can_sense_location(loc_to_check):
                map_info_near_ruin = sense_map_info(loc_to_check)
                break
        
        needs_marking = map_info_near_ruin is not None and map_info_near_ruin.get_mark() == PaintType.EMPTY
        
        if needs_marking:
            if can_mark_tower_pattern(tower_type, target):
                mark_tower_pattern(tower_type, target)
                self.unit.indicator_string = self.unit.indicator_string + "marked, "
            else:
                self.unit.indicator_string = self.unit.indicator_string + "moving to mark, "
                self.unit.nav.bugnav_move_to(target, can_paint=True)
                return None
        
        tile_to_paint = None
        for tile in sense_nearby_map_infos(target, 8):
            if tile.get_mark() != PaintType.EMPTY and tile.get_mark() != tile.get_paint():
                tile_to_paint = tile
                break
        
        if tile_to_paint is not None:
            tile_loc = tile_to_paint.get_map_location()
            if can_attack(tile_loc):
                use_secondary = tile_to_paint.get_mark() == PaintType.ALLY_SECONDARY
                attack(tile_loc, use_secondary)
                self.unit.indicator_string = self.unit.indicator_string + f"painted {tile_loc}, "
            else:
                self.unit.indicator_string = self.unit.indicator_string + f"moving to {tile_loc}, "
                self.unit.nav.bugnav_move_to(tile_loc, can_paint=True)
                return None
        
        if can_complete_tower_pattern(tower_type, target):
            complete_tower_pattern(tower_type, target)
            self.unit.indicator_string = self.unit.indicator_string + "DONE!, "
            return ExploreState
        
        if tile_to_paint is None:
            self.unit.indicator_string = self.unit.indicator_string + "moving to complete, "
            self.unit.nav.bugnav_move_to(target, can_paint=True)
        
        if had_action and is_action_ready():
            self.turns_stuck = self.turns_stuck + 1
            if self.turns_stuck >= random.randint(6, 7):
                self.unit.failed_builds.append(target)
                return ExploreState
        else:
            self.turns_stuck = 0
        
        return None
