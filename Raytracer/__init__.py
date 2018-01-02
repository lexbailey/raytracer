#!/usr/bin/env python

"""
    A simple raytracer
"""

from enum import Enum
from itertools import product
import numpy as np
from PIL import Image
from Raytracer.rayutils import normalize
from Raytracer.renderobjects import Triangle

np.seterr(all="raise")

class ShaderModel():
    """
        Abstract base class for shader models
        subclasses should implement get_colour
    """
    def __init__(self):
        pass

    def get_colour(self, point, normal, lights, viewer):
        return (0, 0, 0)

class AmbientShader(ShaderModel):
    """
        An amibent shader model
    """
    def __init__(self, colour):
        super(AmbientShader, self).__init__()
        self.colour = colour

    def get_colour(self, point, normal, lights, viewer):
        # Ambient shader model returns a constant colour
        return self.colour

class Light():
    """
        Abstract base class for lights
    """
    def __init__(self, position, colour):
        self.position = position
        self.colour = colour

class Projection(Enum):
    """ Types of projection supported by the raytracer """
    Perspective = 0
    Parallel = 1

class RayTracer:
    """
        A really simple ray tracer
    """
    def _init_viewport(self):
        self.viewport = Image.new("RGB", (self.px_size))
        self.viewport_canvas = self.viewport.load()

    def __init__(self, px_size, projection):
        self.px_size = px_size
        assert len(self.px_size) == 2
        self.size = (100, 100)
        self.vp_cop = np.array([0, 0, 0])
        self.vp_copup = np.array([0, 1, 0])
        self.vp_normal = np.array([0, 0, 1])
        self.vp_prp = np.array([0, 0, 3])
        self.objects = []
        self.lights = []
        self.projection = projection
        self._init_viewport()

    def add_object(self, obj):
        self.objects.append(obj)

    def add_light(self, light):
        self.lights.append(light)

    def _trace_ray(self, x, y):
        ray_start = np.array([(x-100)/2, -((y-75)/1.5), 0]) # TODO make this actually not hard coded
        #ray_dir = ray_start - self.vp_normal
        if self.projection == Projection.Parallel:
            ray_dir = -self.vp_normal
        elif self.projection == Projection.Perspective:
            ray_dir = normalize(ray_start - self.vp_prp)
        else:
            raise Exception("Invalid projection type")
        s = np.array([0, 0, 0])
        near_obj, near_t = None, None
        for obj in self.objects:
            intersect = obj.ray_hit(ray_start, ray_dir)
            if intersect is None:
                continue
            t, u, v = intersect
            if near_t is None or t < near_t:
                near_obj, near_t = obj, t
        if near_obj is not None:
            point = ray_start + (ray_dir * t)
            s += near_obj.colour_at_point(point)
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
