import struct
import random
import numpy as np
from numpy import cos, sin, tan


def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([round(b * 255), round(g * 255), round(r * 255)])

# (a, b) - dos vectores de longitud 3
# se calcula el producto cruz entre dos vectores a y b. (a x b)
def mathCrossProduct(a, b):
    c = [a[1] * b[2] - a[2] * b[1],
         a[2] * b[0] - a[0] * b[2],
         a[0] * b[1] - a[1] * b[0]
    ]

    return c

# (a, b) - dos vectores de la misma longitud
# se calcula el producto punto entre dos vectores a y b. (a . b)
def mathDotProduct(a, b):
    total = 0
    for i in range(len(a)):
        total += a[i] * b[i]

    return total

# (a, b) - dos vectores de la misma longitud
# resta entre dos vectores a y b. (a - b)
def mathVectorSubstraction(a, b):
    if len(a) != len(b):
        return

    length = len(a)
    c = [0 for x in a]

    for entry in range(length):
        c[entry] = a[entry] - b[entry]

    return c

# (a, b) - dos vectores de la misma longitud
# suma entre dos vectores a y b. (a - b)
def mathVectorAdd(a, b):
    if len(a) != len(b):
        return

    length = len(a)
    c = [0 for x in a]

    for entry in range(length):
        c[entry] = a[entry] + b[entry]

    return c

# (a) - vector de cualquier largo
# normalización de un vector
def mathLinalgNormal(a):
    normal = 0
    for x in a:
        normal += x **2

    normal = normal ** 0.5

    for x in range(len(a)):
        try:
            a[x] /= normal
        except ZeroDivisionError:
            pass
    
    return a

# (a) - vector de cualquier largo
# encuentra la normal de un vector 
# implementación del método de Frobenius
def mathFrobenius(a):
    normal = 0
    for x in a:
        normal += x **2

    normal = normal ** 0.5

    return normal

# (escalar, vector) - vector de 1D
# se multiplica cada valor del vector por el escalar
def mathVectorTimesScalar(scalar, vector):
    result = []
    for x in vector:
        result.append(x * scalar)

    return result

# (a, b) - dos vectores del mismo tamaño
# se multiplica el vector por cada posicion
def mathVectorMultiplication(a, b):
    result = [0 for x in a]
    for i in range(len(a)):
            result[i] = a[i] * b[i]

    return result

# (vA, vB, vC, vP) - vectores de la misma longitud
# calcula las coordenadas baricentricas
def baricentricCoordinates(vA, vB, vC, vP):
    # u corresponde a vA, v corresponde a vB, w corresponde a vC
    try:
        u = (
            ( (vP[0] - vC[0]) * (vB[1] - vC[1]) + (vP[1] - vC[1]) * (vC[0] - vB[0]) ) 
            /
            ( (vA[0] - vC[0]) * (vB[1] - vC[1]) + (vA[1] - vC[1]) * (vC[0] - vB[0]) ) 
            )

        v = ( 
            ( (vP[0] - vC[0]) * (vC[1] - vA[1]) + (vP[1] - vC[1]) * (vA[0] - vC[0]) ) 
            /
            ( (vA[0] - vC[0]) * (vB[1] - vC[1]) + (vA[1] - vC[1]) * (vC[0] - vB[0]) ) 
            )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

BLACK = color(0, 0, 0)
WHITE = color(1, 1, 1)

