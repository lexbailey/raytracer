#!/usr/bin/env python

import numpy as np
from PIL import Image
from itertools import product

def cross_prod(a, b):
    return [
        (a[1] * b[2]) - (b[1] * a[2]),
        (a[2] * b[0]) - (b[2] * a[0]),
        (a[0] * b[1]) - (b[0] * a[1])
    ]

def ray_triangle_intersect(p, d, v0, v1, v2):
    """
        given a ray starting at point p heading in direction d
        find the distance to the intersection and U,V coords (or
        None)
    """
    e1 = v1 - v0
    e2 = v2 - v0
    h = cross_prod(d, e2)
    a = np.dot(e1, h)

    if a > -0.00001 and a < 0.00001:
        return None

    f = 1/a;
    s = p - v0
    u = f * (np.dot(s, h))

    if u < 0.0 or u > 1.0:
        return None

    q = cross_prod(s, e1)
    v = f * np.dot(d, q)

    if v < 0.0 or u + v > 1.0:
        return None

    t = f * np.dot(e2, q)

    if t > 0.00001:
        return (t, u, v);
    return None

class RenderObject():
    def __init__(self):
        self.colour = (255,255,255)

    def set_colour(self, colour):
        self.colour = colour

    def ray_hit(self):
        return None

class Mesh(RenderObject):
    def __init__(self):
        super(Mesh, self).__init__()
        self.points = []
        self.tris = []

    def add_triangle(self, a, b, c):
        for point in [a, b, c]:
            self.points.append(point)
        n = len(self.points)
        self.tris.append([n-3, n-2, n-1])

    def ray_hit(self, p, d):
        near = None
        for triangle in self.tris:
            tripoints = [self.points[i] for i in triangle]
            intersect = ray_triangle_intersect(p, d, tripoints[0], tripoints[1], tripoints[2])
            if intersect is not None:
                t, u, v = intersect
                if near is None or t < near[0]:
                    near = t, u, v
        return near
                

class Triangle(Mesh):
    def __init__(self, a, b, c):
        mesh = super(Triangle, self)
        mesh.__init__()
        mesh.add_triangle(a, b, c)

class RayTracer:

    def _init_viewport(self):
        self.viewport = Image.new("RGB", (self.px_size))
        self.viewport_canvas = self.viewport.load()

    def __init__(self, px_size):
        self.px_size = px_size
        assert len(self.px_size) == 2
        self.size = (100,100)
        self.vp_cop = np.array([0,0,0])
        self.vp_copup = np.array([0,1,0])
        self.vp_normal = np.array([0,0,1])
        self.objects = []
        self._init_viewport()

    def add_object(self, obj):
        self.objects.append(obj)

    def _trace_ray(self, x, y):
        ray_start = np.array([(x-100)/2, -((y-75)/1.5), 0]) # TODO make this actually not hard coded
        ray_dir = ray_start - self.vp_normal
        s = np.array([0,0,0])
        near_obj, near_t = None, None
        for obj in self.objects:
            intersect = obj.ray_hit(ray_start, ray_dir)
            if intersect is None:
                continue
            t, u, v = intersect
            if near_t is None or t < near_t:
                near_obj, near_t = obj, t
        if near_obj is not None:
            s += near_obj.colour
            #print(s)
            # TODO recurse
        return s

    def iter_all_pixels(self):
        return product(range(self.px_size[0]), range(self.px_size[1]))

    def render(self, filename):
        for x, y in self.iter_all_pixels():
            self.viewport_canvas[x, y] = tuple(self._trace_ray(x, y))
            #print(x, y, end = "")
            #print(".", end = "")
        self.viewport.save(filename)

def main():
    rt = RayTracer((200,150))
    a = np.array([-100,-100,-2])
    b = np.array([100,-100,-2])
    c = np.array([0,100,-2])
    diff1 = np.array([100, 0, -1])
    diff2 = np.array([-100, 0, 1])
    t1 = Triangle(a, b, c)
    t2 = Triangle(a+diff1, b+diff1, c+diff1)
    t2.set_colour((255, 0, 0))
    t3 = Triangle(a+diff2, b+diff2, c+diff2)
    t3.set_colour((0, 0, 255))
    rt.add_object(t1)
    rt.add_object(t2)
    rt.add_object(t3)
    rt.render("test.png")

if __name__ == "__main__":
    main()
