"""Material class definition"""

class Material:
    """Material class.
    Describe the properties of the mesh being drawn. Currently it only supports a
    color and a line width.
    """
    def __init__(self, color, name="UnknownMaterial"):
        """
        Arguments:

            color {color} -- Color of the line

            name {str} -- Name of the material, defaults to 'UnknownMaterial'
        """
        self.color = color
        """{color} Color of the lines on the mesh"""
        self.name = name
        """{str} Name of this material"""
        self.line_width = 2
        """{int} Width of the lines on the mesh"""
