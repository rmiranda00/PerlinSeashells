import bpy
noise = bpy.data.texts['noise.py'].as_module()


pnf = noise.PerlinNoiseFactory(2, tile=(0, 3))