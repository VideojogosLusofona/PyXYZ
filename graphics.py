import pygame

class Graphics:
    screen = None

    @staticmethod
    def init(res):
        pygame.init()

        # Create a window and a display surface
        Graphics.screen = pygame.display.set_mode(res)

    @staticmethod
    def present():
        pygame.display.flip()

    @staticmethod
    def set_mouse_visible(b):
        pygame.mouse.set_visible(b)
 
    @staticmethod
    def set_mouse_grab(b):
        pygame.event.set_grab(b)
      
    @staticmethod
    def clear_screen(color):
        Graphics.screen.fill(color.to_tuple3())

    @staticmethod
    def clear_screen_with_alpha(color):
        Graphics.screen.fill(color.premult_alpha().to_tuple3(), None, pygame.BLEND_RGB_ADD)

    @staticmethod
    def draw_wireframe_polygon(color, polygons, line_width):
        pygame.draw.polygon(Graphics.screen, color.to_tuple3(), polygons, line_width)

    @staticmethod
    def draw_filled_polygon(color, polygons):
        pygame.draw.polygon(Graphics.screen, color.to_tuple3(), polygons, 0)