class RayTracer(object):
    def __init__(self, w, h):
        self.glInit(w, h)
    
    # no tiene parámetros
    # esta función se ejecuta al crear un objeto de tipo render
    # inicializa las variables necesarias en su valor default
    def glInit(self, w, h):

        # colores default
        self.clear_color = BLACK
        self.point_color = WHITE

        # se crea la ventana
        self.glCreateWindow(w, h)

        # cámara y campo de visión
        self.cam_position = [0, 0, 0]
        self.fov = 60

        # se almacenan los elementos de la escena (solamente se revisan los rays una vez)
        # ayuda a la optimizacion
        self.scene = []
        self.material = None

        # valores para simular la luz en los objetos de la escena
        self.point_light = None
        self.ambient_light = None

    # (width, height)
    # se inicializa el framebuffer con la altura y ancho indicados
    def glCreateWindow(self, w, h):
        # altura y largo de la ventana
        self.height = round(h)
        self.width = round(w)

        # se hace un clear 
        self.glClear()

        # se crea un viewport del tamaño de la ventana
        self.glViewPort(0, 0, w, h)
        
        return True

    # no tiene parametros
    # se llena el mapa de bits con el color seleccionado
    def glClear(self):
        self.pixels = [[self.clear_color for x in range(self.width)] for y in range(self.height)]

        #Z - buffer, depthbuffer, buffer de profudidad
        self.zbuffer = [ [ 10000 for x in range(self.width)] for y in range(self.height) ]

    # (r, g, b) - valores entre 0 y 1
    # define el color con el que se realiza el clear
    def glClearColor(self, r, g, b):
        if r > 1 or r < 0 or g > 1 or g < 0 or b > 1 or b < 0:
            return False
        
        self.clear_color = color(r, g, b)
        return True

    # (base, extra) - dos colores
    # simula fondos como estrellas, nieve, etc.
    def glBackground(self, r, g, b):
        self.glClearColor(r, g, b)
        self.glClear()

        for x in range(2, self.width - 2):
            for y in range(2, self.height - 2):
                if random.random() < 0.001:
                    size = random.randint(1, 2)
                    if size == 1:
                        self.glVertexNDC(x, y)
                    else:
                        self.glVertexNDC(x, y)
                        self.glVertexNDC(x + 1, y)
                        self.glVertexNDC(x - 1, y)
                        self.glVertexNDC(x, y + 1)
                        self.glVertexNDC(x, y - 1)

    # (r, g, b) - valores entre 0 y 1
    # define el color con el que se dibuja el punto
    def glColor(self, r, g, b):
        if r > 1 or r < 0 or g > 1 or g < 0 or b > 1 or b < 0:
            return False

        self.point_color = color(r, g, b)
        return True

    # (x, y, width, height)
    # crea el viewport en donde se podrá dibujar
    # restringe al viewport dentro de la ventana
    def glViewPort(self, x, y, width, height):
        if x > self.width or y > self.height:
            return False
        elif x + width > self.width or y + height > self.height:
            return False
        else:
            # se pasan los valores del viewport
            self.vp_start_point_x = x
            self.vp_start_point_y = y
            self.vp_width = width
            self.vp_height = height

            return True

    # no tiene parámetros
    # función extra
    # dibuja el contorno del viewport 
    def glDrawViewPort(self):
        for x in range(self.vp_start_point_x, self.vp_start_point_x + self.vp_width):
            self.pixels[self.vp_start_point_y][x] = color(255, 0, 251)
            self.pixels[self.vp_start_point_y + self.vp_height][x] = color(255, 0, 251)
        
        for y in range(self.vp_start_point_y, self.vp_start_point_y + self.vp_height):
            self.pixels[y][self.vp_start_point_x] = color(255, 0, 251)
            self.pixels[y][self.vp_start_point_x + self.vp_width] = color(255, 0, 251)

    # (x, y) - valores entre -1 y 1
    # se crea un punto dentro del viewport
    # las coordenadas son relativas al viewport
    def glVertex(self, x, y):
        if x > 1 or x < -1 or y > 1 or y < -1:
            return False
        else:
            new_x = (x + 1) * (self.vp_width / 2) + self.vp_start_point_x
            new_y = (y + 1) * (self.vp_height / 2) + self.vp_start_point_y
            self.pixels[round(new_y - 1) if round(new_y) == self.vp_height else round(new_y)][round(new_x - 1) if round(new_x) == self.vp_width else round(new_x)] = self.point_color

            return True

    # (x, y) - coordenadas
    # recibe las coordenadas en pixeles para dibujar 
    def glVertexNDC(self, x, y, color = None):
        self.pixels[(y - 1) if y == self.vp_height else y][(x - 1) if x == self.vp_width else x] = color or self.point_color
    
    # no recibe parámetros
    # revisión de rayos para dibujar o no el pixel
    def glRayTracingRender(self):
        for y in range(self.height):
            for x in range(self.width):

                # campo de vision
                t = tan((self.fov * np.pi / 180) / 2)
                r = t * self.width / self.height

                # coordenadas NDC 
                px = (2 * ((x + 0.5) / self.width) - 1) * r
                py = (2 * ((y + 0.5) / self.height) - 1) * t

                #  direccion de la cámara
                direction = [px, py, -1]
                direction = mathLinalgNormal(direction)

                material = None
                intersect = None

                for figure in self.scene:
                    ray_intersect = figure.ray_intersect(self.cam_position, direction)
                    if ray_intersect is not None:
                        if ray_intersect.distance < self.zbuffer[y][x]:
                            self.zbuffer[y][x] = ray_intersect.distance
                            material = figure.material
                            intersect = ray_intersect
                
                # se dibuja el pixel solamente si hay intersección 
                if intersect:
                    self.glVertexNDC(x, y, self.glPointColor(material, intersect))

    def glPointColor(self, material, intersect):
        object_color = [
            material.diffuse[2] / 255,
            material.diffuse[1] / 255,
            material.diffuse[0] / 255,
        ]

        ambient_color = diffuse_color = spec_color = [0, 0, 0]

        shadow_intensity = 0

        if self.ambient_light:
            ambient_color = [
                self.ambient_light.strength * self.ambient_light.color[2] / 255,
                self.ambient_light.strength * self.ambient_light.color[1] / 255,
                self.ambient_light.strength * self.ambient_light.color[0] / 255,

            ]

        if self.point_light:
            light_direction = mathVectorSubstraction(self.point_light.position, intersect.point)
            light_direction = mathLinalgNormal(light_direction)

            dot = mathDotProduct(light_direction, intersect.normal)
            intensity = self.point_light.intensity * 0 if dot < 0 else dot

            diffuse_color = [
                intensity * self.point_light.color[2] / 255,
                intensity * self.point_light.color[1] / 255,
                intensity * self.point_light.color[0] / 255,
            ]

            view_direction = mathLinalgNormal(mathVectorSubstraction(self.cam_position, intersect.point))

            reflect = 2 * mathDotProduct(intersect.normal, light_direction)
            reflect = mathVectorTimesScalar(reflect, intersect.normal)
            reflect = mathVectorSubstraction(reflect, light_direction)

            spec_intensity = self.point_light.intensity * (max(0, mathDotProduct(view_direction, reflect)) ** material.spec)

            spec_color = [
                spec_intensity * self.point_light.color[2] / 255,
                spec_intensity * self.point_light.color[1] / 255,
                spec_intensity * self.point_light.color[0] / 255,
            ]

            for figure in self.scene:
                if figure is not intersect.sceneObject:
                    ray_intersect = figure.ray_intersect(intersect.point, light_direction)
                    if ray_intersect is not None and intersect.distance < mathFrobenius(mathVectorSubstraction(self.point_light.position, intersect.point)):
                        shadow_intensity = 1

            multiplier = mathVectorAdd(ambient_color, mathVectorTimesScalar((1 - shadow_intensity), mathVectorAdd(diffuse_color, spec_color)))
            final_color = mathVectorMultiplication(multiplier, object_color)

            r = min(1, final_color[0])
            g = min(1, final_color[1])
            b = min(1, final_color[2])

        return color(r, g, b)

    # no tiene parámetros
    # renderiza el mapa de bits
    def glFinish(self, filename):
        file = open(filename, 'wb')

        # file header
        file.write(bytes('B'.encode('ascii')))
        file.write(bytes('M'.encode('ascii')))
                   
        file.write(dword(14 + 40 + self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(14 + 40))

        # image header
        file.write(dword(40))
        file.write(dword(self.width))
        file.write(dword(self.height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        # pixels, 3 bytes each
        for x in range(self.height):
            for y in range(self.width):
                file.write(self.pixels[x][y])

        file.close()

    # función para exportar los valores del zbuffer en un archivo bmp
    def glZBuffer(self):
        file = open('zbuffer.bmp', 'wb')

        # File header 14 bytes
        file.write(bytes('B'.encode('ascii')))
        file.write(bytes('M'.encode('ascii')))
        file.write(dword(14 + 40 + self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(14 + 40))

        # Image Header 40 bytes
        file.write(dword(40))
        file.write(dword(self.width))
        file.write(dword(self.height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        # max y min valores para z
        minZ = 10000
        maxZ = -10000

        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] == -10000:
                    pass
                else:
                    if minZ > self.zbuffer[x][y]:
                        minZ = self.zbuffer[x][y]
                    if maxZ < self.zbuffer[x][y]:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -10000:
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                file.write(color(depth, depth, depth))

        file.close()