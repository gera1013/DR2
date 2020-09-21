import numpy as np
from gl import color, mathVectorSubstraction, mathDotProduct, mathFrobenius, mathVectorAdd, mathVectorTimesScalar, mathLinalgNormal


WHITE = color(1, 1, 1)

class Material(object):
    # inicialización
    def __init__(self, diffuse = WHITE, spec = 0):
        # color del pixel
        self.diffuse = diffuse
        self.spec = spec


class Intersect(object):
    # inicialización
    def __init__(self, distance, point, normal, object):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObject = object

class AmbientLight(object):
    # inicialización
    def __init__(self, strength = 0, _color_ = WHITE):
        self.strength = strength
        self.color = _color_

class PointLight(object):
    # inicialización
    def __init__(self, position = [0, 0, 0], intensity = 1, _color_ = WHITE):
        self.position = position
        self.intensity = intensity
        self.color = _color_

class Sphere(object):

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        # Regresa falso o verdadero si hace interseccion con una esfera

        L = mathVectorSubstraction(self.center, orig)
        tca = mathDotProduct(L, dir)
        magnitude_L = mathFrobenius(L)

        d = (magnitude_L ** 2 - tca ** 2) ** 0.5
        
        if d > self.radius:
            return None

        # thc es la distancia de P1 al punto perpendicular al centro
        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        
        if t0 < 0:
            t0 = t1

        if t0 < 0: # t0 tiene el valor de t1
            return None

        hit = mathVectorAdd(orig, mathVectorTimesScalar(t0, dir))

        norm = mathVectorSubstraction(hit, self.center)
        norm = mathLinalgNormal(norm)

        return Intersect(
            distance = t0,
            point = hit,
            normal = norm,
            object = self
        )
