from battlecode25.stubs import *
from unit import Unit


class Mopper(Unit):
    """Mopper unit class"""
    
    def setup(self):
        Unit.setup(self)
        return self
    
    def run(self):
        pass
