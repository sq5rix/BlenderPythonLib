import bpy
from mathutils import Vector

bl_info = {
    "name": "Studio Lights",
    "blender": (2, 80, 0),
    "category": "Scene",
}

def look_at(obj, target):
    """
    Rotates 'obj' to look towards 'target' point.
    :param obj: The object to be oriented.
    :param target: The location (as a Vector) to be targeted.
    """
    # Direction from the object to the target point
    direction = target - obj.location
    # Point the object's '-Z' and 'Y' towards the target
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quat.to_euler()


class StudioLightsSetup():
    def __init__(self, collection_name="StudioLights"):
        self.collection = self.ensure_collection(collection_name)
        self.cursor_location = bpy.context.scene.cursor.location
        self.main_object_size = 2 * self.calculate_scene_sphere_radius()
        self.light_height = 5
        print('self.main_object_size : ', self.main_object_size )

    def point_light_to_cursor(self, light_name):
        """
        Points the light object with the given name towards the 3D cursor.
        :param light_name: The name of the light object.
        """
        # Get the light object by name
        light = bpy.data.objects.get(light_name)
        if not light or light.type != 'LIGHT':
            print(f"No light found with the name '{light_name}'.")
            return

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
        self.point_light_to_cursor(light.name)

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
        location = (2 * self.main_object_size, -self.main_object_size, self.light_height)
        self.create_light("AREA", "Fill Light", location, -2, 500, (0.8, 0.8, 1))

    def add_rim_light(self):
        location = (0, -2 * self.main_object_size, 2)
        self.create_light("AREA", "Rim Light", location, 1, 750, (1, 0.8, 0.5))

    def add_front_spotlight(self):
        location = (0, self.main_object_size * 2, self.main_object_size / 2)
        self.create_light("SPOT", "Front Spotlight", location, 0, 500, (1, 1, 1), spot_size=1.0, spot_blend=0.1)

    def calculate_scene_sphere_radius(self):
        """Calculates a sphere radius that contains all the scene objects, excluding cameras and lights."""
        min_coord = Vector((float('inf'), float('inf'), float('inf')))
        max_coord = Vector((float('-inf'), float('-inf'), float('-inf')))

        # Iterate through all scene objects
        for obj in bpy.context.scene.objects:
            # Skip cameras and lights
            if obj.type in {'CAMERA', 'LIGHT'}:
                continue

            # Update the min and max coordinates based on the object's bounding box
            for corner in obj.bound_box:
                world_corner = obj.matrix_world @ Vector(corner)
                min_coord = Vector(map(min, zip(min_coord, world_corner)))
                max_coord = Vector(map(max, zip(max_coord, world_corner)))

        # Calculate the center and the bounding box's dimensions
        center = (min_coord + max_coord) / 2
        dimensions = max_coord - min_coord

        # Calculate the radius as half of the largest dimension
        radius = max(dimensions) / 2

        return radius

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
    bl_label = "Studio Lights"
    bl_description = "Setup studio lighting based on the selected object size"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        studio_lights = StudioLightsSetup()
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

