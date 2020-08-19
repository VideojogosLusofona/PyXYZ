from camera import *

class Scene:
    def __init__(self, name):
        self.name = name
        self.camera = Camera(True, 640, 480)
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self, screen):

        camera_matrix = self.camera.get_camera_matrix()
        projection_matrix = self.camera.get_projection_matrix()

        clip_matrix = camera_matrix @ projection_matrix

        for obj in self.objects:
            obj.render(screen, clip_matrix)

