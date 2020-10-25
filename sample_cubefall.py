"""Cubefall sample application"""
import math
import random

from application import Application
from object3d import Object3d
from mesh import Mesh
from material import Material
from color import Color
from vector3 import Vector3
from quaternion import Quaternion

GRAVITY = -9.8

class FallingCube(Object3d):
    """Falling cube 3d object"""
    def __init__(self, mesh):
        super().__init__("FallingCube")
        # Create a cube on a random positions
        self.position = Vector3(random.uniform(-6, 6), random.uniform(6, 10), random.uniform(3, 10))
        self.mesh = mesh
        # Pick a random Color for the cube
        self.material = Material(Color(random.uniform(0.1, 1),
                                       random.uniform(0.1, 1),
                                       random.uniform(0.1, 1), 1),
                                 "FallingCubeMaterial")
        # Starting velocity is zero
        self.velocity = 0
        # Select a random rotation axis
        self.rotation_axis = Vector3(random.uniform(-1, 1),
                                     random.uniform(-1, 1),
                                     random.uniform(-1, 1)).normalized()
        # Select a random rotation speed
        self.rotation_speed = random.uniform(-0.5, 0.5)

    def update(self, delta_time):
        """Animates the cube, accelerating it with gravity and rotating it."""
        self.velocity += GRAVITY * delta_time
        self.position.y += self.velocity * delta_time

        q = Quaternion.AngleAxis(self.rotation_axis, self.rotation_speed * delta_time)
        self.rotation = q * self.rotation

class SampleCubefall(Application):
    def init_scene(self):
        # Moves the camera back 2 units
        self.scene.camera.position -= Vector3(0, 0, 2)

        # Create the cube mesh we're going to use for every single object
        self.cube_mesh = Mesh.create_cube((1, 1, 1))
        # Spawn rate is one cube every 25 ms
        self.spawn_rate = 0.025
        # Keep a timer for the cube spawn
        self.cube_spawn_time = self.spawn_rate
        # Storage for all the objects created this way
        self.falling_objects = []

    def update(self, delta_time):
        # Update the cube spawn timer
        self.cube_spawn_time = self.cube_spawn_time - delta_time
        if self.cube_spawn_time < 0:
            # It's time to spawn a new cube
            self.cube_spawn_time = self.spawn_rate

            # Create a new cube, and add it to the scene
            new_cube = FallingCube(self.cube_mesh)
            self.scene.add_object(new_cube)

            # Add the new cube to the storage, so it can be updated
            self.falling_objects.append(new_cube)

        # Update the cubes
        for falling_object in self.falling_objects:
            falling_object.update(delta_time)

            # Is the cube fallen too far?
            if falling_object.position.y < -8:
                # Remove cube from scene
                self.scene.remove_object(falling_object)

        # Update the storage, so that all cubes that have fallen too far disappear
        self.falling_objects = [x for x in self.falling_objects if x.position.y > -8]

app = SampleCubefall()
app.run()

