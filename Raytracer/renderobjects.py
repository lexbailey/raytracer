"""
    This module contains objects that can be rendered
"""

import numpy as np
from Raytracer.rayutils import ray_triangle_intersect

class RenderObject():
    """
        Abstract base class for objects that can be rendered
    """
    def __init__(self):
        self.colour = (255, 255, 255)

    def set_colour(self, colour):
        """ Set the colour of the object """
        # TODO get rid of this in favour of shaders
        self.colour = colour

    def colour_at_point(self, point):
        """
            Get the colour of this object at the specified point
        """
        # TODO apply shader model
        return self.colour

    def ray_hit(self, p, d):
        """
            find where a ray hits this object, return (t, u, v)
            where t is distance to object, and u and v are the
            triangle coordinates of the intersection. If there
            is no intersection then return None
        """
        return None

class Mesh(RenderObject):
    """
        A RenderObject that represents an arbitrary triangle mesh
    """
    def __init__(self):
        super(Mesh, self).__init__()
        self.points = []
        self.tris = []

    def add_triangle(self, a, b, c):
        """
            Add a triangle to the mesh
        """
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
    """
        A RanderObject that represents a single triangle
    """
    def __init__(self, a, b, c):
        mesh = super(Triangle, self)
        mesh.__init__()
        mesh.add_triangle(a, b, c)
