import bpy
import random
from mathutils import Vector

def create_randomized_curve(length, num_segments, max_displacement):
    # Calculate the height increment per segment
    height_increment = length / num_segments
    
    # Initialize the starting point
    current_point = Vector((0.0, 0.0, 0.0))
    
    # Create a new curve data block
    curve_data = bpy.data.curves.new('RandomCurve', type='CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new('POLY')
    spline.points.add(num_segments)  # Add points; one is already there by default
    
    # Set the first point at the origin
    spline.points[0].co = (current_point.x, current_point.y, current_point.z, 1)

    # Generate and set each subsequent point
    for i in range(1, num_segments + 1):
        # Random displacement in X and Y
        displacement_x = random.uniform(-max_displacement, max_displacement)
        displacement_y = random.uniform(-max_displacement, max_displacement)
        
        # Update current point
        current_point.x += displacement_x
        current_point.y += displacement_y
        current_point.z += height_increment
        
        # Set the point coordinates (the fourth value, w, must be 1 for POLY type splines)
        spline.points[i].co = (current_point.x, current_point.y, current_point.z, 1)

    # Create a new object with the curve
    curve_obj = bpy.data.objects.new('RandomCurveObject', curve_data)
    bpy.context.collection.objects.link(curve_obj)
    bpy.context.view_layer.objects.active = curve_obj
    curve_obj.select_set(True)

    return curve_obj

# Example usage
length = 10.0  # Total length of the curve
num_segments = 10  # Number of segments
max_displacement = 0.5  # Maximum displacement for each segment

create_randomized_curve(length, num_segments, max_displacement)