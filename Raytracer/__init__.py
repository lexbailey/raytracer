#!/usr/bin/env python

"""
    A simple raytracer
"""

from os import cpu_count
from enum import Enum
from math import floor
from itertools import product, chain
from multiprocessing.pool import Pool, ApplyResult
import numpy as np
from PIL import Image
from Raytracer.rayutils import normalize, reflect
from Raytracer.renderobjects import Triangle

np.seterr(all="raise")

def call_bound_method(instance, name, args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    return getattr(instance, name)(*args, **kwargs)

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

    def __init__(self, px_size, projection):
        self.px_size = px_size
        assert len(self.px_size) == 2
        self.size = (150, 100)
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

    def visible_lights(self, point):
        """ return a list of the lights that the given point can see """
        visible = []
        for light in self.lights:
            ray_dir = light.get_position()-point
            near_obj, near_t, pid = self.nearest_object_hit(point, ray_dir)
            if near_obj is None:
                visible.append(light)
        return visible

    def nearest_object_hit(self, ray_start, ray_dir):
        near_obj, near_t, near_pid = None, None, None
        for obj in self.objects:
            intersect = obj.ray_hit(ray_start, ray_dir)
            if intersect is None:
                continue
            (t, u, v), pid = intersect
            if near_t is None or t < near_t:
                near_obj, near_t, near_pid = obj, t, pid
        return near_obj, near_t, near_pid

    def _trace_ray(self, ray_start, ray_dir, bounces=0, limit=10):
        s = np.array([0, 0, 0]).astype(np.dtype("float64"))
        if bounces > limit:
            return s.astype(int)
        near_obj, near_t, pid = self.nearest_object_hit(ray_start, ray_dir)
        if near_obj is not None:
            point = ray_start + (ray_dir * near_t)
            lights = self.visible_lights(point)
            s += near_obj.colour_at_point(point, pid, lights, normalize(ray_start-point))
            reflectiveness = near_obj.get_reflectiveness()
            transmit = near_obj.get_transparency()
            if reflectiveness > 0:
                reflect_ray = reflect(near_obj.normal_at_point(pid), -ray_dir)
                s += reflectiveness * self._trace_ray(point, reflect_ray, bounces=bounces+1, limit=limit)
            if transmit > 0:
                s += transmit * self._trace_ray(point, ray_dir, bounces=bounces+1, limit=limit)
        return s.astype(int)

    def _trace_ray_from_pixel(self, pixel, limit=10):
        x, y = pixel
        #ray_start = np.array([(x-100)/2, -((y-75)/1.5), 0]) # TODO make this actually not hard coded
        ray_start = np.array([(x-300)/6, -((y-200)/4), 0]) # TODO make this actually not hard coded
        if self.projection == Projection.Parallel:
            ray_dir = -self.vp_normal
        elif self.projection == Projection.Perspective:
            ray_dir = normalize(ray_start - self.vp_prp)
        else:
            raise Exception("Invalid projection type")
        return self._trace_ray(ray_start, ray_dir, limit=limit)

    def iter_all_pixels(self):
        return product(range(self.px_size[0]), range(self.px_size[1]))

    def iter_regions(self, num_regions):
        all_pixels = list(self.iter_all_pixels())
        length = len(all_pixels)
        pixels_per_region = floor(length/num_regions)
        for i in range(num_regions):
            start = i * pixels_per_region
            end = ((i + 1) *pixels_per_region)
            # To make sure we don't miss any near the end
            if i == num_regions-1:
                end = None
            yield all_pixels[start:end]

    def _render_region(self, region, limit=10):
        max_px = len(region)
        done_px = 0
        output = []
        for pixel in region:
            output.append(tuple(self._trace_ray_from_pixel(pixel, limit=limit)))
            done_px += 1
            if done_px % 10 == 0:
                print("%.1f%%" % (100*done_px/max_px))

    def render(self, filename, limit=10):
        renderpool = Pool()
        regions = [renderpool.apply_async(call_bound_method, args=(self, "_render_region", (region,), {"limit": limit})) for region in self.iter_regions(cpu_count())]
        renderpool.close()
        map(ApplyResult.wait, regions)
        pixels = list(chain(*[region.get() for region in regions]))
        viewport_canvas = self.viewport.load()
        for x, y in self.iter_all_pixels():
            viewport_canvas[x, y] = tuple(pixels[(x*self.px_size[1])+y])
        scale = 1
        out = self.viewport.resize((self.px_size[0] * scale, self.px_size[1] * scale), resample=Image.NEAREST)
        out.save(filename)
