import bpy

class StudioLightsSetup:
    def __init__(self, main_object_size, collection_name="StudioLights"):
        self.main_object_size = main_object_size
        self.collection = self.ensure_collection(collection_name)

    def ensure_collection(self, collection_name):
        if collection_name not in bpy.data.collections:
            new_collection = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(new_collection)
        return bpy.data.collections[collection_name]

    def create_light(self, light_type, name, location, size, energy, color, spot_size=None, spot_blend=None):
        bpy.ops.object.light_add(type=light_type, location=location)
        light = bpy.context.object
        light.name = name
        light.data.energy = energy
        light.data.color = color

        if light_type == 'AREA':
            light.data.shape = 'DISK'
            light.data.size = size
        elif light_type == 'SPOT':
            light.data.spot_size = spot_size
            light.data.spot_blend = spot_blend
            light.data.show_cone = True

        # Remove light from all collections it was added to, then link to the specified collection
        for col in light.users_collection:
            col.objects.unlink(light)
        self.collection.objects.link(light)
        return light

    def add_key_light(self):
        location = (-self.main_object_size, self.main_object_size, 5)
        self.create_light("AREA", "Key Light", location, 1.5, 1000, (1, 1, 1))

    def add_fill_light(self):
        location = (2 * self.main_object_size, -self.main_object_size, 2)
        self.create_light("AREA", "Fill Light", location, 2, 500, (0.8, 0.8, 1))

    def add_rim_light(self):
        location = (0, -2 * self.main_object_size, 2)
        self.create_light("AREA", "Rim Light", location, 1, 750, (1, 0.8, 0.5))

    def add_front_spotlight(self):
        location = (0, -self.main_object_size * 2, self.main_object_size / 2)
        self.create_light("SPOT", "Front Spotlight", location, 0, 500, (1, 1, 1), spot_size=1.0, spot_blend=0.1)


class StudioLightsSetupPanel(bpy.types.Panel):
    bl_label = "Studio Lights Setup"
    bl_idname = "OBJECT_PT_studio_lights"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.setup_studio_lights", text="Add Studio Lights")

class OBJECT_OT_SetupStudioLights(bpy.types.Operator):
    bl_idname = "object.setup_studio_lights"
    bl_label = "Setup Studio Lights"
    bl_description = "Setup studio lighting based on the selected object size"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        main_object_size = 3  # Example size, adjust as needed
        studio_lights = StudioLightsSetup(main_object_size)
        studio_lights.add_key_light()
        studio_lights.add_fill_light()
        studio_lights.add_rim_light()
        studio_lights.add_front_spotlight()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_SetupStudioLights)
    bpy.utils.register_class(StudioLightsSetupPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SetupStudioLights)
    bpy.utils.unregister_class(StudioLightsSetupPanel)

if __name__ == "__main__":
    register()

