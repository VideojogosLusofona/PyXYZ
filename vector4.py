"""4d vector class and helper functions"""
import math
import vector3
import matrix4

class InvalidVec4OperationException(Exception):
    """Exception thrown when there's an invalid operation with vectors"""
    def __init__(self, op, type1, type2):
        super().__init__(self)
        self.op = op
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        """Returns a readable version of the exception"""
        return f"Invalid Vector4 operation ({self.op}) between {self.type1} and {self.type2}!"

class Vector4:
    """4d vector class.
    It stores XYZW values as floats."""

    def __init__(self, x=0, y=0, z=0, w = 0):
        """
        Arguments:
            x {number} -- X component,defaults to 0

            y {number} -- Y component, defaults to 0

            z {number} -- Z component, defaults to 0

            w {number} -- W component, defaults to 0
        """
        self.x = x
        """{number} - X component"""
        self.y = y
        """{number} - Y component"""
        self.z = z
        """{number} - Z component"""
        self.w = w
        """{number} - W component"""            

    def __str__(self):
        """Converts the 4d vector to a displayable string

        Returns:
            String - Vector in text format (x,y,z,w)"""
        return f"({self.x},{self.y},{self.z},{self.w})"

    def __add__(self, v):
        """Adds this Vector4 to another.
        If we try to add anything other than a Vector4 to it, it throws the
        InvalidVec4OperationException.

        Arguments:
            v {Vector4} -- Vector to add

        Returns:
            Vector4 - Sum of this Vector4 and the given one
        """
        if isinstance(v, Vector4):
            return Vector4(self.x + v.x, self.y + v.y, self.z + v.z, self.w + v.w)
        else:
            raise InvalidVec4OperationException("add", type(self), type(v))

    def __sub__(self, v):
        """Subtracts a Vector4 from this one.
        If we try to subtract anything other than a Vector4, it throws the
        InvalidVec4OperationException.

        Arguments:
            v {Vector4} -- Vector to subtract

        Returns:
            Vector4 - Subraction of the given vector from this one
        """
        if isinstance(v, Vector4):
            return Vector4(self.x - v.x, self.y - v.y, self.z - v.z, self.w - v.w)
        else:
            raise InvalidVec4OperationException("sub", type(self), type(v))

    def __mul__(self, v):
        """Multiplies this Vector4 by a scalar.
        If we try to multiply anything other than a scalar, it throws the
        InvalidVec4OperationException.

        Arguments:
            v {number} -- Scalar to multiply: all components of the vector are
            multiplied by this number

        Returns:
            Vector4 - Multiplication of the Vector4
        """
        if isinstance(v, (int, float)):
            return Vector4(self.x * v, self.y * v, self.z * v, self.w * v)
        elif isinstance(v, matrix4.Matrix4):
            return v.__mul__(self)
        else:
            raise InvalidVec4OperationException("mult", type(self), type(v))

    def __rmul__(self, v):
        """Multiplies this Vector4 by a scalar.
        If we try to multiply anything other than a scalar, it throws the InvalidVec4OperationException

        Arguments:
            v {number} -- Scalar to multiply: all components of the vector are multiplied by
            this number

        Returns:
            Vector4 - Multiplication of the Vector4
        """
        if isinstance(v, (int, float)):
            return Vector4(self.x * v, self.y * v, self.z * v, self.w * v)
        elif isinstance(v, matrix4.Matrix4):
            return v.__rmul__(self)
        else:
            raise InvalidVec4OperationException("rmult", type(self), type(v))

    def __truediv__(self, v):
        """Divides this Vector4 by a scalar.
        If we try to divide anything other than a scalar, it throws the InvalidVec4OperationException

        Arguments:
            v {number} -- Scalar to divide: all components of the vector are divided by this number

        Returns:
            Vector4 - Division of the Vector4
        """
        if isinstance(v, (int, float)):
            return Vector4(self.x / v, self.y / v, self.z / v, self.w / v)
        else:
            raise InvalidVec4OperationException("truediv", type(self), type(v))

    def __eq__(self, v):
        """Checks if this Vector4 is equal to the given one, with a tolerance of 0.0001.
        Exception InvalidVec4OperationException is thrown if we compare something other than a
        Vector4.

        Arguments:
            v {Vector4} -- Vector to compare

        Returns:
            Bool - True if the vectors are the same, false otherwise
        """
        if isinstance(v, Vector4):
            return ((self - v).magnitude()) < 0.0001
        else:
            raise InvalidVec4OperationException("eq", type(self), type(v))

    def __ne__(self, v):
        """Checks if this Vector4 is different to the given one, with a tolerance of 0.0001.
        Exception InvalidVec4OperationException is thrown if we compare something other than a
        Vector4.

        Arguments:
            v {Vector4} -- Vector to compare

        Returns:
            Bool - True if the vectors are different, false otherwise
        """
        if isinstance(v, Vector4):
            return ((self - v).magnitude()) > 0.0001
        else:
            raise InvalidVec4OperationException("neq", type(self), type(v))

    def __isub__(self, v):
        """Subtracts a Vector4 from this one.
        If we try to subtract anything other than a Vector4, it throws the
        InvalidVec4OperationException.

        Arguments:
            v {Vector4} -- Vector to subtract

        Returns:
            Vector4 - Subraction of the given vector from this one
        """
        return self - v

    def __iadd__(self, v):
        """Adds this Vector4 to another.
        If we try to add anything other than a Vector4 to it, it throws the
        InvalidVec4OperationException.

        Arguments:
            v {Vector4} -- Vector to add

        Returns:
            Vector4 - Sum of this Vector4 and the given one
        """
        return self + v

    def __imul__(self, v):
        """Multiplies this Vector4 by a scalar.
        If we try to multiply anything other than a scalar, it throws the
        InvalidVec4OperationException.

        Arguments:
            v {number} -- Scalar to multiply: all components of the vector are
            multiplied by this number.

        Returns:
            Vector4 - Multiplication of the Vector4
        """
        return self * v

    def __idiv__(self, v):
        """Divides this Vector4 by a scalar.
        If we try to divide anything other than a scalar, it throws the InvalidVec4OperationException

        Arguments:
            v {number} -- Scalar to divide: all components of the vector are divided by this number

        Returns:
            Vector4 - Division of the Vector4
        """
        return self / v

    def __neg__(self):
        """Negates this Vector4, component-wise. Equivelent to multiplying by (-1)

        Returns:
            Vector4 - Negated Vector4
        """
        return Vector4(-self.x, -self.y, -self.z, -self.w)

    def magnitude(self):
        """Returns the magnitude of the Vector4.

        Returns:
            Number - Magnitude of the vector
        """
        return math.sqrt(self.dot(self))

    def magnitude_squared(self):
        """Returns the squared magnitude of the Vector4.

        Returns:
            Number - Magnitude of the vector
        """
        return self.dot(self)

    def dot(self, v):
        """Computes the dot product of this Vector4 with another.
        If we try to do this operation with anything other than a Vector4, it throws
        the InvalidVec4OperationException.

        Arguments:
            v {Vector4} -- Vector4 to do the dot product with

        Returns:
            Number - Scalar value corresponding to the dot product of both vectors
        """
        if isinstance(v, Vector4):
            return self.x * v.x + self.y * v.y + self.z * v.z + self.w * v.w
        else:
            raise InvalidVec4OperationException("dot", type(self), type(v))

    def normalize(self):
        """Normalizes this vector"""
        d = 1.0 / self.magnitude()
        self.x *= d
        self.y *= d
        self.z *= d
        self.w *= d

    def normalized(self):
        """Returns the normalized version of this Vector4

        Returns:
            Vector4 - Normalized vector
        """
        d = 1.0 / self.magnitude()
        return Vector4(self.x * d, self.y * d, self.z * d, self.w * d)

    @staticmethod
    def distance(v1, v2):
        """Returns the distance between two positions/vectors

        Arguments:
            v1 {Vector4} - First vector
            v2 {Vector4} - Second vector

        Returns:
            number - Distance between the two positions/vectors
        """
        return (v1 - v2).magnitude()
