import bpy
import math

def create_snail_shell(steps, initial_radius, growth_factor, angle_step):
    # Create a new curve
    curve_data = bpy.data.curves.new('SnailShell', type='CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(steps - 1)

    # Variables for the spiral calculation
    radius = initial_radius
    angle = 0.0

    # Height increment per step along the z-axis
    height_increment = 0.1
    z = 0.0

    # Setting points for the spiral
    for i, point in enumerate(spline.bezier_points):
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        point.co = (x, y, z, 1)
        point.handle_right_type = 'VECTOR'
        point.handle_left_type = 'VECTOR'

        radius += growth_factor
        angle += math.radians(angle_step)
        z += height_increment

    # Create the curve object
    curve_obj = bpy.data.objects.new('SnailShell', curve_data)
    bpy.context.collection.objects.link(curve_obj)

    # Convert curve to mesh
    bpy.context.view_layer.objects.active = curve_obj
    curve_obj.select_set(True)
    bpy.ops.object.convert(target='MESH')

    # Apply Solidify modifier
    solidify = curve_obj.modifiers.new(name='Solidify', type='SOLIDIFY')
    solidify.thickness = 0.1  # Set the thickness as desired

    # Apply the Solidify modifier
    bpy.ops.object.modifier_apply(modifier='Solidify')

    return curve_obj

# Example usage
create_snail_shell(100, 0.5, 0.05, 5)