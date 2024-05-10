import bpy
import random
from mathutils import Vector

# Function to create an icosphere
def create_icosphere(size):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=size, location=(0, 0, 0))
    icosphere = bpy.context.object
    icosphere.name = "EmittingIcosphere"
    return icosphere

