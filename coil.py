import bpy

'''
    coiling_shape --> ordered collection on points in 2 dimensions
        centered around the origin. This can be a function along the
        coiling axis.

    coiling_axis --> specify the start and end points of the interpolation.
        Additional information: the start and end degrees, and the rate
        of coiling i.e. how far the move vertically per rotation
        ** end angle is overspecification based on coiling rate.
        ** also, coiling rate can be a function of coiling axis

    coiling_radius --> the distance from the coiling axis to the center of
        the generating shape. This can be a function along the coiling axis.
'''

class Point2(object):
    def __init__(self, x, y):
        self.x = x
        self.y =y
    
    def __add__(self, other: Point2):
        return Point2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float):
        return Point2(scalar * self.x, scalar * self.y)

    def __str__(self):
        return "(%f, %f)".format(self.x, self.y)

    def to_list(self):
        return [self.x, self.y]

class Point3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y =y
        self.z = z
    
    def __add__(self, other: Point3):
        return Point3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar: float):
        return Point3(scalar * self.x, scalar * self.y, scalar * self.z)

    def __str__(self):
        return "(%f, %f, %f)".format(self.x, self.y, self.z)

    def to_list(self):
        return [self.x, self.y, self.z]

class coiling_axis(object):
    def __init__(self, start_point: Point3, end_point: Point3, start_angle, end_angle, coiling_rate):
        pass

def generate_coil(generating_shape, coiling_axis, coiling_radius):
    pass