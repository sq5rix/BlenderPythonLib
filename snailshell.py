import bpy
import math
from math import radians, sin, cos

def create_snail_shell(steps, initial_radius, growth_factor, angle_step):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("SnailShell")
    obj = bpy.data.objects.new("SnailShell", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Initialize lists for vertices and faces
    verts = []
    faces = []

    # Variables for the spiral calculation
    radius = initial_radius
    angle = 0.0

    # Height increment per step along the z-axis
    height_increment = 0.1
    z = 0.0

    # Create vertices in a spiral
    for i in range(steps):
        x = radius * cos(angle)
        y = radius * sin(angle)
        verts.append((x, y, z))
        
        # Update the radius, angle, and height for next step
        radius += growth_factor
        angle += radians(angle_step)
        z += height_increment
    
    # Add vertices to mesh
    mesh.from_pydata(verts, [], [])

    # Update mesh with new data
    mesh.update()
    return obj

# Example usage
steps = 100
initial_radius = 0.5
growth_factor = 0.1
angle_step = 10  # degrees per step
create_snail_shell(steps, initial_radius, growth_factor, angle_step)