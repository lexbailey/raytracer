"""
    This module contains objects that can be rendered
"""

import numpy as np
import trimesh
from Raytracer.rayutils import ray_triangle_intersect, triangle_normal

class RenderObject():
    """
        Abstract base class for objects that can be rendered
    """
    def __init__(self):
        self.shaders = []
        self.reflectiveness = 0
        self.transparency = 0

    def add_shader(self, shader):
        self.shaders.append(shader)

    def colour_at_point(self, point):
        """
            Get the colour of this object at the specified point
        """
        return (0, 0, 0)

    def ray_hit(self, p, d):
        """
            find where a ray hits this object, return (t, u, v)
            where t is distance to object, and u and v are the
            triangle coordinates of the intersection. If there
            is no intersection then return None
        """
        return None

    def set_reflectiveness(self, reflectiveness):
        self.reflectiveness = reflectiveness

    def get_reflectiveness(self):
        return self.reflectiveness

    def set_transparency(self, transparency):
        self.transparency = transparency

    def get_transparency(self):
        return self.transparency

class Mesh(RenderObject):
    """
        A RenderObject that represents an arbitrary triangle mesh
    """
    def __init__(self):
        super(Mesh, self).__init__()
        self.points = []
        self.tris = []
        self.normals = []

    def normal_at_point(self, pointid):
        normal = self.normals[pointid]
        if normal is not None:
            return normal
        triangle = self.tris[pointid]
        tripoints = [self.points[i] for i in triangle]
        normal = triangle_normal(*tripoints)
        self.normals[pointid] = normal
        return normal

    def colour_at_point(self, point, pointid, lights, viewer):
        outcol = np.array([0,0,0]).astype(np.dtype("float64"))
        normal = self.normal_at_point(pointid)
        for shader in self.shaders:
            outcol += np.array(shader.get_colour(point, normal, lights, viewer))
        return outcol

    def add_triangle(self, a, b, c):
        """
            Add a triangle to the mesh
        """
        for point in [a, b, c]:
            self.points.append(point)
        n = len(self.points)
        self.tris.append([n-3, n-2, n-1])
        self.normals.append(None)

    def ray_hit(self, p, d):
        near = None
        n_tid = None
        for tid, triangle in enumerate(self.tris):
            tripoints = [self.points[i] for i in triangle]
            intersect = ray_triangle_intersect(p, d, tripoints[0], tripoints[1], tripoints[2])
            if intersect is not None:
                t, u, v = intersect
                if near is None or t < near[0]:
                    near = t, u, v
                    n_tid = tid
        if near is None:
            return None
        return (near, n_tid)

class Triangle(Mesh):
    """
        A RanderObject that represents a single triangle
    """
    def __init__(self, a, b, c):
        mesh = super(Triangle, self)
        mesh.__init__()
        mesh.add_triangle(a, b, c)

class ModelMesh(Mesh):
    def __init__(self, filename):
        super(ModelMesh, self).__init__()
        loaded_mesh = trimesh.load(filename)
        self.points = loaded_mesh.vertices
        self.tris = loaded_mesh.faces
