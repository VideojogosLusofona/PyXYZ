import numpy as np
from object3d import *

class Camera(Object3d):
    def __init__(self, ortho, res_x, res_y):
        super().__init__(self)

        self.ortho = ortho
        self.res_x = res_x
        self.res_y = res_y
        self.near_plane = 1
        self.far_plane = 100
        self.fov = math.radians(30)

    def get_projection_matrix(self):
        self.proj_matrix = np.zeros((4, 4))
        if (self.ortho):
            self.proj_matrix[0,0] = self.res_x * 0.5
            self.proj_matrix[1,1] = self.res_y * 0.5
            self.proj_matrix[3,0] = 0
            self.proj_matrix[3,1] = 0
            self.proj_matrix[3,3] = 1
        else:
            t = math.tan(self.fov)
            a = self.res_y / self.res_x
            self.proj_matrix[0,0] = 0.5 * self.res_x / t
            self.proj_matrix[1,1] = 0.5 * self.res_y / (a * t)
            self.proj_matrix[2,3] = 1
            self.proj_matrix[2,2] = self.far_plane / (self.far_plane - self.near_plane)
            self.proj_matrix[3,2] = self.proj_matrix[2,2] * self.near_plane

        return self.proj_matrix

    def get_camera_matrix(self):
        trans = np.identity(4)
        trans[3,0] = -self.position.x
        trans[3,1] = -self.position.y
        trans[3,2] = -self.position.z    

        qrot  = as_rotation_matrix(self.rotation.inverse())
        rotation_matrix = np.identity(4)
        rotation_matrix[0][0] = qrot[0][0]
        rotation_matrix[0][1] = qrot[0][1]
        rotation_matrix[0][2] = qrot[0][2]
        rotation_matrix[1][0] = qrot[1][0]
        rotation_matrix[1][1] = qrot[1][1]
        rotation_matrix[1][2] = qrot[1][2]
        rotation_matrix[2][0] = qrot[2][0]
        rotation_matrix[2][1] = qrot[2][1]
        rotation_matrix[2][2] = qrot[2][2]
        rotation_matrix[3,3] = 1

        return trans @ rotation_matrix

    def RayFromNDC(self, pos):

        vpos = vector3(pos[0], pos[1], self.near_plane)
        vpos.x =  vpos.x * self.res_x * 0.5
        vpos.y = -vpos.y * self.res_y * 0.5
        
        inv_view_proj_matrix = self.get_camera_matrix() @ self.get_projection_matrix()
        inv_view_proj_matrix = np.linalg.inv(inv_view_proj_matrix)

        dir = inv_view_proj_matrix @ vpos.to_np4(1)
        dir = vector3.from_np(dir).normalized()

        return self.position + dir * self.near_plane, dir
