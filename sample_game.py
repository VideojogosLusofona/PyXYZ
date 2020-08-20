# Import pygame into our program
import pygame
import pygame.freetype
import time

from scene import *
from object3d import *
from mesh import *
from material import *
from color import *
from perlin import *

class Missile(Object3d):
    missile_mesh = None
    missile_material = None    

    def __init__(self):
        if (Missile.missile_mesh == None):
            Missile.missile_mesh = Missile.create_missile_mesh()
            Missile.missile_material = Material(color(1,0,0,1), "MissileMaterial")

        super().__init__("Missile")
        
        self.position = vector3(0,random.uniform(0,3),12)
        r = random.uniform(0,100)
        if (r > 66):
            self.position.x = 7
            self.rotation = from_rotation_vector((vector3(0,1,0) * math.radians(90)).to_np3())
        elif (r > 33):
            self.position.y = -2
            self.position.x = random.uniform(-4,4)
            self.rotation = from_rotation_vector((vector3(1,0,0) * math.radians(90)).to_np3())
        else:
            self.position.x = -7
            self.rotation = from_rotation_vector((vector3(0,1,0) * math.radians(-90)).to_np3())

        self.mesh = Missile.missile_mesh
        self.material = Missile.missile_material
        self.missile_speed = 2
        self.missile_rotation_speed = 1.5 # radians per second

    def update(self, delta_time):
        velocity = self.forward() * self.missile_speed
        self.position += velocity * delta_time

        # Rotate missile towards the player
        current_dir = self.forward()
        desired_dir = (vector3(0,0,0) - self.position).normalized()
        dp = np.clip(dot_product(current_dir, desired_dir), -1, 1)
        angle = math.acos(dp)

        if (abs(angle) > self.missile_rotation_speed * delta_time):
            angle = self.missile_rotation_speed * delta_time * math.copysign(1, angle)

        axis = -cross_product(current_dir, desired_dir)

        q = from_rotation_vector((axis * angle).to_np3())
        self.rotation = self.rotation * q

    @staticmethod
    def create_missile_mesh():
        radius = 0.0125
        length = 0.075
        cone = 0.05
        missile_mesh = Mesh.create_cube((radius * 2, radius * 2, length * 2))
        missile_mesh = Mesh.create_tri(vector3(radius, radius, length), vector3(radius, -radius, length), vector3(0,0,length + cone), missile_mesh)
        missile_mesh = Mesh.create_tri(vector3(radius, -radius, length), vector3(-radius, -radius, length), vector3(0,0,length + cone), missile_mesh)
        missile_mesh = Mesh.create_tri(vector3(-radius, -radius, length), vector3(-radius, radius, length), vector3(0,0,length + cone), missile_mesh)
        missile_mesh = Mesh.create_tri(vector3(-radius, radius, length), vector3(radius, radius, length), vector3(0,0,length + cone), missile_mesh)

        return missile_mesh

class Shot(Object3d):
    shot_mesh = None
    shot_material = None    

    def __init__(self):
        if (Shot.shot_mesh == None):
            Shot.shot_mesh = Mesh.create_sphere((0.1,0.1,0.1), 4, 4)
            Shot.shot_material = Material(color(1,1,0,1), "ShotMaterial")

        super().__init__("Shot")
        
        self.position = vector3(0,0,0)
        self.mesh = Shot.shot_mesh
        self.material = Shot.shot_material
        self.shot_speed = 6
        self.direction = vector3(0,0,0)

    def update(self, delta_time):
        velocity = self.direction * self.shot_speed
        self.position += velocity * delta_time

# Computes the height of the terrain at the given x,y point
def sample_height(x, y):
    # 2 octave noise, with a given scale
    scale_noise = 0.4
    noise_height = 5
    n = noise_height * (0.5 * noise2d(x * scale_noise, y * scale_noise) + 0.25 * noise2d(x * scale_noise * 2, y * scale_noise * 2))
    if ((n < 0) or (y < 8)):
        n = 0

    return n

