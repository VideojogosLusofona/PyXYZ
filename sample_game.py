"""Game sample application"""
import math
import random

from application import Application
from input import Input
from graphics import Graphics
from object3d import Object3d
from mesh import Mesh
from material import Material
from color import Color
from vector3 import Vector3, dot_product, cross_product
from quaternion import Quaternion
from perlin import noise2d

class Missile(Object3d):
    """Missile class.
    The missile will launch from a random position (defined on instancing) and will direct itself
    towards the player.
    """
    missile_mesh = None
    """Mesh used by all the missiles, so we don't create a new one every single missile"""
    missile_material = None
    """Material used by all the missiles, so we don't create a new one every single missile"""

    def __init__(self):
        if Missile.missile_mesh is None:
            Missile.missile_mesh = Missile.create_missile_mesh()
            Missile.missile_material = Material(Color(1, 0, 0, 1), "MissileMaterial")

        super().__init__("Missile")

        # Determine the spawn position. There's 33% chance it comes from the right, 33% that it
        # comes from behind the mountains, and 34% chance it comes from the left
        self.position = Vector3(0, random.uniform(0, 3), 12)
        r = random.uniform(0, 100)
        if r > 66:
            self.position.x = 7
            self.rotation = Quaternion.AngleAxis(Vector3(0, 1, 0), math.radians(-90))
        elif r > 33:
            self.position.y = -2
            self.position.x = random.uniform(-4, 4)
            self.rotation = Quaternion.AngleAxis(Vector3(1, 0, 0), math.radians(-90))
        else:
            self.position.x = -7
            self.rotation = Quaternion.AngleAxis(Vector3(0, 1, 0), math.radians(90))

        # Set the mesh and material of the missile
        self.mesh = Missile.missile_mesh
        self.material = Missile.missile_material
        # Sets the missile linear speed
        self.missile_speed = 2
        # Sets the rotation speed (in radians per second)
        self.missile_rotation_speed = 0.75

    def update(self, delta_time):
        """Animates the missile."""
        # Moves missile based on its direction (the forward vector)
        velocity = self.forward() * self.missile_speed
        self.position += velocity * delta_time

        # Rotate missile towards the player - Figure out where it is pointing and
        # where do we want to point it
        current_dir = self.forward()
        desired_dir = (Vector3(0, 0, 0) - self.position).normalized()
        # Find the angle between these two directions
        dp = max(-1, min(1, dot_product(current_dir, desired_dir)))
        angle = math.acos(dp)

        # If the angle is larger than the ammount we can rotate a single frame,
        # given by the time elapsed and the missile rotation speed, we need to
        # clamp the value of the angle
        if abs(angle) > self.missile_rotation_speed * delta_time:
            angle = self.missile_rotation_speed * delta_time * math.copysign(1, angle)

        # Figure out the rotation axis to point the missile towards the desired direction
        axis = cross_product(current_dir, desired_dir)
        axis.normalize()

        if (angle > 0.01):
            # Rotate the missile towards the player
            q = Quaternion.AngleAxis(axis, angle)
            self.rotation = q * self.rotation

    @staticmethod
    def create_missile_mesh():
        """Creates the missile mesh, which is just a quadrilateral prism and a pointy end"""
        radius = 0.0125
        length = 0.075
        cone = 0.05
        missile_mesh = Mesh.create_cube((radius * 2, radius * 2, length * 2))
        missile_mesh = Mesh.create_tri(Vector3(radius, radius, length),
                                       Vector3(radius, -radius, length),
                                       Vector3(0, 0, length + cone), missile_mesh)
        missile_mesh = Mesh.create_tri(Vector3(radius, -radius, length),
                                       Vector3(-radius, -radius, length),
                                       Vector3(0, 0, length + cone), missile_mesh)
        missile_mesh = Mesh.create_tri(Vector3(-radius, -radius, length),
                                       Vector3(-radius, radius, length),
                                       Vector3(0, 0, length + cone), missile_mesh)
        missile_mesh = Mesh.create_tri(Vector3(-radius, radius, length),
                                       Vector3(radius, radius, length),
                                       Vector3(0, 0, length + cone), missile_mesh)

        return missile_mesh

