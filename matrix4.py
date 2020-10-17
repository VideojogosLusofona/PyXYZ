import vector4

USE_NUMPY = False

class InvalidMatrixOperationException(Exception):
    """Exception thrown when there's an invalid operation with matrices"""
    def __init__(self, op, type1, type2):
        super().__init__(self)
        self.op = op
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        """Returns a readable version of the exception"""
        return f"Invalid matrix operation ({self.op}) between {self.type1} and {self.type2}!"


class Matrix4:
    def __init__(self, m=None):
        if m is None:
            self.m = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        elif isinstance(m, (int, float)):
            self.m = [[m, m, m, m], [m, m, m, m], [m, m, m, m], [m, m, m, m]]
        else:
            self.m = m

    def __mul__(self, m):
        if isinstance(m, Matrix4):
            m2 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

            for i in range(0, 4):
                for j in range(0, 4):
                    m2[i][j] = 0
                    for k in range(0, 4):
                        m2[i][j] += self.m[i][k] * m.m[k][j]

            return Matrix4(m2)
        elif isinstance(m, vector4.Vector4):
            x = m.x * self.m[0][0] + m.y * self.m[1][0] + m.z * self.m[2][0] + m.w * self.m[3][0]
            y = m.x * self.m[0][1] + m.y * self.m[1][1] + m.z * self.m[2][1] + m.w * self.m[3][1]
            z = m.x * self.m[0][2] + m.y * self.m[1][2] + m.z * self.m[2][2] + m.w * self.m[3][2]
            w = m.x * self.m[0][3] + m.y * self.m[1][3] + m.z * self.m[2][3] + m.w * self.m[3][3]

            return vector4.Vector4(x, y, z, w)
        else:
            raise InvalidMatrixOperationException("mult", type(self), type(m))

    def __rmul__(self, m):   
        if isinstance(m, Matrix4):
            m2 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            
            for i in range(0, 4):
                for j in range(0, 4):
                    m2[i][j] = 0
                    for k in range(0, 4):
                        m2[i][j] += self.m[k][j] * m.m[i][k]

            return Matrix4(m2)
        elif isinstance(m, vector4.Vector4):
            x = self.m[0][0] * m.x + self.m[0][1] * m.y + self.m[0][2] * m.z + self.m[0][3] * m.w
            y = self.m[1][0] * m.x + self.m[1][1] * m.y + self.m[1][2] * m.z + self.m[1][3] * m.w
            z = self.m[2][0] * m.x + self.m[2][1] * m.y + self.m[2][2] * m.z + self.m[2][3] * m.w
            w = self.m[3][0] * m.x + self.m[3][1] * m.y + self.m[3][2] * m.z + self.m[3][3] * m.w

            return vector4.Vector4(x, y, z, w)
        else:
            raise InvalidMatrixOperationException("mult", type(self), type(m))

    def __getitem__(self, n):
        if isinstance(n, tuple):
            return self.m[n[0]][n[1]]
        return self.m[n]

    def __setitem__(self, n, value):
        if isinstance(n, tuple):
            self.m[n[0]][n[1]] = value
        else:
            self.m[n] = value

    def premultiply_v3(self, v, w):
        ox = v.x * self.m[0][0] + v.y * self.m[1][0] + v.z * self.m[2][0] + w * self.m[3][0]
        oy = v.x * self.m[0][1] + v.y * self.m[1][1] + v.z * self.m[2][1] + w * self.m[3][1]
        oz = v.x * self.m[0][2] + v.y * self.m[1][2] + v.z * self.m[2][2] + w * self.m[3][2]
        ow = v.x * self.m[0][3] + v.y * self.m[1][3] + v.z * self.m[2][3] + w * self.m[3][3]

        return vector4.Vector4(ox, oy, oz, ow)

    def premultiply_v4(self, v):
        x = v.x * self.m[0][0] + v.y * self.m[1][0] + v.z * self.m[2][0] + v.w * self.m[3][0]
        y = v.x * self.m[0][1] + v.y * self.m[1][1] + v.z * self.m[2][1] + v.w * self.m[3][1]
        z = v.x * self.m[0][2] + v.y * self.m[1][2] + v.z * self.m[2][2] + v.w * self.m[3][2]
        w = v.x * self.m[0][3] + v.y * self.m[1][3] + v.z * self.m[2][3] + v.w * self.m[3][3]

        return vector4.Vector4(x, y, z, w)

    def posmultiply_v3(self, v, w):
        ox = self.m[0][0] * v.x + self.m[0][1] * v.y + self.m[0][2] * v.z + self.m[0][3]
        oy = self.m[1][0] * v.x + self.m[1][1] * v.y + self.m[1][2] * v.z + self.m[1][3]
        oz = self.m[2][0] * v.x + self.m[2][1] * v.y + self.m[2][2] * v.z + self.m[2][3]
        ow = self.m[3][0] * v.x + self.m[3][1] * v.y + self.m[3][2] * v.z + self.m[3][3]

        return vector4.Vector4(ox, oy, oz, ow)

    def posmultiply_v4(self, v):
        x = self.m[0][0] * v.x + self.m[0][1] * v.y + self.m[0][2] * v.z + self.m[0][3] * v.w
        y = self.m[1][0] * v.x + self.m[1][1] * v.y + self.m[1][2] * v.z + self.m[1][3] * v.w
        z = self.m[2][0] * v.x + self.m[2][1] * v.y + self.m[2][2] * v.z + self.m[2][3] * v.w
        w = self.m[3][0] * v.x + self.m[3][1] * v.y + self.m[3][2] * v.z + self.m[3][3] * v.w

        return vector4.Vector4(x, y, z, w)

    def invert(self):
        # Use linear arrays instead of arrays of arrays
        tmp = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        src = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        dst = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

        # Create linear arry with transposed matrix
        for i in range(0, 4):
            for j in range(0, 4):
                src[i * 4 + j] = self.m[j][i]

        # Calculate pairs for first 8 elements (cofactors) 
        tmp[0]=src[10]*src[15]
        tmp[1]=src[11]*src[14]
        tmp[2]=src[9]*src[15]
        tmp[3]=src[11]*src[13]
        tmp[4]=src[9]*src[14]
        tmp[5]=src[10]*src[13]
        tmp[6]=src[8]*src[15]
        tmp[7]=src[11]*src[12]
        tmp[8]=src[8]*src[14]
        tmp[9]=src[10]*src[12]
        tmp[10]=src[8]*src[13]
        tmp[11]=src[9]*src[12]
        
        # calculate first 8 elements (cofactors)
        dst[0]=tmp[0]*src[5]+tmp[3]*src[6]+tmp[4]*src[7]
        dst[0]-=tmp[1]*src[5]+tmp[2]*src[6]+tmp[5]*src[7]
        dst[1]=tmp[1]*src[4]+tmp[6]*src[6]+tmp[9]*src[7]
        dst[1]-=tmp[0]*src[4]+tmp[7]*src[6]+tmp[8]*src[7]
        dst[2]=tmp[2]*src[4]+tmp[7]*src[5]+tmp[10]*src[7]
        dst[2]-=tmp[3]*src[4]+tmp[6]*src[5]+tmp[11]*src[7]
        dst[3]=tmp[5]*src[4]+tmp[8]*src[5]+tmp[11]*src[6]
        dst[3]-=tmp[4]*src[4]+tmp[9]*src[5]+tmp[10]*src[6]
        dst[4]=tmp[1]*src[1]+tmp[2]*src[2]+tmp[5]*src[3]
        dst[4]-=tmp[0]*src[1]+tmp[3]*src[2]+tmp[4]*src[3]
        dst[5]=tmp[0]*src[0]+tmp[7]*src[2]+tmp[8]*src[3]
        dst[5]-=tmp[1]*src[0]+tmp[6]*src[2]+tmp[9]*src[3]
        dst[6]=tmp[3]*src[0]+tmp[6]*src[1]+tmp[11]*src[3]
        dst[6]-=tmp[2]*src[0]+tmp[7]*src[1]+tmp[10]*src[3]
        dst[7]=tmp[4]*src[0]+tmp[9]*src[1]+tmp[10]*src[2]
        dst[7]-=tmp[5]*src[0]+tmp[8]*src[1]+tmp[11]*src[2]

        # calculate pairs for second 8 elements (cofactors) 
        tmp[0]=src[2]*src[7]
        tmp[1]=src[3]*src[6]
        tmp[2]=src[1]*src[7]
        tmp[3]=src[3]*src[5]
        tmp[4]=src[1]*src[6]
        tmp[5]=src[2]*src[5]
        tmp[6]=src[0]*src[7]
        tmp[7]=src[3]*src[4]
        tmp[8]=src[0]*src[6]
        tmp[9]=src[2]*src[4]
        tmp[10]=src[0]*src[5]
        tmp[11]=src[1]*src[4]

        # calculate second 8 elements (cofactors) 
        dst[8]=tmp[0]*src[13]+tmp[3]*src[14]+tmp[4]*src[15]
        dst[8]-=tmp[1]*src[13]+tmp[2]*src[14]+tmp[5]*src[15]
        dst[9]=tmp[1]*src[12]+tmp[6]*src[14]+tmp[9]*src[15]
        dst[9]-=tmp[0]*src[12]+tmp[7]*src[14]+tmp[8]*src[15]
        dst[10]=tmp[2]*src[12]+tmp[7]*src[13]+tmp[10]*src[15]
        dst[10]-=tmp[3]*src[12]+tmp[6]*src[13]+tmp[11]*src[15]
        dst[11]=tmp[5]*src[12]+tmp[8]*src[13]+tmp[11]*src[14]
        dst[11]-=tmp[4]*src[12]+tmp[9]*src[13]+tmp[10]*src[14]
        dst[12]=tmp[2]*src[10]+tmp[5]*src[11]+tmp[1]*src[9]
        dst[12]-=tmp[4]*src[11]+tmp[0]*src[9]+tmp[3]*src[10]
        dst[13]=tmp[8]*src[11]+tmp[0]*src[8]+tmp[7]*src[10]
        dst[13]-=tmp[6]*src[10]+tmp[9]*src[11]+tmp[1]*src[8]
        dst[14]=tmp[6]*src[9]+tmp[11]*src[11]+tmp[3]*src[8]
        dst[14]-=tmp[10]*src[11]+tmp[2]*src[8]+tmp[7]*src[9]
        dst[15]=tmp[10]*src[10]+tmp[4]*src[8]+tmp[9]*src[9]
        dst[15]-=tmp[8]*src[9]+tmp[11]*src[10]+tmp[5]*src[8]
        # calculate determinant 

        det=src[0]*dst[0]+src[1]*dst[1]+src[2]*dst[2]+src[3]*dst[3]
        
        # calculate inverse
        det=1/det
        for i in range(0,16):
            dst[i] *= det

        for i in range(0,4):
            for j in range(0,4):
                self.m[i][j] = dst[i * 4 + j]

    @staticmethod
    def zeros():
        return Matrix4(0)

    @staticmethod
    def identity():
        m = Matrix4(0)
        m.m[0][0] = m.m[1][1] = m.m[2][2] = m.m[3][3] = 1
        return m

