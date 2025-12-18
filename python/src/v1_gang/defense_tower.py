from battlecode25.stubs import *
from tower import Tower


class Defense(Tower):
    def setup(self):
        Tower.setup(self)
        return self
    
    def run(self):
        pass
