import fisr
import math

class Vec3f:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        inv_norm = fisr.fast_inv_sqrt(self.sq_len())
        self.x *= inv_norm
        self.y *= inv_norm
        self.z *= inv_norm
        return self

    def sq_len(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self):
        return math.sqrt(self.sq_len())

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def midpoint(self, other):
        return Vec3f(
            (self.x + other.x) / 2,
            (self.y + other.y) / 2,
            (self.z + other.z) / 2
        )

    def inverse(self):
        return Vec3f(
            1 / self.x,
            1 / self.y,
            1 / self.z
        )

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

class Colors:
    BLACK = Vec3f(0, 0, 0)
    WHITE = Vec3f(1, 1, 1)