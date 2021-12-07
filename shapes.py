from util import Colors, Vec3f
import math

class Shape:
    def __init__(self, surface_color, reflection=0, transparency=0, emission_color=Colors.BLACK):
        self.surface_color = surface_color
        self.reflection = reflection
        self.transparency = transparency
        self.emission_color = emission_color

    def is_intersecting(self, ray_origin, ray_dir):
        raise NotImplementedError()

class Sphere(Shape):
    def __init__(self, center, radius, \
            surface_color, reflection=0, transparency=0, emission_color=Colors.BLACK):
        self.center = center
        self.radius_sq = radius * radius
        super().__init__(surface_color, reflection, transparency, emission_color)

    def is_intersecting(self, ray_origin, ray_dir):
        l = self.center - ray_origin
        t_ca = l.dot(ray_dir)
        if t_ca < 0:
            return (False,)
        d_sq = l.dot(l) - t_ca * t_ca
        if d_sq > self.radius_sq:
            return (False,)
        t_hc = math.sqrt(self.radius_sq - d_sq)
        return (True, t_ca - t_hc, t_ca + t_hc)

class Box(Shape):
    def __init__(self, min_corner, max_corner, \
            surface_color, reflection=0, transparency=0, emission_color=Colors.BLACK):
        self.corners = (min_corner, max_corner)
        self.center = min_corner.midpoint(max_corner)
        super().__init__(surface_color, reflection, transparency, emission_color)

    def is_intersecting(self, ray_origin, ray_dir):
        inv_dir = ray_dir.inverse()
        t_min = (self.corners[inv_dir.x < 0].x - ray_origin.x) * inv_dir.x; 
        t_max = (self.corners[1 - (inv_dir.x < 0)].x - ray_origin.x) * inv_dir.x; 
        ty_min = (self.corners[inv_dir.y < 0].y - ray_origin.y) * inv_dir.y; 
        ty_max = (self.corners[1 - (inv_dir.y < 0)].y - ray_origin.y) * inv_dir.y; 
    
        if t_min > ty_max or ty_min > t_max:
            return (False,)
        t_min = max(t_min, ty_min)
        t_max = max(t_min, ty_max)
    
        tz_min = (self.corners[inv_dir.z < 0].z - ray_origin.z) * inv_dir.z
        tz_max = (self.corners[1 - (inv_dir.z < 0)].z - ray_origin.z) * inv_dir.z
    
        if t_min > tz_max or tz_min > t_max:
            return (False,)
        t_min = max(t_min, tz_min)
        t_max = max(t_min, tz_max)

        t = t_min if t_min >= 0 else t_max
        return (True, t, 0) if t >= 0 else (False,)