"""Color class definition"""

import math

class InvalidColorOperationException(Exception):
    """Exception thrown when there's an invalid operation with colors"""
    def __init__(self, op, type1, type2):
        super().__init__(self)
        self.op = op
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        """Returns a readable version of the exception"""
        return f"Invalid color operation ({self.op}) between {self.type1} and {self.type2}!"

class color:
    """Color class.
    It stores RGBA values as floats, in a range from 0 to 1.
    """
    def __init__(self, r=0, g=0, b=0, a=1):
        """
        Arguments:

            r {number} -- Red component, [0..1], defaults to 0

            g {number} -- Green component, [0..1], defaults to 0

            b {number} -- Blue component, [0..1], defaults to 0

            a {number} -- Alpha component, [0..1], defaults to 1
        """
        self.r = r
        """{number} Red component. Should be in the [0..1] range, although there is no
        guarantees"""
        self.g = g
        """{number} Green component. Should be in the [0..1] range, although there is no
        guarantees"""
        self.b = b
        """{number} Blue component. Should be in the [0..1] range, although there is no
        guarantees"""
        self.a = a
        """{number} Alpha component. Should be in the [0..1] range, although there is no
        guarantees. Note that most Pygame functions don't use the alpha component, unless
        stated otherwise, and even so it might require extra setup."""

    def __str__(self):
        """Converts the color to a displayable string

        Returns:
            String - Color in text format (r,g,b,a)"""
        return f"({self.r},{self.g},{self.b},{self.a})"

    def __add__(self, c):
        """Adds this color to another. No validation of the output is done, i.e. any component
        can overflow. If we try to add anything other than a color to a color, it throws the
        InvalidColorOperationException.

        Arguments:
            c {color} -- Color to add

        Returns:
            Color - Sum of this color and the given one
        """
        if isinstance(c, color):
            return color(self.r + c.r, self.g + c.g, self.b + c.b, self.a + c.a)
        else:
            raise InvalidColorOperationException("add", type(self), type(c))

    def __sub__(self, c):
        """Subtracts a color to this color. No validation of the output is done, i.e.
        any component can underflow. If we try to subtract anything other than a color to
        a color, it throws the InvalidColorOperationException.

        Arguments:
            c {color} -- Color to subtract

        Returns:
            Color - Subraction of the given color from this color
        """
        if isinstance(c, color):
            return color(self.r - c.r, self.g - c.g, self.b - c.b, self.a - c.a)
        else:
            raise InvalidColorOperationException("sub", type(self), type(c))

    def __mul__(self, c):
        """Multiplies this color by another color or a scalar. No validation of the output
        is done, i.e. any component can underflow. If we try to multiply anything other than a
        color or a scalar, it throws the InvalidColorOperationException.

        Arguments:
            c {color} -- Color to multiply: a component-wise multiplication is done
            or
            c {number} -- Scalar to multiply: all components of the color are multiplied by
            this number

        Returns:
            Color - Multiplication of the color
        """
        if isinstance(c, (int, float)):
            return color(self.r * c, self.g * c, self.b * c, self.a * c)
        elif isinstance(c, color):
            return color(self.r * c.r, self.g * c.g, self.b * c.b, self.a * c.a)
        else:
            raise InvalidColorOperationException("mult", type(self), type(c))

    def __truediv__(self, c):
        """Divides this color by a scalar. No validation of the output is done, i.e. any
        component can underflow. If we try to divide anything other than a scalar, it throws
        the InvalidColorOperationException.

        Arguments:
            c {number} -- Scalar to divide: all components of the color are divided by this
            number

        Returns:
            Color - Color divided by the number
        """
        if isinstance(c, (int, float)):
            return color(self.r / c, self.g / c, self.b / c, self.a / c)
        else:
            raise InvalidColorOperationException("mult", type(self), type(c))

    def __eq__(self, c):
        """Checks if this color is equal to the given one, with a tolerance of 0.0001.
        Exception InvalidColorOperationException is raised if we compare something other
        than a color.

        Arguments:
            c {color} -- Color to compare

        Returns:
            Bool - True if the colors are the same, false otherwise
        """
        if isinstance(c, color):
            return ((self - c).magnitude()) < 0.0001
        else:
            raise InvalidColorOperationException("eq", type(self), type(c))

    def __ne__(self, c):
        """Checks if this color is different to the given one, with a tolerance of 0.0001.
        Exception InvalidColorOperationException is raised if we compare something other
        than a color.

        Arguments:
            c {color} -- Color to compare

        Returns:
            Bool - True if the colors are different, false otherwise
        """
        if isinstance(c, color):
            return ((self - c).magnitude()) > 0.0001
        else:
            raise InvalidColorOperationException("neq", type(self), type(c))

    def __isub__(self, c):
        """Subtracts a color to this color. No validation of the output is done, i.e.
        any component can underflow. If we try to subtract anything other than a color to
        a color, it throws the InvalidColorOperationException.

        Arguments:
            c {color} -- Color to subtract

        Returns:
            Color - Subraction of the given color from this color
        """
        return self - c

    def __iadd__(self, c):
        """Adds this color to another. No validation of the output is done, i.e. any component
        can overflow. If we try to add anything other than a color to a color, it throws the
        InvalidColorOperationException.

        Arguments:
            c {color} -- Color to add

        Returns:
            Color - Sum of this color and the given one
        """
        return self + c

    def __imul__(self, c):
        """Multiplies this color by another color or a scalar. No validation of the output
        is done, i.e. any component can underflow. If we try to multiply anything other than
        a color or a scalar, it throws the InvalidColorOperationException.

        Arguments:
            c {color} -- Color to multiply: a component-wise multiplication is done
            or
            c {number} -- Scalar to multiply: all components of the color are multiplied by this
            number

        Returns:
            Color - Multiplication of the color
        """
        return self * c

    def __idiv__(self, c):
        """Divides this color by a scalar. No validation of the output is done, i.e. any
        component can underflow. If we try to divide anything other than a scalar, it
        throws the InvalidColorOperationException.

        Arguments:
            c {number} -- Scalar to divide: all components of the color are divided by this number

        Returns:
            Color - Color divided by the number
        """
        return self / c

    def __neg__(self):
        """Inverts this color. All components except for alpha are inverted.

        Returns:
            Color - Color (1-r, 1-g, 1-b, a)
        """
        return color(1-self.r, 1-self.g, 1-self.b, self.a)

    def magnitude(self):
        """Returns the magnitude of the color.

        Returns:
            Number - Magnitude of the color as a 4D vector
        """
        return math.sqrt(self.dot(self))

    def dot(self, c):
        """Computes the dot product of this color with another.
        If we try to do this operation with anything other than a color, it throws the
        InvalidColorOperationException.

        Arguments:
            c {color} -- Color to do the dot product with

        Returns:
            Number - Scalar value corresponding to the dot product of both colors
        """
        if isinstance(c, color):
            return self.r * c.r + self.g * c.g + self.b * c.b + self.a * c.a
        else:
            raise InvalidColorOperationException("dot", type(self), type(c))

    def normalize(self):
        """Normalizes this color, as if it was a 4D vector.
        """
        d = 1.0 / self.magnitude()
        self.r *= d
        self.g *= d
        self.b *= d
        self.a *= d

    def normalized(self):
        """Returns the normalized version of this color, treating it as a 4D vector.

        Returns:
            Color - Normalized color
        """
        d = 1.0 / self.magnitude()
        return color(self.r * d, self.g * d, self.b * d, self.a * d)

    def premult_alpha(self):
        """Multiplies the RGB components with the alpha component, for use with pre-multiplied
        alpha blend mode and returns this new color.

        Returns:
            Color - Premultiplied color
        """
        return color(self.r * self.a, self.g * self.a, self.b * self.a, self.a)

    def tuple3(self):
        """Converts a color to a 3-tuple, to be used with Pygame

        Returns:
            Tuple - (r * 255, g * 255, b * 255)
        """
        return (self.r * 255, self.g * 255, self.b * 255)

    def tuple4(self):
        """Converts a color to a 4-tuple, to be used with Pygame

        Returns:
            Tuple - (r * 255, g * 255, b * 255, a * 255)
        """
        return (self.r * 255, self.g * 255, self.b * 255, self.a * 255)

    def saturate(self):
        """Clamps all the color components between the valid [0..1] range
        """
        self.r = min(max(self.r, 0), 1)
        self.g = min(max(self.g, 0), 1)
        self.b = min(max(self.b, 0), 1)
        self.a = min(max(self.a, 0), 1)

    def saturated(self):
        """Returns a clamped version of this color

        Returns:
            Color - Clamped color
        """
        return color(
            min(max(self.r, 0), 1),
            min(max(self.g, 0), 1),
            min(max(self.b, 0), 1),
            min(max(self.a, 0), 1)
        )
