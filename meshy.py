import bpy
import requests
import os

class OBJECT_OT_send_to_meshy(bpy.types.Operator):
    bl_idname = "object.send_to_meshy"
    bl_label = "Convert Image to Mesh"
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'IMAGE'
    
    def execute(self, context):
        api_key = 'YOUR_API_KEY_HERE'
        headers = {'Authorization': f'Bearer {api_key}'}
        url = 'https://api.meshy.ai/v1/image-to-3d'

        # Assuming the image is saved and accessible
        image_path = bpy.path.abspath(context.active_object.filepath)
        files = {'file': open(image_path, 'rb')}
        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            json_response = response.json()
            model_url = json_response['model_urls']['glb']  # Assuming GLB format is desired
            
            # Download the GLB file
            model_response = requests.get(model_url)
            if model_response.status_code == 200:
                model_path = os.path.join(bpy.path.abspath('//'), 'downloaded_model.glb')
                with open(model_path, 'wb') as f:
                    f.write(model_response.content)
                
                # Import the model into Blender
                bpy.ops.import_scene.gltf(filepath=model_path)
            else:
                self.report({'ERROR'}, "Failed to download the model")
                return {'CANCELLED'}
        else:
            self.report({'ERROR'}, "API request failed")
            return {'CANCELLED'}
        
        self.report({'INFO'}, "Model imported successfully")
        return {'FINISHED'}
        
class OBJECT_PT_meshy_panel(bpy.types.Panel):
    bl_label = "Meshy AI Integration"
    bl_idname = "OBJECT_PT_meshy"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        self.layout.operator(OBJECT_OT_send_to_meshy.bl_idname)
        
def register():
    bpy.utils.register_class(OBJECT_OT_send_to_meshy)
    bpy.utils.register_class(OBJECT_PT_meshy_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_send_to_meshy)
    bpy.utils.unregister_class(OBJECT_PT_meshy_panel)

if __name__ == "__main__":
    register()