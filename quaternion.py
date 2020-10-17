"""Quaternion class and helper functions"""
import math
import vector4
import matrix4

class InvalidQuaternionOperationException(Exception):
    """Exception thrown when there's an invalid operation with vectors"""
    def __init__(self, op, type1, type2):
        super().__init__(self)
        self.op = op
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        """Returns a readable version of the exception"""
        return f"Invalid Quaternion operation ({self.op}) between {self.type1} and {self.type2}!"

class Quaternion:
    """Quaternion class.
    It stores XYZW values as floats."""

    def __init__(self, x=0, y=0, z=0, w = 0):
        """
        Arguments:
            x {number} -- X component,defaults to 0

            y {number} -- Y component, defaults to 0

            z {number} -- Z component, defaults to 0

            w {number} -- W component, defaults to 0
        """
        if (isinstance(x, (vector4.Vector4, Quaternion))):
            self.x = x.x
            """{number} - X component"""
            self.y = x.y
            """{number} - Y component"""
            self.z = x.z
            """{number} - Z component"""
            self.w = x.w
            """{number} - W component"""
        else:
            self.x = x
            """{number} - X component"""
            self.y = y
            """{number} - Y component"""
            self.z = z
            """{number} - Z component"""
            self.w = w
            """{number} - W component"""

    def __str__(self):
        """Converts the quaternion vector to a displayable string

        Returns:
            String - Quaternion in text format (x,y,z,w)"""
        return f"({self.x},{self.y},{self.z},{self.w})"

    def __add__(self, v):
        """Adds this Quaternion to another.
        If we try to add anything other than a Quaternion to it, it throws the
        InvalidVec4OperationException.

        Arguments:
            v {Quaternion} -- Quaternion to add

        Returns:
            Quaternion - Sum of this Quaternion and the given one
        """
        if isinstance(v, Quaternion):
            return Quaternion(self.x + v.x, self.y + v.y, self.z + v.z, self.w + v.w)
        else:
            raise InvalidQuaternionOperationException("add", type(self), type(v))

    def __sub__(self, v):
        """Subtracts a Quaternion from this one.
        If we try to subtract anything other than a Quaternion, it throws the
        InvalidQuaternionOperationException.

        Arguments:
            v {Quaternion} -- Vector to subtract

        Returns:
            Quaternion - Subraction of the given quaternion from this one
        """
        if isinstance(v, Quaternion):
            return Quaternion(self.x - v.x, self.y - v.y, self.z - v.z, self.w - v.w)
        else:
            raise InvalidQuaternionOperationException("sub", type(self), type(v))

    def __mul__(self, q):
        """Multiplies this Quaternion by another one or a scalar.
        If we try to multiply anything other than a Quaternion, it throws the
        InvalidQuaternionOperationException.

        Arguments:
            v {number,Quaternion} -- Scalar or quaternion to multiply: In scalar multiplication, 
            all components of the quaternion are multiplied by this number; in quaternion
            multiplication, the rotations are composited


        Returns:
            Quaternion - Multiplication of the Quaternions
        """
        if isinstance(q, (int, float)):
            return Quaternion(self.x * q, self.y * q, self.z * q, self.w * q)
        elif isinstance(q, (Quaternion)):
            a = (self.w + self.x)*(q.w + q.x)
            b = (self.z - self.y)*(q.y - q.z)
            c = (self.w - self.x)*(q.y + q.z) 
            d = (self.y + self.z)*(q.w - q.x)
            e = (self.x + self.z)*(q.x + q.y)
            f = (self.x - self.z)*(q.x - q.y)
            g = (self.w + self.y)*(q.w - q.z)
            h = (self.w - self.y)*(q.w + q.z)

            w = b + (-e - f + g + h) * 0.5
            x = a - ( e + f + g + h) * 0.5 
            y = c + ( e - f + g - h) * 0.5 
            z = d + ( e - f - g + h) * 0.5

            return Quaternion(x, y, z, w)
        else:
            raise InvalidQuaternionOperationException("mult", type(self), type(q))

    def __truediv__(self, v):
        """Divides this Quaternion by a scalar.
        If we try to divide anything other than a scalar, it throws the InvalidQuaternionOperationException

        Arguments:
            v {number} -- Scalar to divide: all components of the vector are divided by this number

        Returns:
            Quaternion - Division of the Quaternion
        """
        if isinstance(v, (int, float)):
            return Quaternion(self.x / v, self.y / v, self.z / v, self.w / v)
        else:
            raise InvalidQuaternionOperationException("truediv", type(self), type(v))

    def __eq__(self, v):
        """Checks if this Quaternion is equal to the given one, with a tolerance of 0.0001.
        Exception InvalidQuaternionOperationException is thrown if we compare something other than a
        Vector4.

        Arguments:
            v {Quaternion} -- Vector to compare

        Returns:
            Bool - True if the quaternions are the same, false otherwise
        """
        if isinstance(v, Quaternion):
            return ((self - v).magnitude()) < 0.0001
        else:
            raise InvalidQuaternionOperationException("eq", type(self), type(v))

    def __ne__(self, v):
        """Checks if this Quaternion is different to the given one, with a tolerance of 0.0001.
        Exception InvalidQuaternionOperationException is thrown if we compare something other than a
        Quaternion.

        Arguments:
            v {Quaternion} -- Quaternion to compare

        Returns:
            Bool - True if the quaternions are different, false otherwise
        """
        if isinstance(v, Quaternion):
            return ((self - v).magnitude()) > 0.0001
        else:
            raise InvalidQuaternionOperationException("neq", type(self), type(v))

    def __isub__(self, v):
        """Subtracts a Quaternion from this one.
        If we try to subtract anything other than a Quaternion, it throws the
        InvalidQuaternionOperationException.

        Arguments:
            v {Quaternion} -- Quaternion to subtract

        Returns:
            Quaternion - Subraction of the given quaternion from this one
        """
        return self - v

    def __iadd__(self, v):
        """Adds this Quaternion to another.
        If we try to add anything other than a Quaternion to it, it throws the
        InvalidQuaternionOperationException.

        Arguments:
            v {Quaternion} -- Quaternion to add

        Returns:
            Quaternion - Sum of this Quaternion and the given one
        """
        return self + v

    def __imul__(self, v):
        """Multiplies this Quaternion by a scalar or quaternion.
        If we try to multiply anything other than a scalar or another quaternion, it throws the
        InvalidQuaternionOperationException.

        Arguments:
            v {number,quaternion} -- Scalar or quaternion to multiply: In scalar multiplication, 
            all components of the quaternion are multiplied by this number; in quaternion
            multiplication, the rotations are composited

        Returns:
            Quaternion - Multiplication of the Quaternion
        """
        return self * v

    def __idiv__(self, v):
        """Divides this Quaternion by a scalar.
        If we try to divide anything other than a scalar, it throws the InvalidQuaternionOperationException

        Arguments:
            v {number} -- Scalar to divide: all components of the quaternion are divided by this number

        Returns:
            Quaternion - Division of the Quaternion
        """
        return self / v

    def __neg__(self):
        """Negates this Quaternion, component-wise. Equivelent to multiplying by (-1)

        Returns:
            Quaternion - Negated Quaternion
        """
        return Quaternion(-self.x, -self.y, -self.z, -self.w)

    def magnitude(self):
        """Returns the magnitude of the Quaternion.

        Returns:
            Number - Magnitude of the quaternion
        """
        return math.sqrt(self.dot(self))

    def magnitude_squared(self):
        """Returns the squared magnitude of the Quaternion.

        Returns:
            Number - Magnitude of the quaternion
        """
        return self.dot(self)

    def dot(self, v):
        """Computes the dot product of this Quaternion with another.
        If we try to do this operation with anything other than a Quaternion, it throws
        the InvalidQuaternionOperationException.

        Arguments:
            v {Quaternion} -- Quaternion to do the dot product with

        Returns:
            Number - Scalar value corresponding to the dot product of both quaternions
        """
        if isinstance(v, Quaternion):
            return self.x * v.x + self.y * v.y + self.z * v.z + self.w * v.w
        else:
            raise InvalidQuaternionOperationException("dot", type(self), type(v))

    def normalize(self):
        """Normalizes this quaternion"""
        d = 1.0 / self.magnitude()
        self.x *= d
        self.y *= d
        self.z *= d
        self.w *= d

    def normalized(self):
        """Returns the normalized version of this Quaternion

        Returns:
            Quaternion - Normalized vector
        """
        d = 1.0 / self.magnitude()
        return Quaternion(self.x * d, self.y * d, self.z * d, self.w * d)

    def invert(self):
        inv_norm = 1 / self.magnitude()
        self.x = -self.x * inv_norm
        self.y = -self.y * inv_norm
        self.z = -self.z * inv_norm
        self.w =  self.w * inv_norm

    def inverted(self):
        inv_norm = 1 / self.magnitude()
        return Quaternion(-self.x * inv_norm, -self.y * inv_norm, -self.z * inv_norm, self.w * inv_norm)

    def as_rotation_matrix(self):
        matrix = matrix4.Matrix4.identity()

        xx = self.x * self.x
        xy = self.x * self.y
        xz = self.x * self.z
        xw = self.x * self.w

        yy = self.y * self.y
        yz = self.y * self.z
        yw = self.y * self.w

        zz =self.z * self.z
        zw =self.z * self.w

        matrix[0, 0] = 1 - 2 * (yy + zz)
        matrix[1, 0] =     2 * (xy - zw)
        matrix[2, 0] =     2 * (xz + yw)
        matrix[0, 1] =     2 * (xy + zw)
        matrix[1, 1] = 1 - 2 * (xx + zz) 
        matrix[2, 1] =     2 * (yz - xw) 
        matrix[0, 2] =     2 * (xz - yw) 
        matrix[1, 2] =     2 * (yz + xw)
        matrix[2, 2] = 1 - 2 * (xx + yy)
        matrix[0, 3] = 0
        matrix[1, 3] = 0
        matrix[2, 3] = 0

        return matrix

    @staticmethod
    def identity():
        return Quaternion(0, 0, 0, 1)

    @staticmethod
    def AngleAxis(axis, angle):
        ang = -angle
        ang2 = ang * 0.5
        sin_ang2 = math.sin(ang2)

        x = -axis.x * sin_ang2
        y = -axis.y * sin_ang2
        z = -axis.z * sin_ang2
        w = math.cos(ang2)

        return Quaternion(x, y, z, w)
