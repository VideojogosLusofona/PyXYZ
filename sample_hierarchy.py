"""Hierarchy sample application"""
import math

from application import Application
from object3d import Object3d
from mesh import Mesh
from material import Material
from color import Color
from vector3 import Vector3
from quaternion import Quaternion

class SampleHierarchy(Application):
    def init_scene(self):
        # Moves the camera back 2 units
        self.scene.camera.position -= Vector3(0, 0, 2)

        # Create a cube and place it in a scene, at position (0,0,0)
        self.obj1 = Object3d("TestObject")
        self.obj1.scale = Vector3(1, 1, 1)
        self.obj1.position = Vector3(0, 0, 2)
        self.obj1.mesh = Mesh.create_cube((1, 1, 1))
        self.obj1.material = Material(Color(1, 0, 0, 1), "TestMaterial1")
        self.scene.add_object(self.obj1)

        # Create a second object, and add it as a child of the first object
        # When the first object rotates, this one will also mimic the transform
        self.obj2 = Object3d("ChildObject")
        self.obj2.position += Vector3(0, 0.75, 0)
        self.obj2.mesh = Mesh.create_cube((0.5, 0.5, 0.5))
        self.obj2.material = Material(Color(0, 1, 0, 1), "TestMaterial2")
        self.obj1.add_child(self.obj2)

        # Specify the rotation of the object. It will rotate 15 degrees around the axis given,
        # every second
        self.angle = 15
        self.axis = Vector3(1, 0.7, 0.2)
        self.axis.normalize()

    def update(self, delta_time):
        # Rotates the object, considering the time passed (not linked to frame rate)
        q = Quaternion.AngleAxis(self.axis, math.radians(self.angle) * delta_time)
        self.obj1.rotation = q * self.obj1.rotation

app = SampleHierarchy()
app.run()

