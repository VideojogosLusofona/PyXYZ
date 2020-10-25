import pygame
import time

from graphics import Graphics
from camera import Camera
from scene import Scene
from input import Input
from color import Color

class Application:
    # Define the size/resolution of our window
    res = (640, 480)
    # Define the clear color
    clear_color = Color(0, 0, 0)
    # Current running application
    current_application = None

    def init(self):
        # Initializes graphics
        Graphics.init(self.res)

        # Create a scene
        self.scene = Scene("Main")
        self.scene.camera = Camera(False, self.res[0], self.res[1])

        # Initializes the scene on this application
        self.init_scene()

    def run(self):
        Application.current_application = self

        self.exit = False

        # Initialize application
        self.init()

        # Timer
        delta_time = 0
        prev_time = time.time()

        # Show mouse cursor
        Graphics.set_mouse_visible(True)

        # Don't grab the mouse
        Graphics.set_mouse_grab(False)

        # Game loop, runs forever
        while not self.exit:
            # Reset this frames benchmarks
            #Mesh.stat_vertex_count = 0
            #Mesh.stat_transform_time = 0
            #Mesh.stat_render_time = 0

            # Process OS events - This gets events from pygame and processes them
            # by dispatching them to the correct handlers
            for event in pygame.event.get():
                # Checks if the user closed the window
                if event.type == pygame.QUIT:
                    # Exits the application immediately
                    return
                elif event.type == pygame.KEYDOWN:
                    self.on_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.on_key_up(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_button_down()

            # Clears the screen with a very dark blue (0, 0, 20)
            Graphics.clear_screen(self.clear_color)

            # Update the scene
            self.update(delta_time)

            # Writes the benchmarks results
            #print("Frame stats:")
            #print(f"Vertex count = {Mesh.stat_vertex_count}")
            #print(f"Transform time = {Mesh.stat_transform_time}s")
            #print(f"Render time = {Mesh.stat_render_time}s")

            # Render the scene
            self.scene.render()

            # Render any extra elements
            self.render()

            # Swaps the back and front buffer, effectively displaying what we rendered
            Graphics.present()

            # Updates the timer, so we we know how long has it been since the last frame
            delta_time = time.time() - prev_time
            prev_time = time.time()

            # Write frame time
            #print(f"Frame time = {delta_time}s")

        Application.current_application = None

    def set_exit(self, b, code = 0):
        self.exit = b
        self.exit_code = code

    @staticmethod
    def get_resolution():
        return Application.current_application.res

    def init_scene(self):
        print("Application.init_scene should be implemented!")

    def update(self, delta_time):
        print("Application.update should be implemented!")

    def render(self):
        pass

    def on_key_up(self, key):
        if key == Input.K_ESCAPE:
            self.set_exit(True)

    def on_key_down(self, key):
        pass

    def on_button_down(self):
        pass