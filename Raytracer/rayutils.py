"""
    Various util functions needed by the raytracer
"""

import numpy as np

def normalize(v):
    """
        returns the normalized form of v
    """
    n = np.linalg.norm(v)
    try:
        return v/n
    except FloatingPointError:
        return v

def cross_prod(a, b):
    """
        returns the cross product of a and b
    """
    a = a.tolist()
    b = b.tolist()
    return np.array([
        (a[1] * b[2]) - (b[1] * a[2]),
        (a[2] * b[0]) - (b[2] * a[0]),
        (a[0] * b[1]) - (b[0] * a[1])
    ])

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
    f = 1/a
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
        return (t, u, v)
    return None
