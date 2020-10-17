"""Terrain sample application"""
import time
import math
import pygame
import pygame.freetype

from quaternion import Quaternion
from scene import Scene
from object3d import Object3d
from camera import Camera
from mesh import Mesh
from material import Material
from color import Color
from vector3 import Vector3, dot_product, cross_product
from perlin import noise2d

def sample_height(x, y):
    """Computes the height of the terrain at the given x,y point, using
    2 octave 2d Perlin noise noise, with a given scale"""
    scale_noise = 1.25
    n = 0.5 * noise2d(x * scale_noise, y * scale_noise)
    n += 0.25 * noise2d(x * scale_noise * 2, y * scale_noise * 2)

    return n

def clamp_to_water(p, water_depth):
    """Clamps a height to be above water level as defined in the given parameter.
    If the value gets clamped, it returns True, otherwise it returns False"""
    if p. y <= water_depth:
        p. y = water_depth
        return True

    return False

def create_terrain():
    """Creates a terrain, composed of different meshes (one per each type of material)
    It support snow, water, grassland and cliffsize, based on hard-coded parameters"""

    # Size of the terrain
    size_x = 4
    size_z = 4
    # Number of divisions of the terrain. Vertex count scales with the square of this
    div = 40
    # Paramters for water and snow height/depth
    water_depth = -0.1
    snow_height = 0.15

    px = size_x / div
    pz = size_z / div

    # For centering the terrain on the object center
    origin = Vector3(-size_x * 0.5, 0, -size_z * 0.5)

    # Create the meshes for each type of terrain
    grass_mesh = Mesh("Terrain_Grass")
    snow_mesh = Mesh("Terrain_Snow")
    cliff_mesh = Mesh("Terrain_Cliff")
    water_mesh = Mesh("Terrain_Water")

    for dz in range(0, div):
        for dx in range(0, div):
            p1 = Vector3(dx * px, 0, dz * pz) + origin
            p2 = Vector3((dx + 1) * px, 0, dz * pz) + origin
            p3 = Vector3((dx + 1) * px, 0, (dz + 1) * pz) + origin
            p4 = Vector3(dx * px, 0, (dz + 1) * pz) + origin

            p1.y = sample_height(p1.x, p1.z)
            p2.y = sample_height(p2.x, p2.z)
            p3.y = sample_height(p3.x, p3.z)
            p4.y = sample_height(p4.x, p4.z)

            # Check if any of the points is underwater
            water = clamp_to_water(p1, water_depth)
            water |= clamp_to_water(p2, water_depth)
            water |= clamp_to_water(p3, water_depth)
            water |= clamp_to_water(p4, water_depth)

            # Create the polygons
            poly = []
            poly.append(p1)
            poly.append(p2)
            poly.append(p3)
            poly.append(p4)

            if water:
                # Polygon was under water, add it to that mesh
                water_mesh.polygons.append(poly)
            else:
                # Check for snow height
                avg_y = (p1.y + p2.y + p3.y + p4.y) * 0.25
                if avg_y > snow_height:
                    # The polygon was above a certain point
                    snow_mesh.polygons.append(poly)
                else:
                    # Check for cliff face, check the normal
                    normal = cross_product((p3 - p1).normalized(), (p2 - p1).normalized())
                    if dot_product(normal, Vector3(0, 1, 0)) < 0.5:
                        cliff_mesh.polygons.append(poly)
                    else:
                        grass_mesh.polygons.append(poly)

    # Create materials for the terrain
    grass_material = Material(Color(0.1, 0.6, 0.1, 1), "GrassMaterial")
    snow_material = Material(Color(0.8, 0.8, 0.8, 1), "SnowMaterial")
    cliff_material = Material(Color(0.4, 0.4, 0.4, 1), "CliffMaterial")
    water_material = Material(Color(0, 0.5, 0.7, 1), "WaterMaterial")

    # Return meshes and materials
    meshes = [grass_mesh, snow_mesh, cliff_mesh, water_mesh]
    materials = [grass_material, snow_material, cliff_material, water_material]

    return meshes, materials

# Define a main function, just to keep things nice and tidy
def main():
    """Main function, it implements the application loop"""
    # Initialize pygame, with the default parameters
    pygame.init()

    # Define the size/resolution of our window
    res_x = 1280
    res_y = 720

    # Create a window and a display surface
    screen = pygame.display.set_mode((res_x, res_y))

    # Create a scene
    scene = Scene("TestScene")
    scene.camera = Camera(False, res_x, res_y)

    # Moves the camera back 2 units
    scene.camera.position -= Vector3(0, 0, 4)
    scene.camera.rotation = Quaternion.AngleAxis(Vector3(1, 0, 0), math.radians(-15))

    # Creates the terrain meshes and materials
    terrain_meshes, terrain_materials = create_terrain()

    # Create container object for all the terrain sub-objects
    master_object = Object3d("TerrainObject")
    master_object.position = Vector3(0, -1, 0)
    scene.add_object(master_object)

    # Create the terrain objects and place it in a scene, at position (0,0,0)
    for _, (mesh, material) in enumerate(zip(terrain_meshes, terrain_materials)):
        obj = Object3d("TerrainObject")
        obj.scale = Vector3(1, 1, 1)
        obj.position = Vector3(0, 0, 0)
        obj.mesh = mesh
        obj.material = material
        master_object.add_child(obj)

    # Specify the rotation of the object. It will rotate 15 degrees around the axis given,
    # every second
    angle = 15
    axis = Vector3(0, 1, 0)
    axis.normalize()

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
                    return

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0, 0, 0))

        # Rotates the object, considering the time passed (not linked to frame rate)
        q = Quaternion.AngleAxis(axis, math.radians(angle) * delta_time)
        master_object.rotation = q * master_object.rotation

        #Commented code serves to make benchmarks
        Mesh.stat_vertex_count = 0
        Mesh.stat_transform_time = 0
        Mesh.stat_render_time = 0

        scene.render(screen)

        #Writes the benchmarks results
        print("Frame stats:")
        print(f"Vertex count = {Mesh.stat_vertex_count}")
        print(f"Transform time = {Mesh.stat_transform_time}s")
        print(f"Render time = {Mesh.stat_render_time}s")

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()

        print(f"Frame time = {delta_time}s")

# Run the main function
main()
