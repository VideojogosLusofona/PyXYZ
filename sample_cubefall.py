# Import pygame into our program
import pygame
import pygame.freetype
import time
import random

from scene import Scene
from object3d import Object3d
from camera import Camera
from mesh import Mesh
from material import Material
from color import color
from vector3 import vector3
from quaternion import from_rotation_vector

gravity = -9.8

class FallingCube(Object3d):
    def __init__(self, mesh):
        super().__init__("FallingCube")
        self.position = vector3(random.uniform(-6, 6), random.uniform(6, 10), random.uniform(3, 10))
        self.mesh = mesh
        self.material = Material(color(random.uniform(0.1, 1),random.uniform(0.1, 1),random.uniform(0.1, 1),1), "FallingCubeMaterial")
        self.velocity = 0
        self.rotation_axis = vector3(random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)).normalized()
        self.rotation_speed = random.uniform(-0.5, 0.5)

    def update(self, delta_time):
        self.velocity += gravity * delta_time
        self.position.y += self.velocity * delta_time

        q = from_rotation_vector((self.rotation_axis * self.rotation_speed * delta_time).to_np3())
        self.rotation = q * self.rotation

# Define a main function, just to keep things nice and tidy
def main():
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
    scene.camera.position -= vector3(0,0,2)

    cube_mesh = Mesh.create_cube((1,1,1))
    spawn_rate = 0.025
    cube_spawn_time = spawn_rate
    falling_objects = []

    # Timer
    delta_time = 0
    prev_time = time.time()

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)

    # Game loop, runs forever
    while (True):
        # Process OS events
        for event in pygame.event.get():
            # Checks if the user closed the window
            if (event.type == pygame.QUIT):
                # Exits the application immediately
                return
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    return

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,0))

        cube_spawn_time = cube_spawn_time - delta_time
        if (cube_spawn_time < 0):
            cube_spawn_time = spawn_rate
            
            newCube = FallingCube(cube_mesh)
            scene.add_object(newCube)

            falling_objects.append(newCube)

        for falling_object in falling_objects:
            falling_object.update(delta_time)
            if (falling_object.position.y < -8):
                scene.remove_object(falling_object)

        falling_objects = [x for x in falling_objects if x.position.y > -8]

        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()


# Run the main function
main()
