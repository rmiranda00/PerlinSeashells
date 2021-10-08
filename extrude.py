import bpy
import math
import numpy as np

def v_index(i, j, n):
    return i * n + j

def interpolate_mesh(start_vertices, end_vertices, iterations):
    vertices = []
    edges = []
    faces = []

    difference_vectors = end_vertices - start_vertices
    n = len(start_vertices)

    for i in range(0, iterations + 1):
        for j in range(0, n):
            start_v = start_vertices[j]
            diff_v = difference_vectors[j]

            vertex = start_v + (1.0 * i / iterations) * diff_v

            vertices.append(list(vertex))

    for i in range(0, iterations + 1):
        for j in range(0, n):
            bottom_left = v_index(i, j, n)
            bottom_right = v_index(i, (j + 1) % n, n)

            edges.append([bottom_left, bottom_right])

            if i < iterations:
                top_left = v_index(i + 1, j, n)
                top_right = v_index(i + 1, (j+1) % n, n)

                edges += [
                    [bottom_left, top_left], 
                    [bottom_right, top_right], 
                    [top_left, top_right]
                ]

                faces.append([bottom_left, bottom_right, top_right, top_left])

    new_mesh = bpy.data.meshes.new('new_mesh')
    new_mesh.from_pydata(vertices, edges, faces)
    new_mesh.update()

    new_object = bpy.data.objects.new('new_object', new_mesh)

    new_collection = bpy.data.collections.new('new_collection')
    bpy.context.scene.collection.children.link(new_collection)

    new_collection.objects.link(new_object)

def make_circle(x, y, z, r, n):
    center = np.array([x, y, z])
    theta = 2 * math.pi / n
    vertices = []
    for i in range(0, n):
        xi = r * math.cos(i * theta) + center[0]
        yi = r * math.sin(i * theta) + center[1]
        zi = z
        pi = np.array([xi, yi, zi])
        vertices.append(pi)
    return np.array(vertices)    
    
c1 = make_circle(0, 0, 0, 1, 100)
c2 = make_circle(0,0,10,2,100)

interpolate_mesh(c1, c2, 20)
