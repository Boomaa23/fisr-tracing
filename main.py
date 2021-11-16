from util import Shape, Vec3f
import math
import struct

MAX_RAY_DEPTH = 5
HEIGHT = 500
WIDTH = 500

class Sphere(Shape):
    def __init__(self, center, radius, surface_color, reflection=0, transparency=0, emission_color=Vec3f(0, 0, 0)):
        self.center = center
        self.radius = radius
        self.radiusSq = radius * radius
        self.surface_color = surface_color
        self.reflection = reflection
        self.transparency = transparency
        self.emission_color = emission_color

    def calc_intersection(self, ray_origin, ray_dir):
        l = self.center - ray_origin
        tca = l.dot(ray_dir)
        if tca < 0:
            return (False,)
        d2 = l.dot(l) - tca * tca
        if d2 > self.radiusSq:
            return (False,)
        thc = math.sqrt(self.radiusSq - d2)
        return (True, tca - thc, tca + thc)

def mix(a, b, mix):
    return b * mix + a * (1 - mix)

def trace(ray_origin, ray_dir, spheres, depth):
    tnear = float('inf')
    sphere = None
    for s in spheres:
        t0 = float('inf')
        t1 = float('inf')
        intersect = s.calc_intersection(ray_origin, ray_dir)
        if intersect[0]:
            t0 = intersect[1]
            t1 = intersect[2]
            if t0 < 0:
                t0 = t1
            if t0 < tnear:
                tnear = t0
                sphere = s
    if not sphere:
        return Vec3f(2, 2, 2)
    surface_color = Vec3f(0, 0, 0)
    point_intersect = ray_origin + ray_dir * tnear
    normal_intersect = sphere.center.normalize()
    bias = 1e-4
    inside = False
    if ray_dir.dot(normal_intersect) > 0:
        normal_intersect = -normal_intersect
        inside = True
    if (sphere.transparency > 0 or sphere.reflection > 0) and depth < MAX_RAY_DEPTH:
        facing_ratio = -ray_dir.dot(normal_intersect)
        fresnel_effect = mix(pow(1 - facing_ratio, 3), 1, 0.1)
        refl_dir = ray_dir - normal_intersect * 2 * ray_dir.dot(normal_intersect)
        refl_dir.normalize()
        refl = trace(point_intersect + normal_intersect * bias, refl_dir, spheres, depth + 1)
        refr = Vec3f(0, 0, 0)
        if sphere.transparency:
            ior = 1.1
            eta = 1 / ior if inside else ior
            cosi = -normal_intersect.dot(ray_dir)
            k = 1 - eta * eta * (1 - cosi * cosi)
            refr_dir = ray_dir * eta + normal_intersect * (eta * cosi - math.sqrt(k))
            refr_dir.normalize()
            refr = trace(point_intersect - normal_intersect * bias, refr_dir, spheres, depth + 1)
        surface_color = refl * fresnel_effect + refr * (1 - fresnel_effect) * sphere.transparency * sphere.surface_color
    else:
        for i in range(len(spheres)):
            if spheres[i].emission_color.x > 0:
                transmission = Vec3f(1, 1, 1)
                light_dir = spheres[i].center - point_intersect
                light_dir.normalize()
                t0 = None
                t1 = None
                for j in range(len(spheres)):
                    if i != j:
                        intersect = spheres[j].calc_intersection(point_intersect + normal_intersect * bias, light_dir)
                        if intersect[0]:
                            t0 = intersect[1]
                            t1 = intersect[2]
                            break
                surface_color += sphere.surface_color * transmission * \
                    max(0, normal_intersect.dot(light_dir))#, spheres[i].emission_color)
    return surface_color + sphere.emission_color

def make_spheres():
    return [
        Sphere(Vec3f( 0.0, -10004, -20), 10000, Vec3f(0.20, 0.20, 0.20), 0, 0.0),
        Sphere(Vec3f( 0.0,      0, -20),     4, Vec3f(1.00, 0.32, 0.36), 1, 0.5),
        Sphere(Vec3f( 5.0,     -1, -15),     2, Vec3f(0.90, 0.76, 0.46), 1, 0.0),
        Sphere(Vec3f( 5.0,      0, -25),     3, Vec3f(0.65, 0.77, 0.97), 1, 0.0),
        Sphere(Vec3f(-5.5,      0, -15),     3, Vec3f(0.90, 0.90, 0.90), 1, 0.0),
        Sphere(Vec3f( 0.0,     20, -30),     3, Vec3f(0.00, 0.00, 0.00), 0, 0.0, Vec3f(3, 3, 3))
    ]

def main():
    inv_width = 1 / WIDTH
    inv_height = 1 / HEIGHT
    fov = 30
    aspect_ratio = WIDTH / HEIGHT
    angle = math.tan(math.pi * 0.5 * fov / 180)
    spheres = make_spheres()

    image = [[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            xx = (2 * ((x + 0.5) * inv_width) - 1) * angle * aspect_ratio
            yy = (1 - 2 * ((y + 0.5) * inv_height)) * angle
            ray_dir = Vec3f(xx, yy, -1).normalize(); 
            image[y][x] = trace(Vec3f(0, 0, 0), ray_dir, spheres, 0)
    
    with open("out.ppm", "wb") as out_ppm:
        out_ppm.write(f'P6\n{WIDTH} {HEIGHT}\n255\n'.encode())
        for y in range(HEIGHT):
            for x in range(WIDTH):
                px = image[y][x]
                out_ppm.write(struct.pack("f", min(1, px.x * 255)))
                out_ppm.write(struct.pack("f", min(1, px.y * 255)))
                out_ppm.write(struct.pack("f", min(1, px.z * 255)))

if __name__ == "__main__":
    main()