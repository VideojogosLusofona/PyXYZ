import math

class InvalidColorOperationException(Exception):
    def __init__(self, op, type1, type2):
        self.op = op
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        return "Invalid color operation (" + self.op + ") between " + str(self.type1) + " and " + str(self.type2)

class color:
    def __init__(self, r = 0, g = 0, b = 0, a = 1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return "(" + str(self.r) + "," + str(self.g) + "," + str(self.b) + "," + str(self.a) + ")"

    def __add__(self, v):
        if (isinstance(v, color)):
            return color(self.r + v.r, self.g + v.g, self.b + v.b, self.a + v.a)
        else:
            raise(InvalidColorOperationException("add", type(self), type(v)))

    def __sub__(self, v):
        if (isinstance(v, color)):
            return color(self.r - v.r, self.g - v.g, self.b - v.b, self.a - v.a)
        else:
            raise(InvalidColorOperationException("sub", type(self), type(v)))

    def __mul__(self, v):
        if (isinstance(v, (int, float))):
            return color(self.r * v, self.g * v, self.b * v, self.a * v)
        elif (isinstance(v, color)):
            return color(self.r * v.r, self.g * v.g, self.b * v.b, self.a * v.a)
        else:
            raise(InvalidColorOperationException("mult", type(self), type(v)))

    def __truediv__(self, v):
        if (isinstance(v, (int, float))):
            return color(self.r / v, self.g / v, self.b / v, self.a / v)
        else:
            raise(InvalidColorOperationException("mult", type(self), type(v)))

    def __eq__(self, v):
        if (isinstance(v, color)):
            return (((self - v).magnitude()) < 0.0001)
        else:
            raise(InvalidColorOperationException("eq", type(self), type(v)))

    def __ne__(self, v):
        if (isinstance(v, color)):
            return (((self - v).magnitude()) > 0.0001)
        else:
            raise(InvalidColorOperationException("neq", type(self), type(v)))

    def __isub__(self, v):
        return self - v

    def __iadd__(self, v):
        return self + v

    def __imul__(self, v):
        return self * v

    def __idiv__(self, v):
        return self / v

    def __neg__(self):
        return color(1-self.r, 1-self.g, 1-self.b, self.a)

    def magnitude(self):
        return math.sqrt(self.dot(self))

    def dot(self, v):
        if (isinstance(v, color)):
            return self.r * v.r + self.g * v.g + self.b * v.b + self.a * v.a
        else:
            raise(InvalidColorOperationException("dot", type(self), type(v)))

    def normalize(self):
        d = 1.0 / self.magnitude()
        self.r *= d
        self.g *= d
        self.b *= d
        self.a *= d

    def normalized(self):
        d = 1.0 / self.magnitude()
        return color(self.r * d, self.g * d, self.b * d, self.a * d)

    def tuple3(self):
        return (self.r * 255, self.g * 255, self.b * 255)

    def tuple4(self):
        return (self.r * 255, self.g * 255, self.b * 255, self.a * 255)

    def saturate(self):
        return color(
                min(max(self.r, 0), 1),
                min(max(self.g, 0), 1),
                min(max(self.b, 0), 1),
                min(max(self.a, 0), 1)
        )
