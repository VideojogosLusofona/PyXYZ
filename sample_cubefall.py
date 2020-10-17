"""Cubefall sample application"""
import time
import random
import pygame

from quaternion import Quaternion

from scene import Scene
from object3d import Object3d
from camera import Camera
from mesh import Mesh
from material import Material
from color import Color
from vector3 import Vector3

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

def main():
    """Main function, it implements the application loop"""
    # Initialize pygame, with the default parameters
    pygame.init()

    # Define the size/resolution of our window
    res_x = 640
    res_y = 480

    # Create a window and a display surface
    screen = pygame.display.set_mode((res_x, res_y))

    # Create a scene
    scene = Scene("TestScene")
    scene.camera = Camera(False, res_x, res_y)

    # Moves the camera back 2 units
    scene.camera.position -= Vector3(0, 0, 2)

    # Create the cube mesh we're going to use for every single object
    cube_mesh = Mesh.create_cube((1, 1, 1))
    # Spawn rate is one cube every 25 ms
    spawn_rate = 0.025
    # Keep a timer for the cube spawn
    cube_spawn_time = spawn_rate
    # Storage for all the objects created this way
    falling_objects = []

    # Timer
    delta_time = 0
    prev_time = time.time()

    # Show mouse cursor
    pygame.mouse.set_visible(True)
    # Don't lock the mouse cursor to the game window
    pygame.event.set_grab(False)

    # Game loop, runs forever
    while True:
        # Process OS events
        for event in pygame.event.get():
            # Checks if the user closed the window
            if event.type == pygame.QUIT:
                # Exits the application immediately
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # If ESC is pressed exit the application
                    return

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0, 0, 0))

        # Update the cube spawn timer
        cube_spawn_time = cube_spawn_time - delta_time
        if cube_spawn_time < 0:
            # It's time to spawn a new cube
            cube_spawn_time = spawn_rate

            # Create a new cube, and add it to the scene
            new_cube = FallingCube(cube_mesh)
            scene.add_object(new_cube)

            # Add the new cube to the storage, so it can be updated
            falling_objects.append(new_cube)

        # Update the cubes
        for falling_object in falling_objects:
            falling_object.update(delta_time)

            # Is the cube fallen too far?
            if falling_object.position.y < -8:
                # Remove cube from scene
                scene.remove_object(falling_object)

        # Update the storage, so that all cubes that have fallen too far disappear
        falling_objects = [x for x in falling_objects if x.position.y > -8]

        # Render the scene
        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()


# Run the main function
main()
