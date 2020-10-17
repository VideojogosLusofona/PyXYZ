"""3d vector class and helper functions"""
import math
import vector4

class InvalidVec3OperationException(Exception):
    """Exception thrown when there's an invalid operation with vectors"""
    def __init__(self, op, type1, type2):
        super().__init__(self)
        self.op = op
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        """Returns a readable version of the exception"""
        return f"Invalid Vector3 operation ({self.op}) between {self.type1} and {self.type2}!"

class Vector3:
    """3d vector class.
    It stores XYZ values as floats."""

    def __init__(self, x=0, y=0, z=0):
        """
        Arguments:
            x {number} -- X component,defaults to 0

            y {number} -- Y component, defaults to 0

            z {number} -- Z component, defaults to 0
        """
        self.x = x
        """{number} - X component"""
        self.y = y
        """{number} - Y component"""
        self.z = z
        """{number} - Z component"""

    def __str__(self):
        """Converts the 3d vector to a displayable string

        Returns:
            String - Vector in text format (x,y,z)"""
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def __add__(self, v):
        """Adds this Vector3 to another.
        If we try to add anything other than a Vector3 to it, it throws the
        InvalidVec3OperationException.

        Arguments:
            v {Vector3} -- Vector to add

        Returns:
            Vector3 - Sum of this Vector3 and the given one
        """
        if isinstance(v, Vector3):
            return Vector3(self.x + v.x, self.y + v.y, self.z + v.z)
        else:
            raise InvalidVec3OperationException("add", type(self), type(v))

    def __sub__(self, v):
        """Subtracts a Vector3 from this one.
        If we try to subtract anything other than a Vector3, it throws the
        InvalidVec3OperationException.

        Arguments:
            v {Vector3} -- Vector to subtract

        Returns:
            Vector3 - Subraction of the given vector from this one
        """
        if isinstance(v, Vector3):
            return Vector3(self.x - v.x, self.y - v.y, self.z - v.z)
        else:
            raise InvalidVec3OperationException("sub", type(self), type(v))

    def __mul__(self, v):
        """Multiplies this Vector3 by a scalar.
        If we try to multiply anything other than a scalar, it throws the
        InvalidVec3OperationException.

        Arguments:
            v {number} -- Scalar to multiply: all components of the vector are
            multiplied by this number

        Returns:
            Vector3 - Multiplication of the Vector3
        """
        if isinstance(v, (int, float)):
            return Vector3(self.x * v, self.y * v, self.z * v)
        else:
            raise InvalidVec3OperationException("mult", type(self), type(v))

    def __rmul__(self, v):
        """Multiplies this Vector3 by a scalar.
        If we try to multiply anything other than a scalar, it throws the InvalidVec3OperationException

        Arguments:
            v {number} -- Scalar to multiply: all components of the vector are multiplied by
            this number

        Returns:
            Vector3 - Multiplication of the Vector3
        """
        if isinstance(v, (int, float)):
            return Vector3(self.x * v, self.y * v, self.z * v)
        else:
            raise InvalidVec3OperationException("rmult", type(self), type(v))

    def __truediv__(self, v):
        """Divides this Vector3 by a scalar.
        If we try to divide anything other than a scalar, it throws the InvalidVec3OperationException

        Arguments:
            v {number} -- Scalar to divide: all components of the vector are divided by this number

        Returns:
            Vector3 - Division of the Vector3
        """
        if isinstance(v, (int, float)):
            return Vector3(self.x / v, self.y / v, self.z / v)
        else:
            raise InvalidVec3OperationException("truediv", type(self), type(v))

    def __eq__(self, v):
        """Checks if this Vector3 is equal to the given one, with a tolerance of 0.0001.
        Exception InvalidVec3OperationException is thrown if we compare something other than a
        Vector3.

        Arguments:
            v {Vector3} -- Vector to compare

        Returns:
            Bool - True if the vectors are the same, false otherwise
        """
        if isinstance(v, Vector3):
            return ((self - v).magnitude()) < 0.0001
        else:
            raise InvalidVec3OperationException("eq", type(self), type(v))

    def __ne__(self, v):
        """Checks if this Vector3 is different to the given one, with a tolerance of 0.0001.
        Exception InvalidVec3OperationException is thrown if we compare something other than a
        Vector3.

        Arguments:
            v {Vector3} -- Vector to compare

        Returns:
            Bool - True if the vectors are different, false otherwise
        """
        if isinstance(v, Vector3):
            return ((self - v).magnitude()) > 0.0001
        else:
            raise InvalidVec3OperationException("neq", type(self), type(v))

    def __isub__(self, v):
        """Subtracts a Vector3 from this one.
        If we try to subtract anything other than a Vector3, it throws the
        InvalidVec3OperationException.

        Arguments:
            v {Vector3} -- Vector to subtract

        Returns:
            Vector3 - Subraction of the given vector from this one
        """
        return self - v

    def __iadd__(self, v):
        """Adds this Vector3 to another.
        If we try to add anything other than a Vector3 to it, it throws the
        InvalidVec3OperationException.

        Arguments:
            v {Vector3} -- Vector to add

        Returns:
            Vector3 - Sum of this Vector3 and the given one
        """
        return self + v

    def __imul__(self, v):
        """Multiplies this Vector3 by a scalar.
        If we try to multiply anything other than a scalar, it throws the
        InvalidVec3OperationException.

        Arguments:
            v {number} -- Scalar to multiply: all components of the vector are
            multiplied by this number.

        Returns:
            Vector3 - Multiplication of the Vector3
        """
        return self * v

    def __idiv__(self, v):
        """Divides this Vector3 by a scalar.
        If we try to divide anything other than a scalar, it throws the InvalidVec3OperationException

        Arguments:
            v {number} -- Scalar to divide: all components of the vector are divided by this number

        Returns:
            Vector3 - Division of the Vector3
        """
        return self / v

    def __neg__(self):
        """Negates this Vector3, component-wise. Equivelent to multiplying by (-1)

        Returns:
            Vector3 - Negated Vector3
        """
        return Vector3(-self.x, -self.y, -self.z)

    def magnitude(self):
        """Returns the magnitude of the Vector3.

        Returns:
            Number - Magnitude of the vector
        """
        return math.sqrt(self.dot(self))

    def magnitude_squared(self):
        """Returns the squared magnitude of the Vector3.

        Returns:
            Number - Magnitude of the vector
        """
        return self.dot(self)

    def dot(self, v):
        """Computes the dot product of this Vector3 with another.
        If we try to do this operation with anything other than a Vector3, it throws
        the InvalidVec3OperationException.

        Arguments:
            v {Vector3} -- Vector3 to do the dot product with

        Returns:
            Number - Scalar value corresponding to the dot product of both vectors
        """
        if isinstance(v, Vector3):
            return self.x * v.x + self.y * v.y + self.z * v.z
        else:
            raise InvalidVec3OperationException("dot", type(self), type(v))

    def cross(self, v):
        """Computes the cross product of this Vector3 with another.
        If we try to do this operation with anything other than a Vector3, it throws
        the InvalidVec3OperationException.

        Arguments:
            v {Vector3} -- Vector3 to do the cross product with

        Returns:
            Vector3 - Cross product of both vectors
        """
        if isinstance(v, Vector3):
            return Vector3(self.y * v.z - self.z * v.y,
                           self.z * v.x - self.x * v.z,
                           self.x * v.y - self.y * v.x)
        else:
            raise InvalidVec3OperationException("dot", type(self), type(v))

    def normalize(self):
        """Normalizes this vector"""
        d = 1.0 / self.magnitude()
        self.x *= d
        self.y *= d
        self.z *= d

    def normalized(self):
        """Returns the normalized version of this Vector3

        Returns:
            Vector3 - Normalized vector
        """
        d = 1.0 / self.magnitude()
        return Vector3(self.x * d, self.y * d, self.z * d)

    def x0z(self):
        """Returns this vector, but with the y component zeroed.

        Returns:
            Vector3 - (x,0,z)
        """
        return Vector3(self.x, 0, self.z)

    @staticmethod
    def distance(v1, v2):
        """Returns the distance between two positions/vectors

        Arguments:
            v1 {Vector3} - First vector
            v2 {Vector3} - Second vector

        Returns:
            number - Distance between the two positions/vectors
        """
        return (v1 - v2).magnitude()

def dot_product(v1, v2):
    """Returns the dot product between two vectors

    Arguments:
        v1 {Vector3} - First vector
        v2 {Vector3} - Second vector

    Returns:
        number - Dot product between the vectors
    """
    return v1.dot(v2)

def cross_product(v1, v2):
    """Returns the cross product between two vectors

    Arguments:
        v1 {Vector3} - First vector
        v2 {Vector3} - Second vector

    Returns:
        Vector3 - Cross product between the vectors
    """
    return v1.cross(v2)