# The following code is used to setup Numpy versions of the matrix operations,
# for better performance
if USE_NUMPY:
    import numpy as np
    print("Using Numpy")
    
    def numpy_matrix___init__(self, m = None):
        if (m is None):
            self.m = np.identity(4)
        elif isinstance(m, (int, float)):
            self.m = np.zeros((4, 4))
            self.m.fill(m)
        elif isinstance(m, np.ndarray):
            self.m = m
        else:
            self.m = np.array(m)

    def numpy_matrix_zeros():
        return Matrix4(0)

    def numpy_matrix_identity():
        return Matrix4()

    def numpy_matrix___getitem__(self, n):
        return self.m[n]

    def numpy_matrix___setitem__(self, n, value):
        self.m[n] = value

    def numpy_matrix___mul__(self, m):   
        if isinstance(m, Matrix4):
            return Matrix4(self.m @ m.m)
        elif isinstance(m, vector4.Vector4):
            v = np.array([m.x, m.y, m.z, m.w])
            v = v @ self.m
            return vector4.Vector4(v[0], v[1], v[2], v[3])
        else:
            raise InvalidMatrixOperationException("mult", type(self), type(m))

    def numpy_matrix___rmul__(self, m):   
        if isinstance(m, Matrix4):
            return Matrix4(m.m @ self.m)
        elif isinstance(m, vector4.Vector4):
            v = np.array([m.x, m.y, m.z, m.w]).transpose()
            v = self.m @ v
            return vector4.Vector4(v[0], v[1], v[2], v[3])
        else:
            raise InvalidMatrixOperationException("mult", type(self), type(m))

    def numpy_matrix_premultiply_v3(self, v, w):
        v = np.array([v.x, v.y, v.z, w]) @ self.m

        return vector4.Vector4(v[0], v[1], v[2], v[3])

    def numpy_matrix_premultiply_v4(self, v):
        v = np.array([v.x, v.y, v.z, v.w]) @ self.m

        return vector4.Vector4(v[0], v[1], v[2], v[3])

    def numpy_matrix_posmultiply_v3(self, v, w):
        v = self.m @ np.array([v.x, v.y, v.z, w])

        return vector4.Vector4(v[0], v[1], v[2], v[3])

    def numpy_matrix_posmultiply_v4(self, v):
        v = self.m @ np.array([v.x, v.y, v.z, v.w])

        return vector4.Vector4(v[0], v[1], v[2], v[3])

    def numpy_matrix_invert(self):
        self.m = np.linalg.inv(self.m)

    Matrix4.__init__ = numpy_matrix___init__
    Matrix4.identity = numpy_matrix_identity
    Matrix4.zeros = numpy_matrix_zeros
    Matrix4.__getitem__ = numpy_matrix___getitem__
    Matrix4.__setitem__ = numpy_matrix___setitem__
    Matrix4.__mul__ = numpy_matrix___mul__
    Matrix4.__rmul__ = numpy_matrix___rmul__
    Matrix4.premultiply_v3 = numpy_matrix_premultiply_v3
    Matrix4.premultiply_v4 = numpy_matrix_premultiply_v4
    Matrix4.invert = numpy_matrix_invert

else:
    print("Not using Numpy")
