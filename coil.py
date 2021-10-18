import bpy
from typing import Any, Union

import math

class Vector2(object):
    def __init__(self, x, y):
        self.x = x
        self.y =y
    
    def __add__(self, other: 'Vector2'):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other: Any):
        if type(other) is type(self):
            return self.x * other.x + self.y * other.y
        else:
            return Vector2(other * self.x, other * self.y)

    def __rmul__(self, other: Any):
        return self.__mul__(other)

    def __sub__(self, other: 'Vector3'):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-1 * self.x, -1 * self.y)

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def normalize(self):
        return self.__mul__(1/ self.__abs__()) 

    def project(self, other: 'Vector2'):
        normal = other.normalize()
        return normal * self.__mul__(normal)

    def to_list(self):
        return [self.x, self.y]

class Vector3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y =y
        self.z = z
    
    def __add__(self, other: 'Vector3'):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other: Any):
        if type(other) is type(self):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            return Vector3(other * self.x, other * self.y, other * self.z)

    def __rmul__(self, other: Any):
        return self.__mul__(other)

    def __sub__(self, other: 'Vector3'):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vector3(-1 * self.x, -1 * self.y, -1 * self.y)

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        return self.__mul__(1/ self.__abs__()) 

    def project(self, other: 'Vector3'):
        normal = other.normalize()
        return normal * self.__mul__(normal)

    def __str__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)

    def __pow__(self, other: 'Vector3'):
        return Vector3(self.y * other.z - other.y * self.z, - self.x * other.z + other.x * self.z, self.x * other.y - other.x * self.y)

    def to_list(self):
        return [self.x, self.y, self.z]

def make_lambda_function(input):
    if type(input) is float or type(input) is int:
        return lambda x : input
    elif type(input) is type(lambda x : None):
        return input

class coiling_axis(object):
    def __init__(self, start_point: Vector3, tangent: Vector3, normal: Vector3, coiling_rate, displacement, coiling_radius, scaling_factor, iterations: int):        
        self.start_point = start_point

        self.tangent = tangent.normalize()
        self.normal = (normal - normal.project(tangent)).normalize()
        self.binormal = (normal ** tangent).normalize()

        self.displacement = make_lambda_function(displacement)
        self.coiling_rate = make_lambda_function(coiling_rate)
        self.coiling_radius = make_lambda_function(coiling_radius)
        self.scaling_factor = make_lambda_function(scaling_factor)

        self.max_iterations = iterations
        self.current_iteration = 0

    def get_axis_position(self):
        current_axis_position = self.displacement(self.current_iteration)
        return current_axis_position * self.tangent + self.start_point

    def get_normal_vector(self):
        current_angle = self.coiling_rate(self.current_iteration)
        return math.cos(current_angle) * self.normal + math.sin(current_angle) * self.binormal

    def get_tangent_vector(self):
        return self.tangent

    def get_radius(self):
        return self.coiling_radius(self.current_iteration)

    def get_scaling_factor(self):
        return self.scaling_factor(self.current_iteration)

    def iterate(self):
        self.current_iteration += 1
        return self.current_iteration < self.max_iterations

def make_circle(r, n):
    center = Vector2(0, 0)
    theta = 2 * math.pi / n
    vertices = []
    for i in range(0, n):
        r_i = r * Vector2(math.cos(i * theta), math.sin(i * theta))
        p_i = center + r_i
        vertices.append(p_i)
    return vertices

def generate_coil(generating_shape, coiling_axis):
    vertices = []
    n_vertices = 0
    edges = []
    faces = []

    last_vertices = []
    tangent = coiling_axis.get_tangent_vector()

    while coiling_axis.iterate():
        new_vertices = []

        axis_position = coiling_axis.get_axis_position()
        normal = coiling_axis.get_normal_vector()
        coiling_radius = coiling_axis.get_radius()
        scaling_factor = coiling_axis.get_scaling_factor()

        iteration_center = axis_position + coiling_radius * normal

        for gen_v in generating_shape:
            gen_v = scaling_factor * gen_v
            v = iteration_center + gen_v.x * normal + gen_v.y * tangent
            new_vertices.append(n_vertices)
            vertices.append(v.to_list())
            n_vertices += 1

        l = len(generating_shape)
        for i in range(0, l):
            edges.append([new_vertices[i], new_vertices[(i + 1) % l]])

            if (last_vertices):
                edges.append([last_vertices[i], last_vertices[(i + 1) % l]])
                edges.append([last_vertices[i], new_vertices[i]])
                edges.append([last_vertices[(i + 1) % l], new_vertices[(i + 1) % l]])

                faces.append([
                    last_vertices[i], last_vertices[(i + 1) % l],
                    new_vertices[(i + 1) % l], new_vertices[i]
                ])
                
        last_vertices = new_vertices

    generate_mesh(vertices, edges, faces)

