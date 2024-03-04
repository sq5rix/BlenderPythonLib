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


def look_at(obj, target_point):
    """
    Rotates an object to look at a target point in 3D space.

    Args:
    - obj: The object to orient.
    - target_point: The location (Vector) to look at.
    """
    # Direction from the object to the target point
    direction = target_point - obj.location
    # Point the object's '-Z' and 'Y' towards the target
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
