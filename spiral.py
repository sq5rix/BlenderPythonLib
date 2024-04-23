import bpy
import math

def create_spiral(initial_diameter, turns, height, diameter_growth_percent):
    # Calculate the initial radius from the diameter
    initial_radius = initial_diameter / 2.0

    # Calculate the total number of steps (one step per degree for smoothness)
    total_steps = int(turns * 360)
    z_step = height / total_steps  # Height increment per step
    angle_step = 2 * math.pi / 360  # Radians per step

    # Radius increment per step based on growth percent
    radius_growth_per_step = initial_radius * (diameter_growth_percent / 100) / 360

    # Create a new curve
    curve_data = bpy.data.curves.new('SpiralCurve', type='CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new('POLY')
    spline.points.add(total_steps - 1)  # total_steps points, one is already there

    # Populate the spline with points
    radius = initial_radius
    for i in range(total_steps):
        x = radius * math.cos(i * angle_step)
        y = radius * math.sin(i * angle_step)
        z = i * z_step
        spline.points[i].co = (x, y, z, 1)  # The fourth value (w) must be 1 for POLY type splines

        # Increase the radius for the next point
        radius += radius_growth_per_step

    # Create a new object with the curve
    curve_obj = bpy.data.objects.new('SpiralObject', curve_data)
    bpy.context.collection.objects.link(curve_obj)
    bpy.context.view_layer.objects.active = curve_obj
    curve_obj.select_set(True)

    return curve_obj

# Example usage
initial_diameter = 1.0
turns = 5
height = 5.0
diameter_growth_percent = 10.0

create_spiral(initial_diameter, turns, height, diameter_growth_percent)