# Creates a terrain, composed of different meshes (one per each type of material)
# It support snow, water, grassland and cliffsize, based on hard-coded parameters
def create_terrain():
    # Size of the terrain
    size_x = 16
    size_z = 16
    # Number of divisions of the terrain. Vertex count scales with the square of this
    div = 40

    px = size_x / div
    pz = size_z / div

    # For centering the terrain on the object center
    origin = vector3(-size_x * 0.5, 0, 0)

    terrain_mesh = Mesh("Terrain")

    for dz in range(0, div):
        for dx in range(0, div):
            p1 = vector3(dx * px, 0, dz * pz) + origin
            p2 = vector3((dx + 1) * px, 0, dz * pz) + origin
            p3 = vector3((dx + 1) * px, 0, (dz + 1) * pz) + origin
            p4 = vector3(dx * px, 0, (dz + 1) * pz) + origin

            p1.y = sample_height(p1.x, p1.z)
            p2.y = sample_height(p2.x, p2.z)
            p3.y = sample_height(p3.x, p3.z)
            p4.y = sample_height(p4.x, p4.z)

            poly = []
            poly.append(p1)
            poly.append(p2)
            poly.append(p3)
            poly.append(p4)

            terrain_mesh.polygons.append(poly)

    # Create materials for the terrain
    terrain_material = Material(color(0.1,0.6,0.1,1), "TerrainMaterial")

    obj = Object3d("TerrainObject")
    obj.scale = vector3(1, 1, 1)
    obj.position = vector3(0, -1, 1)
    obj.mesh = terrain_mesh
    obj.material = terrain_material

    # Return object
    return obj

# Define a main function, just to keep things nice and tidy
def main():
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
    scene.camera.position -= vector3(0,0,0)

    # Creates the terrain meshes and materials
    terrain_object = create_terrain()
    scene.add_object(terrain_object)

    missile_spawn_time = 2
    missile_timer = missile_spawn_time
    missiles = []

    flash_color = color(0,0,0,0)
    total_flash_time = 0
    flash_timer = 0

    shot_cooldown = 0.2
    shot_timer = 0
    shots = []

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
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                if (shot_timer <= 0):
                    shot_timer = shot_cooldown

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos = ((mouse_pos[0] / res_x) * 2 - 1, (mouse_pos[1] / res_y) * 2 - 1)

                    shot = Shot()
                    shot.position, shot.direction = scene.camera.RayFromNDC(mouse_pos)

                    scene.add_object(shot)
                    shots.append(shot)

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,0))

        # Spawn new missiles
        missile_timer -= delta_time
        if (missile_timer < 0):
            missile_spawn_time -= 0.025
            if (missile_spawn_time < 0.5):
                missile_spawn_time = 0.5
            missile_timer = missile_spawn_time
            
            new_missile = Missile()
            scene.add_object(new_missile)
            missiles.append(new_missile)

        # Animate missiles
        missiles_to_destroy = []
        for missile in missiles:
            missile.update(delta_time)

            if (missile.position.z < 0.1):
                if (missile.position.magnitude() < 0.25):
                    flash_color = color(1,0,1,1)
                    total_flash_time = flash_timer = 1
                else:
                    # Mark for destruction
                    pass 
                # Destroy missile
                missiles_to_destroy.append(missile)
                scene.remove_object(missile)

        # Animate shots
        shots_to_destroy = []
        for shot in shots:
            shot.update(delta_time)

            if (shot.position.z > 12):
                # Destroy shot
                shots_to_destroy.append(shot)
                scene.remove_object(shot)

        # Update shot cooldown
        shot_timer -= delta_time

        # Check collisions
        for shot in shots:
            for missile in missiles:
                distance = vector3.distance(shot.position, missile.position)
                if (distance < 0.5):
                    missiles_to_destroy.append(missile)
                    scene.remove_object(missile)
                    shots_to_destroy.append(shot)
                    scene.remove_object(shot)
                    flash_color = color(0,1,1,1)
                    total_flash_time = flash_timer = 0.5

        # Actually delete objects
        missiles = [x for x in missiles if x not in missiles_to_destroy]
        shots = [x for x in shots if x not in shots_to_destroy]

        # Render scene
        scene.render(screen)

        # Render screen flash
        if (flash_timer > 0):
            flash_timer -= delta_time
            if (flash_timer > 0):         
                flash_color.a = flash_timer / total_flash_time       
                screen.fill(flash_color.premult_alpha().tuple3(), None, pygame.BLEND_RGB_ADD)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()

# Run the main function
main()
