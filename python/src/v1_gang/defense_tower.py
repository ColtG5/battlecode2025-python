from battlecode25.stubs import *
from tower import Tower


class Defense(Tower):
    """Defense tower class"""
    
    def setup(self):
        Tower.setup(self)
        return self
    
    def run(self):
        pass
