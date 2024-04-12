import bpy
from bpy.props import IntProperty, FloatProperty
from bpy.types import Operator, Panel
from mathutils import Vector 

def animate_object_along_curve(obj, curve, start_frame, end_frame):
    # Check if the curve is a valid curve object
    if curve.type != 'CURVE':
        print("The provided curve object is not a curve.")
        return

    # Create or find the Follow Path constraint
    follow_path_constraint = None
    for constraint in obj.constraints:
        if constraint.type == 'FOLLOW_PATH':
            follow_path_constraint = constraint
            break
    else:
        follow_path_constraint = obj.constraints.new(type='FOLLOW_PATH')

    # Set the curve target and options
    follow_path_constraint.target = curve
    follow_path_constraint.use_curve_follow = True
    follow_path_constraint.forward_axis = 'FORWARD_Y'
    follow_path_constraint.up_axis = 'UP_Z'

    # Set the object at the start of the curve
    obj.location = curve.splines[0].bezier_points[0].co
    obj.keyframe_insert(data_path="location", frame=start_frame)

    # Insert keyframe for the constraint influence
    follow_path_constraint.offset_factor = 0.0
    follow_path_constraint.keyframe_insert(data_path="offset_factor", frame=start_frame)

    # Set the object at the end of the curve
    obj.location = curve.splines[0].bezier_points[-1].co
    obj.keyframe_insert(data_path="location", frame=end_frame)

    # Insert keyframe for the constraint influence
    follow_path_constraint.offset_factor = 1.0
    follow_path_constraint.keyframe_insert(data_path="offset_factor", frame=end_frame)

    print("Animation setup completed.")


def create_bezier_curves_between_face_pairs(face_pairs):
    curve_objects = []  
    # To store references to the created curve objects
    # todo reat global faces 
    for face_data_1, face_data_2 in face_pairs:
        center1, normal1 = face_data_1
        center2, normal2 = face_data_2
        
        # Calculate handle positions
        distance = (center1 - center2).length
        height_factor = 4
        handle1 = center1 + normal1.normalized() * distance * height_factor
        handle2 = center2 + normal2.normalized() * distance * height_factor

        # Create and configure the curve
        curve_data = bpy.data.curves.new(name="BezierCurve", type='CURVE')
        curve_data.dimensions = '3D'
        spline = curve_data.splines.new('BEZIER')
        spline.bezier_points.add(1)

        p0, p1 = spline.bezier_points[0], spline.bezier_points[1]
        p0.co = center1
        p0.handle_right_type = 'FREE'
        p0.handle_right = handle1
        p1.co = center2
        p1.handle_left_type = 'FREE'
        p1.handle_left = handle2

        # Create curve object and add to the scene
        curve_obj = bpy.data.objects.new("BezierCurveObj", curve_data)
        bpy.context.scene.collection.objects.link(curve_obj)
        curve_objects.append(curve_obj)
    
    return curve_objects

# Global variable to store the data of selected faces
GLOBAL_FACE_DATA = []

def store_selected_faces_data(obj):
    """Store the center and normal of selected faces."""
    selected_faces_info = []
    if obj.type == 'MESH':
        mesh = obj.data
        for poly in mesh.polygons:
            if poly.select:
                center = sum((obj.matrix_world @ obj.data.vertices[vert].co for vert in poly.vertices), Vector()) / len(poly.vertices)
                normal = obj.matrix_world.to_3x3() @ poly.normal
                selected_faces_info.append((center, normal))
    return selected_faces_info

class SWARM_OT_CaptureFaces(Operator):
    bl_idname = "swarm.capture_faces"
    bl_label = "Capture Faces"
    bl_description = "Capture selected faces for the swarm animation"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        global GLOBAL_FACE_DATA
        GLOBAL_FACE_DATA = store_selected_faces_data(context.active_object)
        self.report({'INFO'}, F"Captured {len(GLOBAL_FACE_DATA)} faces")
        return {'FINISHED'}

class SWARM_OT_animate(Operator):
    bl_idname = "swarm.animate"
    bl_label = "Animate Swarm"
    bl_description = "Animate a swarm of objects between selected faces"
    bl_options = {'REGISTER', 'UNDO'}

    number_of_objects: IntProperty(name="Number of Objects", default=10, min=1)
    min_height: FloatProperty(name="Min Fly Height", default=1.0, min=0.1)
    max_height: FloatProperty(name="Max Fly Height", default=2.0, min=0.1)
    min_rest_time: FloatProperty(name="Min Rest Time", default=1.0, min=0.0)
    max_rest_time: FloatProperty(name="Max Rest Time", default=3.0, min=0.1)

    def execute(self, context):
        # Here, you would implement the logic to animate objects based on GLOBAL_FACE_DATA
        # and the parameters provided by the user.
        return {'FINISHED'}

class SWARM_PT_Panel(Panel):
    bl_label = "Swarm Animation"
    bl_idname = "SWARM_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Swarm'

    def draw(self, context):
        layout = self.layout
        layout.operator(SWARM_OT_CaptureFaces.bl_idname)
        layout.operator(SWARM_OT_animate.bl_idname)

def register():
    bpy.utils.register_class(SWARM_OT_CaptureFaces)
    bpy.utils.register_class(SWARM_OT_animate)
    bpy.utils.register_class(SWARM_PT_Panel)

def unregister():
    bpy.utils.unregister_class(SWARM_OT_CaptureFaces)
    bpy.utils.unregister_class(SWARM_OT_animate)
    bpy.utils.unregister_class(SWARM_PT_Panel)

if __name__ == "__main__":
    register()