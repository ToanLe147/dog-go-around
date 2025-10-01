from ursina import *

class Game:
    def __init__(self):
        # Create a player cube
        self.player = Entity(
            model='cube',
            color=color.blue,
            scale=(1, 1, 1),
            position=(0, 1, 0)
        )

        # Create a ground plane
        self.ground = Entity(
            model='plane',
            scale=(10, 1, 10),
            color=color.green,
            position=(0, 0, 0),
            texture='white_cube',
            texture_scale=(10, 10)
        )

        # Create a simple camera
        self.camera = EditorCamera()

    def update(self):
        # Player movement
        if held_keys['w']:
            self.player.position += self.player.forward * time.dt * 5
        if held_keys['s']:
            self.player.position -= self.player.forward * time.dt * 5
        if held_keys['a']:
            self.player.position -= self.player.right * time.dt * 5
        if held_keys['d']:
            self.player.position += self.player.right * time.dt * 5
        if held_keys['space']:
            self.player.position += Vec3(0, 1, 0) * time.dt * 5
        if held_keys['shift']:
            self.player.position -= Vec3(0, 1, 0) * time.dt * 5

        # Rotation with arrow keys
        if held_keys['left arrow']:
            self.player.rotation_y -= time.dt * 100
        if held_keys['right arrow']:
            self.player.rotation_y += time.dt * 100
