from ursina import *

class SpinningCube(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='cube', color=color.orange, scale=(2, 2, 2), **kwargs)

    def update(self):
        self.rotation_y += time.dt * 100
