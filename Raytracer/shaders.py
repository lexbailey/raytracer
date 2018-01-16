"""
    Shader models
"""

import numpy as np
from Raytracer.rayutils import normalize, reflect


class ShaderModel():
    """
        Abstract base class for shader models
        subclasses should implement get_colour
    """

    def __init__(self, colour):
        self.colour = colour

    def set_colour(self, colour):
        """
            Set the base colour of the shader
        """
        self.colour = colour

    def get_colour(self, point, normal, lights, viewer):
        """
            Get the colour produced by the shader model at the given
            point considering the normal, a set of lights, and a viewer
            direction.
        """
        return (0, 0, 0)


class AmbientShader(ShaderModel):
    """
        An amibent shader model
    """

    def get_colour(self, point, normal, lights, viewer):
        # Ambient shader model returns a constant colour
        return self.colour


class DiffuseShader(ShaderModel):
    """
        Lambertian model of difuse shading
    """

    def get_colour(self, point, normal, lights, viewer):
        output = np.array([0, 0, 0]).astype(np.dtype("float64"))
        for light in lights:
            light_dir = normalize(light.get_position() - point)
            output += np.array(light.get_colour()) * np.dot(normal, light_dir)
        return tuple(output)


class SpecularShader(ShaderModel):
    """
        Specular shading model
    """

    def __init__(self, colour, shininess):
        super(SpecularShader, self).__init__(colour)
        self.shininess = shininess

    def get_colour(self, point, normal, lights, viewer):
        output = np.array([0, 0, 0]).astype(np.dtype("float64"))
        for light in lights:
            light_dir = normalize(light.get_position() - point)
            reflection_ray = reflect(normal, light_dir)
            output += np.clip(pow(np.dot(reflection_ray, viewer),
                                  self.shininess) * np.array(light.get_colour()), 0, None)
        return tuple(output)


class Light():
    """
        Abstract base class for lights
    """

    def __init__(self, position, colour):
        self.position = position
        self.colour = colour

    def get_position(self):
        """ Get the potision of the light """
        return self.position

    def get_colour(self):
        """ Get the colour of the light """
        return self.colour
