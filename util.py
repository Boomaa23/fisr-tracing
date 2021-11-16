import math
import struct

def fast_inv_sqrt(number):
    return 1 / math.sqrt(number)
    # y = number
    # i = struct.unpack("i", struct.pack("f", y))[0]
    # i = 0x5f3759df - (i >> 1)
    # y = struct.unpack("f", struct.pack("i", i))[0]
    # return y * (1.5 - (number * 0.5 * y * y))

class Vec3f:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        normSq = self.sqLen(); 
        if (normSq > 0):
            invNor = fast_inv_sqrt(self.length())
            self.x *= invNor
            self.y *= invNor
            self.z *= invNor
        return self

    def sqLen(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self):
        return math.sqrt(self.sqLen())

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __add__(self, other):
        return Vec3f(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
    
    def __sub__(self, other):
        return Vec3f(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __mul__(self, other):
        if isinstance(other, Vec3f):
            return Vec3f(
                self.x * other.x,
                self.y * other.y,
                self.z * other.z
            )
        else:
            return Vec3f(
                self.x * other,
                self.y * other,
                self.z * other
            )

    def __neg__(self):
        return Vec3f(
            -self.x,
            -self.y,
            -self.z
        )
    
    def __IADD__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __IMUL__(self, other):
        self.x *= other.x
        self.y *= other.y
        self.z *= other.z
        return self

    def __str__(self):
        return f'[{self.x}, {self.y}, {self.z}]'

class Shape:
    def calc_intersection(self, ray_origin, ray_dir):
        raise NotImplementedError()