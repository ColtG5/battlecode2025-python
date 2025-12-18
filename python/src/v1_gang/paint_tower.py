from battlecode25.stubs import *
from tower import Tower


class Paint(Tower):
    def setup(self):
        Tower.setup(self)
        return self
    
    def run(self):
        if self.can_spawn_next_unit():
            self.spawn_next_unit()
