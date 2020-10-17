"""Scene class definition"""
from camera import Camera

class Scene:
    """Scene class.
    It handles a scene, storing a list of objects and a camera/viewpoint"""
    def __init__(self, name):
        """
        Arguments:

            name {str} -- Name of the material, defaults to 'UnknownMesh'
        """
        self.name = name
        """ {str} Name of the scene"""
        self.camera = Camera(True, 640, 480)
        """ {Camera} Camera linked to this scene"""
        self.objects = []
        """ {List[Object3d]} List of 3d objects on the scene"""

    def add_object(self, obj):
        """Adds a 3d object to the scene.

        Arguments:

            obj {Object3d} -- 3d object to add to the scene
        """
        if obj not in self.objects:
            self.objects.append(obj)

    def remove_object(self, obj):
        """Removes a 3d object from the scene. This function does not scan the child objects,
        so it's only used to remove objects at the root level. If the object is not at the root
        level of the scene, nothing happens

        Arguments:

            obj {Object3d} -- 3d object to remove from the scene
        """
        if obj in self.objects:
            self.objects.remove(obj)

    def render(self, screen):
        """Renders this scene on the given target

        Arguments:

            screen {pygame.Surface} -- Pygame surface where the scene should be drawn
        """
        # Create clip matrix to be passed to the root-level objects, so they can be drawn
        camera_matrix = self.camera.get_camera_matrix()
        projection_matrix = self.camera.get_projection_matrix()

        clip_matrix = camera_matrix * projection_matrix

        # Render all root-level objects
        for obj in self.objects:
            obj.render(screen, clip_matrix)
            