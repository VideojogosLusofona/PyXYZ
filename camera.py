"""Camera class definition"""

import math
from quaternion import Quaternion
from vector3 import Vector3
from matrix4 import Matrix4
from object3d import Object3d

class Camera(Object3d):
    """Camera class.
    It allows us to have a viewport into the scene. Each scene has a camera set."""

    def __init__(self, ortho, res_x, res_y):
        """
        Arguments:
            ortho {bool} - True if this is an ortographic camera, false otherwise.

            res_x {int} - Horizontal resolution of the window. This will be the size of the window
            in ortographic view

            res_y {int} - Vertical resolution of the window. This will be the size of the window in
            ortographic view
        """
        super().__init__(self)

        self.ortho = ortho
        """{bool} True if this is an ortographic camera, false otherwise"""
        self.res_x = res_x
        """{int} Horizontal resolution of the window. This will be the size of the window in
        ortographic view"""
        self.res_y = res_y
        """{int} Vertical resolution of the window. This will be the size of the window in
        ortographic view"""
        self.near_plane = 1
        """{number} Distance from the camera to the near plane. Defaults to 1"""
        self.far_plane = 100
        """{number} Distance from the camera to the far plane. Defaults to 100"""
        self.fov = math.radians(60)
        """{number} Field of view angle (in radians) of the camera (if in perspective mode)"""
        self.proj_matrix = Matrix4.identity()
        """{Matrix4} Projection matrix. This is only set after get_projection_matrix is called
        once"""

    def get_projection_matrix(self):
        """Retrieves the projection matrix of this camera.
        This function sets up the proj_matrix attribute as well.

        Returns:
            Matrix4 - Projection matrix of this camera
        """
        self.proj_matrix = Matrix4.zeros()
        if self.ortho:
            self.proj_matrix[0, 0] = self.res_x * 0.5
            self.proj_matrix[1, 1] = self.res_y * 0.5
            self.proj_matrix[3, 0] = 0
            self.proj_matrix[3, 1] = 0
            self.proj_matrix[3, 3] = 1
        else:
            t = math.tan(self.fov * 0.5)
            a = self.res_y / self.res_x
            self.proj_matrix[0, 0] = 0.5 * self.res_x / t
            self.proj_matrix[1, 1] = 0.5 * self.res_y / (a * t)
            self.proj_matrix[2, 3] = 1
            self.proj_matrix[2, 2] = self.far_plane / (self.far_plane - self.near_plane)
            self.proj_matrix[3, 2] = self.proj_matrix[2, 2] * self.near_plane

        return self.proj_matrix

    def get_camera_matrix(self):
        """Retrieves the view matrix of this camera. This is basically the same as a PRS matrix
        without scalling, and with the position and rotation negated.

        Returns:
            Matrix4 - View matrix of this camera
        """
        trans = Matrix4.identity()
        trans[3, 0] = -self.position.x
        trans[3, 1] = -self.position.y
        trans[3, 2] = -self.position.z

        rotation_matrix = self.rotation.inverted().as_rotation_matrix()

        return trans * rotation_matrix

    def ray_from_ndc(self, pos):
        """Retrieves a ray (origin, direction) corresponding to the given position on screen.
        This function takes the coordinates as NDC (normalized device coordinates), in which the
        lower-left corner of the screen corresponds to (-1,-1) and the upper-right corresponds to
        (1,1).
        For example, to convert mouse coordinates to NDC, you could do something like:

        >>> mouse_pos = pygame.mouse.get_pos()
        >>> mouse_pos = ((mouse_pos[0] / res_x) * 2 - 1, (mouse_pos[1] / res_y) * 2 - 1)
        >>> origin, dir = camera.RayFromNDC(mouse_pos)

        Arguments:
            pos {2-tuple} -- Screen position in NDC (normalized device coordinates)

        Returns:
            Vector3, Vector3 - Origin and direction of the ray corresponding to that screen
            positions
        """

        vpos = Vector3(pos[0], pos[1], self.near_plane)
        vpos.x = vpos.x * self.res_x * 0.5
        vpos.y = -vpos.y * self.res_y * 0.5

        inv_view_proj_matrix = self.get_camera_matrix() * self.get_projection_matrix()
        inv_view_proj_matrix.invert()

        direction = inv_view_proj_matrix.posmultiply_v3(vpos, 1)
        direction = Vector3(direction.x, direction.y, direction.z).normalized()

        return self.position + direction * self.near_plane, direction
