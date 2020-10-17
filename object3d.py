"""3d Object class"""

from quaternion import Quaternion
from vector3 import Vector3
from vector4 import Vector4
from matrix4 import Matrix4

class Object3d:
    """3d object class.
    This is the base class of all objects added to the scene graph.
    """
    def __init__(self, name):
        """
        Arguments:

            name {str} -- Name of the object
        """
        self.name = name
        """ {str} Name of the object"""
        self.position = Vector3()
        """ {Vector3} Local position of the object (relative to parent)"""
        self.rotation = Quaternion.identity()
        """ {quaternion} Local rotation of the object {relative to parent)"""
        self.scale = Vector3(1, 1, 1)
        """ {Vector3} Local scale of the object (relative to parent)"""
        self.mesh = None
        """ {Mesh} Mesh to be rendered in this object"""
        self.material = None
        """ {Material} Material to be used rendering this object"""
        self.children = []
        """ {List[Object3d]} Children objects of this object"""

    def get_matrix(self):
        """
        Retrieves the local transformation matrix of this object

        Returns:

            {Matrix4} -- Local transformation matrix
        """
        return Object3d.get_prs_matrix(self.position, self.rotation, self.scale)

    def render(self, screen, clip_matrix):
        """
        Renders this object with the given clip_matrix.

        Arguments:

            screen {pygame.Surface} -- Pygame surface in which this object will be rendered

            clip_matrix {Matrix4} -- Parent transformation matrix (including view and projection
            matrix)
        """

        # Retrieve the local transformation matrix
        world_matrix = self.get_matrix()

        # Multiply the local transformation with the clip matrix (transformation compositing)
        mesh_matrix = world_matrix * clip_matrix

        # If there's a mesh and a material
        if ((self.material is not None) and (self.mesh is not None)):
            self.mesh.render(screen, mesh_matrix, self.material)

        # Traverse the children of this object, rendering them
        for child in self.children:
            child.render(screen, mesh_matrix)

    def add_child(self, obj):
        """
        Adds a child object to the hierarchy of this one

        Arguments:

            obj {Object3d} -- Object to add to the hierarchy
        """
        self.children.append(obj)

    def remove_child(self, obj):
        """
        Removes a child object from the hierarchy of this one. If the object isn't a child of
        this one, nothing happens

        Arguments:

            obj {Object3d} -- Object to remove from the hierarchy
        """
        if obj in self.children:
            self.children.remove(obj)

    def get_position(self):
        """
        Retrieves the local position of this object. You can use self.position instead, this
        method actually computes the transfomation matrix and multiplies the 4d vector (0,0,0,1)
        by it. Results should be very similar.

        Returns:

            {Vector3} - Local position of the object
        """
        v = self.get_matrix() * Vector4(0, 0, 0, 1)
        return Vector3(v.x, v.y, v.z)

    def forward(self):
        """
        Retrieves the local forward vector of this object. The forward vector is defined as
        being the z-positive vector multiplied with the local transformation matrix

        Returns:

            {Vector3} - Local forward vector of the object
        """
        v = self.get_matrix() * Vector4(0, 0, 1, 0)
        return Vector3(v.x, v.y, v.z)

    def up(self):
        """
        Retrieves the local up vector of this object. The up vector is defined as being
        the y-positive vector multiplied with the local transformation matrix

        Returns:

            {Vector3} - Local up vector of the object
        """
        v = self.get_matrix() * Vector4(0, 1, 0, 0)
        return Vector3(v.x, v.y, v.z)

    def right(self):
        """
        Retrieves the local right vector of this object. The right vector is defined as being
        the x-positive vector multiplied with the local transformation matrix

        Returns:

            {Vector3} - Local right vector of the object
        """
        v = self.get_matrix() * Vector4(1, 0, 0, 0)
        return Vector3(v.x, v.y, v.z)

    @staticmethod
    def get_prs_matrix(position, rotation, scale):
        """
        Creates a PRS matrix from the given position, rotation and scale

        Arguments:

            position {Vector3} - Position

            rotation {quaternion} - Rotation

            scale {Vector3} - Scale

        Returns:

            {Matrix4} - PRS matrix
        """
        trans = Matrix4.identity()
        trans[3][0] = position.x
        trans[3][1] = position.y
        trans[3][2] = position.z

        rotation_matrix = rotation.as_rotation_matrix()

        scale_matrix = Matrix4.identity()
        scale_matrix[0][0] = scale.x
        scale_matrix[1][1] = scale.y
        scale_matrix[2][2] = scale.z

        return scale_matrix * rotation_matrix * trans
