bl_info = {
    "name": "Swarm",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class SWARM_OT_animate(bpy.types.Operator):
    """Animate a swarm of objects"""
    bl_idname = "object.swarm_animate"
    bl_label = "Swarm Animate"
    bl_options = {'REGISTER', 'UNDO'}

    # Plugin parameters as properties
    number_of_objects: bpy.props.IntProperty(name="Number of Objects", default=10, min=1)
    # Add other properties here

    def execute(self, context):
        # Implementation of the animation logic
        return {'FINISHED'}

class SWARM_PT_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Swarm"
    bl_idname = "OBJECT_PT_swarm"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Swarm'

    def draw(self, context):
        layout = self.layout
        layout.operator(SWARM_OT_animate.bl_idname)

def register():
    bpy.utils.register_class(SWARM_OT_animate)
    bpy.utils.register_class(SWARM_PT_panel)

def unregister():
    bpy.utils.unregister_class(SWARM_OT_animate)
    bpy.utils.unregister_class(SWARM_PT_panel)

if __name__ == "__main__":
    register()