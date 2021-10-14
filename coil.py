from typing import Any

import math

'''
    coiling_shape --> ordered collection on points in 2 dimensions
        centered around the origin. This can be a function along the
        coiling axis.

    coiling_axis --> specify the start and end points of the interpolation.
        Additional information: the start and end degrees, and the rate
        of coiling i.e. how far the move vertically per rotation
        ** end angle is overspecification based on coiling rate.
        ** also, coiling rate can be a function of coiling axis
        ** also specifying the number of iterations

    coiling_radius --> the distance from the coiling axis to the center of
        the generating shape. This can be a function along the coiling axis.
'''

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

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        return self.__mul__(1/ self.__abs__()) 

    def project(self, other: 'Vector3'):
        normal = other.normalize()
        return normal * self.__mul__(normal)

    def __str__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)

    def to_list(self):
        return [self.x, self.y, self.z]

class coiling_axis(object):
    def __init__(self, start_point: Vector3, end_point: Vector3, start_angle: Vector3, coiling_rate: float, iterations: int):
        self.start_point = start_point
        self.end_point = end_point

        axial_vector = end_point - start_point
        self.start_angle = start_angle - start_angle.project(axial_vector)
        
        self.coiling_rate = coiling_rate
        self.max_iterations = iterations
        self.current_iteration = 0

    def get_axis_location(self):
        diff_vector = self.end_point - self.start_point
        return self.start_point + (self.current_iteration / self.max_iterations) * diff_vector

    def get_normal_vector(self):
        diff_vector = self.end_point - self.start_point
        curr_angle = self.start_angle + self.coiling_rate * self.current_iteration



    

def generate_coil(generating_shape, coiling_axis, coiling_radius):
    pass