class Shot(Object3d):
    """Shot class.
    A shot will be a sphere moving towards the forward direction continuously.
    """
    shot_mesh = None
    """Mesh used by all the shots, so we don't create a new one every single shot"""
    shot_material = None
    """Material used by all the shots, so we don't create a new one every single shot"""

    def __init__(self):
        if Shot.shot_mesh is None:
            Shot.shot_mesh = Mesh.create_sphere((0.1, 0.1, 0.1), 4, 4)
            Shot.shot_material = Material(Color(1, 1, 0, 1), "ShotMaterial")

        super().__init__("Shot")

        # The position and direction will be overwritten by the code that spawns the shot
        self.position = Vector3(0, 0, 0)
        self.mesh = Shot.shot_mesh
        self.material = Shot.shot_material
        self.shot_speed = 6
        self.direction = Vector3(0, 0, 0)

    def update(self, delta_time):
        """Animates the missile."""
        # Moves the shot in the direction set
        velocity = self.direction * self.shot_speed
        self.position += velocity * delta_time

class SampleGame(Application):
    def __init__(self):
        self.res = (1280,720)

    # Computes the height of the terrain at the given x,y point
    @staticmethod
    def sample_height(x, y):
        """Samples a pseudo heighmap, built with 2-octaves of 2d perlin noise. This is
        clamped near the player, so we have a nice flat area near him. We also clamp it to
        values above 0, so it looks more natural"""
        # 2 octave noise, with a given scale
        scale_noise = 0.4
        noise_height = 5
        n = 0.5 * noise2d(x * scale_noise, y * scale_noise)
        n += 0.25 * noise2d(x * scale_noise * 2, y * scale_noise * 2)
        n *= noise_height
        if ((n < 0) or (y < 8)):
            n = 0

        return n

    @staticmethod
    def create_terrain():
        """Creates a terrain to use as a background in the game"""
        # Size of the terrain
        size_x = 16
        size_z = 16
        # Number of divisions of the terrain. Vertex count scales with the square of this
        div = 20

        px = size_x / div
        pz = size_z / div

        # For centering the terrain on the object center
        origin = Vector3(-size_x * 0.5, 0, 0)

        terrain_mesh = Mesh("Terrain")

        # Create the geometry of the terrain and add it to the mesh
        for dz in range(0, div):
            for dx in range(0, div):
                p1 = Vector3(dx * px, 0, dz * pz) + origin
                p2 = Vector3((dx + 1) * px, 0, dz * pz) + origin
                p3 = Vector3((dx + 1) * px, 0, (dz + 1) * pz) + origin
                p4 = Vector3(dx * px, 0, (dz + 1) * pz) + origin

                p1.y = SampleGame.sample_height(p1.x, p1.z)
                p2.y = SampleGame.sample_height(p2.x, p2.z)
                p3.y = SampleGame.sample_height(p3.x, p3.z)
                p4.y = SampleGame.sample_height(p4.x, p4.z)

                poly = []
                poly.append(p1)
                poly.append(p2)
                poly.append(p3)
                poly.append(p4)

                terrain_mesh.polygons.append(poly)

        # Create materials for the terrain
        terrain_material = Material(Color(0.1, 0.6, 0.1, 1), "TerrainMaterial")

        # Create object to display the terrain
        obj = Object3d("TerrainObject")
        obj.scale = Vector3(1, 1, 1)
        obj.position = Vector3(0, -1, 1)
        obj.mesh = terrain_mesh
        obj.material = terrain_material

        return obj

    def init_scene(self):
        # Creates the terrain meshes and materials
        terrain_object = SampleGame.create_terrain()
        self.scene.add_object(terrain_object)

        # Game variables
        # A missile spawns every 2 seconds (this time gets smaller every missile, to
        # make the game harder with time)
        self.missile_spawn_time = 2
        # Time until the next missile is shot
        self.missile_timer = self.missile_spawn_time
        # Storage for all missiles active in the game
        self.missiles = []

        # Flashing effect Color
        self.flash_color = Color(0, 0, 0, 0)
        # Total time of the current flash
        self.total_flash_time = 0
        # Time elapsed for the current flash
        self.flash_timer = 0

        # Minimum time between player shots
        self.shot_cooldown = 0.2
        # Timer for the shot cooldown
        self.shot_timer = 0
        # Storage for all the shots active in the game
        self.shots = []

    def update(self, delta_time):
        # Spawn new missiles
        self.missile_timer -= delta_time
        if self.missile_timer < 0:
            # It's time to spawn a new missile
            # Reduce time until the next missile, but clamp it so we don't have more than
            # one missile every half a second
            self.missile_spawn_time -= 0.025
            if self.missile_spawn_time < 0.5:
                self.missile_spawn_time = 0.5
            # Reset the timer
            self.missile_timer = self.missile_spawn_time

            # Create a new missile
            new_missile = Missile()
            # Add the missile to the scene (for rendering) and on the missile storage,
            # for all other operations
            self.scene.add_object(new_missile)
            self.missiles.append(new_missile)

        # Animate missiles
        # We need the following to keep track of all missiles we'll have to destroy,
        # since we can't change the storage while we're iterating it
        missiles_to_destroy = []
        for missile in self.missiles:
            # Update the missile
            missile.update(delta_time)

            # Check if the missile is close to the player plane (z < 0.1)
            if missile.position.z < 0.1:
                # Check if the missile is close enough to the player to hit him
                if missile.position.magnitude() < 0.25:
                    # It has hit the player, flash the screen red for one second
                    self.flash_color = Color(1, 0, 1, 1)
                    self.total_flash_time = self.flash_timer = 1
                # Destroy missile (remove it from the scene and add it to the destruction
                # list so we can remove it in a bit)
                missiles_to_destroy.append(missile)
                self.scene.remove_object(missile)

        # Animate shots
        # We need the following to keep track of all shots we'll have to destroy,
        # since we can't change the storage while we're iterating it
        shots_to_destroy = []
        for shot in self.shots:
            # Update the shot
            shot.update(delta_time)

            # Check if the shot is too far away, and add it to the destruction list,
            # besides removing it from the scene
            if shot.position.z > 12:
                # Destroy shot
                shots_to_destroy.append(shot)
                self.scene.remove_object(shot)

        # Update shot cooldown
        self.shot_timer -= delta_time

        # Check collisions
        for shot in self.shots:
            # Check each shot with each missile
            for missile in self.missiles:
                # Check the distance between the shot and the missile, it it is below
                # a threshould (in this case 0.5), destroy the missile and the shot
                distance = Vector3.distance(shot.position, missile.position)
                if distance < 0.5:
                    # Add it to the missile destruction list, and remove it from the scene
                    missiles_to_destroy.append(missile)
                    self.scene.remove_object(missile)
                    # Add it to the shot destruction list, and remove it from the scene
                    shots_to_destroy.append(shot)
                    self.scene.remove_object(shot)
                    # Flash the screen cyan for 0.5 seconds
                    self.flash_color = Color(0, 1, 1, 1)
                    self.total_flash_time = self.flash_timer = 0.5

        # Actually delete objects
        self.missiles = [x for x in self.missiles if x not in missiles_to_destroy]
        self.shots = [x for x in self.shots if x not in shots_to_destroy]

        # Update screen flash
        if self.flash_timer > 0:
            self.flash_timer -= delta_time
            if self.flash_timer > 0:
                self.flash_color.a = self.flash_timer / self.total_flash_time

    def on_button_down(self):
        # If the user has the mouse button down
        if self.shot_timer <= 0:
            # We're not on cooldown, so we can shoot

            # Get the mouse position and convert it to NDC (normalized
            # device coordinates)
            w,h = self.res
            mouse_pos = Input.get_mouse_pos()
            mouse_pos = ((mouse_pos[0] / w) * 2 - 1, (mouse_pos[1] / h) * 2 - 1)

            # Create a shot
            shot = Shot()
            # Initialize the position and direction of the shot, based on the
            # mouse position on the screen. For this, we request the scene camera the
            # ray corresponding to the mouse position
            shot.position, shot.direction = self.scene.camera.ray_from_ndc(mouse_pos)

            # Add the shot to the scene (for rendering) and on the shot storage, for
            # all other operations
            self.scene.add_object(shot)
            self.shots.append(shot)

            # Reset the cooldown
            self.shot_timer = self.shot_cooldown

    def render(self):
        if (self.flash_timer > 0):
            # Render the full screen rectangle, using additive blend
            Graphics.clear_screen_with_alpha(self.flash_color)

app = SampleGame()
app.run()
