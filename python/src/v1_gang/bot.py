import random

from battlecode25.stubs import *
from soldier import Soldier
from mopper import Mopper
from splasher import Splasher
from money_tower import Money
from defense_tower import Defense
from paint_tower import Paint

robot = None


def turn():
    global robot
    
    # Initialize robot on first turn
    if robot is None:
        robot_type = get_type()
        
        if robot_type == UnitType.SOLDIER:
            robot = Soldier().setup()
        elif robot_type == UnitType.MOPPER:
            robot = Mopper().setup()
        elif robot_type == UnitType.SPLASHER:
            robot = Splasher().setup()
        elif robot_type == UnitType.LEVEL_ONE_MONEY_TOWER or robot_type == UnitType.LEVEL_TWO_MONEY_TOWER or robot_type == UnitType.LEVEL_THREE_MONEY_TOWER:
            robot = Money().setup()
        elif robot_type == UnitType.LEVEL_ONE_DEFENSE_TOWER or robot_type == UnitType.LEVEL_TWO_DEFENSE_TOWER or robot_type == UnitType.LEVEL_THREE_DEFENSE_TOWER:
            robot = Defense().setup()
        elif robot_type == UnitType.LEVEL_ONE_PAINT_TOWER or robot_type == UnitType.LEVEL_TWO_PAINT_TOWER or robot_type == UnitType.LEVEL_THREE_PAINT_TOWER:
            robot = Paint().setup()
    
    robot.init()
    robot.before_turn()
    robot.run()
    robot.after_turn()
    robot.cleanup()