def generate_mesh(vertices, edges, faces):
    new_mesh = bpy.data.meshes.new('new_mesh')
    new_mesh.from_pydata(vertices, edges, faces)
    new_mesh.update()

    new_object = bpy.data.objects.new('new_object', new_mesh)

    new_collection = bpy.data.collections.new('new_collection')
    bpy.context.scene.collection.children.link(new_collection)

    new_collection.objects.link(new_object)
    
# Generating some seashells...

# Tubular Shell
start = Vector3(0,0,10)
tangent = Vector3(0,0,1)
normal = Vector3(1,0,0)

l = 2

def coiling_rate(n):
    return n * math.pi / 18

def displacement(n):
    return 0

def coiling_radius(n):
    return 0.0005 * n ** 2

def scaling_factor(n):
    return 0.0005 * n ** 2

iterations = 109

axis = coiling_axis(start, tangent, normal, coiling_rate, displacement, coiling_radius, scaling_factor, iterations)
circle = make_circle(1, 20)

generate_coil(circle, axis)

# Classical shell
start = Vector3(20,0,0)
tangent = Vector3(0,0,1)
normal = Vector3(1,0,0)

l = 1.01

def coiling_rate(n):
    return n * math.pi / 18

def displacement(n):
    return 5 * l ** (n - 300)

def coiling_radius(n):
    return l ** (n - 300)

def scaling_factor(n):
    return l ** (n - 300)

iterations = 400

axis = coiling_axis(start, tangent, normal, coiling_rate, displacement, coiling_radius, scaling_factor, iterations)
circle = make_circle(1, 20)

generate_coil(circle, axis)

# spherical shell

start = Vector3(35,0,0)
tangent = Vector3(0,0,1)
normal = Vector3(1,0,0)

l = 1.03

def coiling_rate(n):
    return n * math.pi / 18

def displacement(n):
    return 0.35 * 1.5 * l ** (n - 300)

def coiling_radius(n):
    return 0.35 * l ** (n - 300)

def scaling_factor(n):
    return 0.35 * l ** (n - 300)

iterations = 400

axis = coiling_axis(start, tangent, normal, coiling_rate, displacement, coiling_radius, scaling_factor, iterations)
circle = make_circle(1, 20)

generate_coil(circle, axis)

# custom generating curve shell...

start = Vector3(55,0,0)
tangent = Vector3(0,0,1)
normal = Vector3(1,0,0)

l = 1.03

def coiling_rate(n):
    return n * math.pi / 18

def displacement(n):
    return 0.5 * 1.5 * l ** (n - 300)

def coiling_radius(n):
    return 0

def scaling_factor(n):
    return 0.5 * (l ** (n - 300)) / 6

iterations = 400

axis = coiling_axis(start, tangent, normal, coiling_rate, displacement, coiling_radius, scaling_factor, iterations)
generating_curve = [
    Vector2(0,-6), Vector2(0,-4), Vector2(0,-2), Vector2(0,0), Vector2(0,2), Vector2(0,4), Vector2(0,6),
    Vector2(0.2, 6.3), Vector2(0.4, 6.1), Vector2(0.672, 5.5), Vector2(0.845, 5), Vector2(1, 4), Vector2(2, 2),
    Vector2(3.394, 0), Vector2(4.363, -2), Vector2(3.394, -4), Vector2(1.104, -6), Vector2(0.4, -6.4), Vector2(0.2, -6.3)
]

generate_coil(generating_curve, axis)

# Patelliform Shell
start = Vector3(65,0,10)
tangent = Vector3(0,1,0)
normal = Vector3(1,0,0)

l = 1.34

def coiling_rate(n):
    return n * math.pi / 18

def displacement(n):
    return 0

def coiling_radius(n):
    return 0.0075 * l ** (n - 300)

def scaling_factor(n):
    return 0.0075 * l ** (n - 300)

iterations = 325

axis = coiling_axis(start, tangent, normal, coiling_rate, displacement, coiling_radius, scaling_factor, iterations)
circle = make_circle(1, 20)

generate_coil(circle, axis)
