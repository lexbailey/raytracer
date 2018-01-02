#!/usr/bin/env python

import numpy as np
from PIL import Image
from itertools import product

class Mesh():
    def __init__(self):
        self.points = []
        self.tris = []

    def add_triangle(self, a, b, c):
        for point in [a, b, c]:
            self.points.append(point)
        n = len(self.points)
        self.tris.append([n-3, n-2, n-1])

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
        self.size = (10,10)
        self.vp_cop = np.matrix([0,0,0])
        self.vp_copup = np.matrix([0,1,0])
        self.vp_normal = np.matrix([0,0,1])
        self.objects = []
        self._init_viewport()

    def add_object(self, obj):
        self.objects.append(obj)

    def _trace_ray(self, x, y):
        return (0,0,0)

    def iter_all_pixels(self):
        return product(range(self.px_size[0]), range(self.px_size[1]))

    def render(self, filename):
        for x, y in self.iter_all_pixels():
            self.viewport_canvas[x, y] = self._trace_ray(x, y)
        self.viewport.save(filename)

if __name__ == "__main__":
    rt = RayTracer((400,300))
    a = np.matrix([-1,-1,0])
    b = np.matrix([1,-1,0])
    c = np.matrix([0,1,0])
    rt.add_object(Triangle(a, b, c))
    rt.render("test.png")
