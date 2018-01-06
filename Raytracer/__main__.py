"""
    Main code generates a test image
"""

import numpy as np
from Raytracer import RayTracer, Projection
from Raytracer.renderobjects import Triangle, ModelMesh
from Raytracer.shaders import Light, AmbientShader, DiffuseShader, SpecularShader

rt = RayTracer((600, 400), Projection.Perspective)
#rt = RayTracer((200,150), Projection.Parallel)
a = np.array([-50, -50, -2])
b = np.array([50, -50, -2])
c = np.array([0, 50, -2])
diff1 = np.array([50, 0, -1])
diff2 = np.array([-50, 0, 1])
t1 = Triangle(a, b, c)
#t2 = Triangle(a+diff1, b+diff1, c+diff1)
t2 = Triangle(
    np.array([20, -50, -5]),
    np.array([50, 50, -2]),
    np.array([100, -50, 1])
    )
t3 = Triangle(a+diff2, b+diff2, c+diff2)

t2.set_reflectiveness(0.7)
t1.set_reflectiveness(0.7)
t3.set_reflectiveness(0.7)
t1.set_transparency(0.776)
t3.set_transparency(0.376)

amb_white = AmbientShader((100, 100, 100))
amb_red = AmbientShader((100, 0, 0))
amb_blue = AmbientShader((0, 0, 100))

diff_white = DiffuseShader((100, 100, 100))
diff_red = DiffuseShader((100, 0, 0))
diff_blue = DiffuseShader((0, 0, 100))

spec = SpecularShader((100, 100, 100), 1)

t1.add_shader(amb_red)
t2.add_shader(amb_white)
t3.add_shader(amb_blue)

t1.add_shader(diff_red)
t2.add_shader(diff_white)
t3.add_shader(diff_blue)

t1.add_shader(spec)
t2.add_shader(spec)
t3.add_shader(spec)

#rt.add_object(t1)
#rt.add_object(t2)
#rt.add_object(t3)

teapot = ModelMesh("teapot.stl")
teapot.add_shader(SpecularShader((100, 100, 100), 1))
teapot.add_shader(DiffuseShader((100, 100, 100)))
rt.add_object(teapot)

light_pos = np.array([-20,0,5])
light_pos2 = np.array([30,5,5])
rt.add_light(Light(light_pos, (128, 128, 128)))
#rt.add_light(Light(light_pos2, (200, 0, 0)))
rt.render("test.png", limit=3)
