import bpy
from bpy.props import IntProperty, FloatProperty
from bpy.types import Operator, Panel
from mathutils import Vector

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