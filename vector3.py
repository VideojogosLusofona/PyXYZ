import math
import numpy as np

"""3d vector helper class and functions"""


class InvalidOperationException(Exception):
    """Exception thrown when there's an invalid operation with vectors"""
    def __init__(self, op, type1, type2):
        self.op = op
        self.type1 = type1
        self.type2 = type2

    """Returns a readable version of the exception"""
    def __str__(self):
        return "Invalid operation (" + self.op + ") between " + str(self.type1) + " and " + str(self.type2)

class vector3:
    """3d vector class. 
    It stores XYZ values as floats."""
    def __init__(self, x = 0, y = 0, z = 0):
        """
        Arguments:
            x {number} -- X component,defaults to 0

            y {number} -- Y component, defaults to 0

            z {number} -- Z component, defaults to 0
        """
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """Converts the 3d vector to a displayable string
        
        Returns:
            String - Vector in text format (x,y,z)"""
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def __add__(self, v):
        """Adds this vector3 to another. 
        If we try to add anything other than a vector3 to it, it throws the InvalidOperationException
        
        Arguments:
            v {vector3} -- Vector to add

        Returns:
            vector3 - Sum of this vector3 and the given one
        """
        if (isinstance(v, vector3)):
            return vector3(self.x + v.x, self.y + v.y, self.z + v.z)
        else:
            raise(InvalidOperationException("add", type(self), type(v)))

    def __sub__(self, v):
        """Subtracts a vector3 from this one.
        If we try to subtract anything other than a vector3, it throws the InvalidOperationException
        
        Arguments:
            v {vector3} -- Vector to subtract

        Returns:
            vector3 - Subraction of the given vector from this one
        """
        if (isinstance(v, vector3)):
            return vector3(self.x - v.x, self.y - v.y, self.z - v.z)
        else:
            raise(InvalidOperationException("sub", type(self), type(v)))

    def __mul__(self, v):
        """Multiplies this vector3 by a scalar.
        If we try to multiply anything other than a scalar, it throws the InvalidOperationException
        
        Arguments:
            v {number} -- Scalar to multiply: all components of the vector are multiplied by this number

        Returns:
            vector3 - Multiplication of the vector3
        """
        if (isinstance(v, (int, float))):
            return vector3(self.x * v, self.y * v, self.z * v)
        else:
            raise(InvalidOperationException("mult", type(self), type(v)))

    def __rmul__(self, v):
        """Multiplies this vector3 by a scalar.
        If we try to multiply anything other than a scalar, it throws the InvalidOperationException
        
        Arguments:
            v {number} -- Scalar to multiply: all components of the vector are multiplied by this number

        Returns:
            vector3 - Multiplication of the vector3
        """
        if (isinstance(v, (int, float))):
            return vector3(self.x * v, self.y * v, self.z * v)
        else:
            raise(InvalidOperationException("mult", type(self), type(v)))

    def __truediv__(self, v):
        """Divides this vector3 by a scalar.
        If we try to divide anything other than a scalar, it throws the InvalidOperationException
        
        Arguments:
            v {number} -- Scalar to divide: all components of the vector are divided by this number

        Returns:
            vector3 - Division of the vector3
        """
        if (isinstance(v, (int, float))):
            return vector3(self.x / v, self.y / v, self.z / v)
        else:
            raise(InvalidOperationException("mult", type(self), type(v)))

    def __eq__(self, v):
        """Checks if this vector3 is equal to the given one, with a tolerance of 0.0001. Exception InvalidOperationException is 
        thrown if we compare something other than a vector3.
        
        Arguments:
            v {vector3} -- Vector to compare

        Returns:
            Bool - True if the vectors are the same, false otherwise
        """
        if (isinstance(v, vector3)):
            return (((self - v).magnitude()) < 0.0001)
        else:
            raise(InvalidOperationException("eq", type(self), type(v)))

    def __ne__(self, v):
        """Checks if this vector3 is different to the given one, with a tolerance of 0.0001. Exception InvalidOperationException is 
        thrown if we compare something other than a vector3.
        
        Arguments:
            v {vector3} -- Vector to compare

        Returns:
            Bool - True if the vectors are different, false otherwise
        """
        if (isinstance(v, vector3)):
            return (((self - v).magnitude()) > 0.0001)
        else:
            raise(InvalidOperationException("neq", type(self), type(v)))

    def __isub__(self, v):
        """Subtracts a vector3 from this one.
        If we try to subtract anything other than a vector3, it throws the InvalidOperationException
        
        Arguments:
            v {vector3} -- Vector to subtract

        Returns:
            vector3 - Subraction of the given vector from this one
        """
        return self - v

    def __iadd__(self, v):
        """Adds this vector3 to another. 
        If we try to add anything other than a vector3 to it, it throws the InvalidOperationException
        
        Arguments:
            v {vector3} -- Vector to add

        Returns:
            vector3 - Sum of this vector3 and the given one
        """
        return self + v

    def __imul__(self, v):
        """Multiplies this vector3 by a scalar.
        If we try to multiply anything other than a scalar, it throws the InvalidOperationException
        
        Arguments:
            v {number} -- Scalar to multiply: all components of the vector are multiplied by this number

        Returns:
            vector3 - Multiplication of the vector3
        """
        return self * v

    def __idiv__(self, v):
        """Divides this vector3 by a scalar.
        If we try to divide anything other than a scalar, it throws the InvalidOperationException
        
        Arguments:
            v {number} -- Scalar to divide: all components of the vector are divided by this number

        Returns:
            vector3 - Division of the vector3
        """
        return self / v

    def __neg__(self):
        """Negates this vector3, component-wise. Equivelent to multiplying by (-1)
        
        Returns:
            vector3 - Negated vector3
        """
        return vector3(-self.x, -self.y, -self.z)

    def magnitude(self):
        """Returns the magnitude of the vector3.
        
        Returns:
            Number - Magnitude of the vector
        """
        return math.sqrt(self.dot(self))

    def magnitude_squared(self):
        """Returns the squared magnitude of the vector3.
        
        Returns:
            Number - Magnitude of the vector
        """
        return self.dot(self)

    def dot(self, v):
        """Computes the dot product of this vector3 with another.
        If we try to do this operation with anything other than a vector3, it throws the InvalidOperationException
        
        Arguments:
            v {vector3} -- Vector3 to do the dot product with

        Returns:
            Number - Scalar value corresponding to the dot product of both vectors
        """
        if (isinstance(v, vector3)):
            return self.x * v.x + self.y * v.y + self.z * v.z
        else:
            raise(InvalidOperationException("dot", type(self), type(v)))

    def cross(self, v):
        """Computes the cross product of this vector3 with another.
        If we try to do this operation with anything other than a vector3, it throws the InvalidOperationException
        
        Arguments:
            v {vector3} -- Vector3 to do the cross product with

        Returns:
            vector3 - Cross product of both vectors
        """
        if (isinstance(v, vector3)):
            return vector3(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z, self.x * v.y - self.y * v.x)
        else:
            raise(InvalidOperationException("dot", type(self), type(v)))

    def normalize(self):
        """Normalizes this vector"""
        d = 1.0 / self.magnitude()
        self.x *= d
        self.y *= d
        self.z *= d

    def normalized(self):
        """Returns the normalized version of this vector3

        Returns:
            vector3 - Normalized vector
        """
        d = 1.0 / self.magnitude()
        return vector3(self.x * d, self.y * d, self.z * d)

    def x0z(self):
        """Returns this vector, but with the y component zeroed.

        Returns:
            vector3 - (x,0,z)
        """
        return vector3(self.x, 0, self.z)

    def to_np3(self):
        """Converts a vector3 to a 3-component numpy array

        Returns:
            np.array - [x,y,z]
        """
        return np.array([self.x, self.y, self.z])

    def to_np4(self, w = 1):
        """Converts a vector3 to a 4-component numpy array, with the given w as the 4th component.

        Arguments:
            w {number} - Value of the w component on the np.array.

        Returns:
            np.array - [x,y,z,w]
        """
        return np.array([self.x, self.y, self.z, w])

    @staticmethod
    def from_np(np_array):
        """Converts a np.array to a vector3. No validation is done on the array to confirm it has 3 components.

        Arguments:
            np_array {np.array} - np.array with 3-components (rows or columns)

        Returns:
            vector3 - A vector3
        """        
        return vector3(np_array[0], np_array[1], np_array[2])

    @staticmethod
    def distance(v1, v2):
        """Returns the distance between two positions/vectors

        Arguments:
            v1 {vector3} - First vector
            v2 {vector3} - Second vector

        Returns:
            number - Distance between the two positions/vectors
        """        
        return (v1 - v2).magnitude()

def dot_product(v1, v2):
    """Returns the dot product between two vectors

    Arguments:
        v1 {vector3} - First vector
        v2 {vector3} - Second vector

    Returns:
        number - Dot product between the vectors
    """        
    return v1.dot(v2)

def cross_product(v1, v2):
    """Returns the cross product between two vectors

    Arguments:
        v1 {vector3} - First vector
        v2 {vector3} - Second vector

    Returns:
        vector3 - Cross product between the vectors
    """        
    return v1.cross(v2)

