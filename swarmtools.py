import bpy
from mathutils import Vector

def create_bezier_between_faces(obj, face_index1, face_index2):
    # Ensure the object is a mesh
    if obj.type != 'MESH':
        print("Selected object is not a mesh")
        return

    mesh = obj.data
    # Get the world matrix of the object
    mw = obj.matrix_world
    
    # Get the center and normal of the first face
    f1 = mesh.polygons[face_index1]
    center1 = mw @ sum((obj.data.vertices[vert].co for vert in f1.vertices), Vector()) / len(f1.vertices)
    normal1 = mw.to_3x3() @ f1.normal

    # Get the center and normal of the second face
    f2 = mesh.polygons[face_index2]
    center2 = mw @ sum((obj.data.vertices[vert].co for vert in f2.vertices), Vector()) / len(f2.vertices)
    normal2 = mw.to_3x3() @ f2.normal

    # Calculate the distance between the faces and set the height
    distance = (center1 - center2).length
    height = 4 * distance

    # Calculate control points
    control1 = center1 + normal1 * height
    control2 = center2 + normal2 * height

    # Create the curve
    curve_data = bpy.data.curves.new('BezierCurve', type='CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new(type='BEZIER')
    spline.bezier_points.add(1)
    
    # Assign points
    spline.bezier_points[0].co = center1
    spline.bezier_points[0].handle_right_type = 'FREE'
    spline.bezier_points[0].handle_right = control1
    
    spline.bezier_points[1].co = center2
    spline.bezier_points[1].handle_left_type = 'FREE'
    spline.bezier_points[1].handle_left = control2
    
    # Create curve object
    curve_obj = bpy.data.objects.new('BezierCurveObj', curve_data)
    bpy.context.scene.collection.objects.link(curve_obj)

# Example usage
if bpy.context.object and bpy.context.object.type == 'MESH' and bpy.context.object.mode == 'EDIT':
    bpy.ops.object.mode_set(mode='OBJECT')  # Temporarily switch to Object Mode to access mesh data
    selected_faces = [p.index for p in bpy.context.object.data.polygons if p.select]
    
    if len(selected_faces) == 2:
        create_bezier_between_faces(bpy.context.object, selected_faces[0], selected_faces[1])
    else:
        print("Please select exactly two faces.")
    
    bpy.ops.object.mode_set(mode='EDIT')  # Switch back to Edit Mode