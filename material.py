"""Material class definition"""

class Material:
    """Material class.
    Describe the properties of the mesh being drawn. Currently it only supports a
    Color and a line width.
    """
    def __init__(self, Color, name="UnknownMaterial"):
        """
        Arguments:

            Color {Color} -- Color of the line

            name {str} -- Name of the material, defaults to 'UnknownMaterial'
        """
        self.Color = Color
        """{Color} Color of the lines on the mesh"""
        self.name = name
        """{str} Name of this material"""
        self.line_width = 2
        """{int} Width of the lines on the mesh"""
