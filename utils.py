import bpy
import random
from mathutils import Vector, Euler
import bpy

def clear_scene():
    """
    Removes all objects from the current Blender scene.
    """
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

