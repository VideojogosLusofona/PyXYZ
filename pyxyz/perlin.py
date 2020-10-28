"""Simple 2d Perlin noise implementation, based on https://github.com/karlll/perlin2d.py"""
import math
import random

W = 255
H = 255
gradtable = [(0, 0) for i in range(0, W*H)]

def _precalc_gradtable():
    rnd = random.Random()
    for i in range(0, H):
        for j in range(0, W):
            x = float((rnd.randint(1, 2*W))-W)/W
            y = float((rnd.randint(1, 2*H))-H)/H
            s = math.sqrt(x * x + y * y)
            if s != 0:
                x = x / s
                y = y / s
            else:
                x = 0
                y = 0
            gradtable[i*H+j] = (x, y)

#calculate dot product for v1 and v2
def _dot(v1, v2):
    return (v1[0]*v2[0]) + (v1[1]*v2[1])

# get a pseudorandom gradient vector
def _gradient(x, y):

    # normalize!
    return gradtable[y*H+x]

def _s_curve(x):
    return 3*x*x - 2*x*x*x

def noise2d(x, y):
    """Returns perlin noise corresponding to the given (x,y)

    Arguments:
        x {number} - X coordinate
        y {number} - Y coordinate

    Returns:
        {number} - A number in the range [-1,1]
    """

    x0 = math.floor(x)
    y0 = math.floor(y)
    x1 = x0 + 1.0
    y1 = y0 + 1.0

    i_x0 = int(x0)
    i_x1 = int(x1)
    i_y0 = int(y0)
    i_y1 = int(y1)

    s = _dot(_gradient(i_x0, i_y0), (x-x0, y-y0))
    t = _dot(_gradient(i_x1, i_y0), (x-x1, y-y0))
    u = _dot(_gradient(i_x0, i_y1), (x-x0, y-y1))
    v = _dot(_gradient(i_x1, i_y1), (x-x1, y-y1))

    s_x = _s_curve(x - x0)
    a = s + s_x*t - s_x*s
    b = u + s_x*v - s_x*u

    s_y = _s_curve(y - y0)
    z = a + s_y*b - s_y*a

    return z

_precalc_gradtable()
