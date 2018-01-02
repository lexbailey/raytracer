"""
    Main code generates a test image
"""

import numpy as np
from Raytracer import RayTracer, Projection
from Raytracer.renderobjects import Triangle

rt = RayTracer((200, 150), Projection.Perspective)
#rt = RayTracer((200,150), Projection.Parallel)
a = np.array([-10, -10, -2])
b = np.array([10, -10, -2])
c = np.array([0, 10, -2])
diff1 = np.array([10, 0, -1])
diff2 = np.array([-10, 0, 1])
t1 = Triangle(a, b, c)
t2 = Triangle(a+diff1, b+diff1, c+diff1)
t2.set_colour((255, 0, 0))
t3 = Triangle(a+diff2, b+diff2, c+diff2)
t3.set_colour((0, 0, 255))
rt.add_object(t1)
rt.add_object(t2)
rt.add_object(t3)
rt.render("test.png")
