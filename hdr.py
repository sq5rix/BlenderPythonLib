import bpy

H_RES = 1024
RES = 400

import bpy

class RenderSettingsManager:
    def __init__(self):
        """Initialize the RenderSettingsManager by reading current render settings."""
        self.get_render()

    def get_render(self):
        """Reads the current render settings from the scene and stores them in instance variables."""
        scene = bpy.context.scene
        render = scene.render

        self.engine = scene.render.engine
        self.resolution_x = render.resolution_x
        self.resolution_y = render.resolution_y
        self.resolution_percentage = render.resolution_percentage
        self.use_denoising = scene.cycles.use_denoising
        self.file_format = scene.render.image_settings.file_format
        # Add more parameters as needed

    def set_render(self, engine='CYCLES', resolution_x=2048, resolution_y=1024, resolution_percentage=400,
                   use_denoising=True, file_format='HDR'):
        """Sets the render settings for the scene based on the provided parameters."""
        scene = bpy.context.scene
        render = scene.render

        scene.render.engine = engine
        render.resolution_x = resolution_x
        render.resolution_y = resolution_y
        render.resolution_percentage = resolution_percentage
        scene.cycles.use_denoising = use_denoising
        scene.render.image_settings.file_format = file_format
        # Apply additional settings as needed

        # Update instance variables to reflect the changes
        self.get_render()


def add_denoise_node():
    """Adds a Denoise node to the compositor with default values."""
    # Enable use of nodes in the compositor
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree

    # Clear existing nodes
    # Comment out the next line if you don't want to remove existing nodes
    # tree.nodes.clear()

    # Create Denoise node
    denoise_node = tree.nodes.new(type='CompositorNodeDenoise')
    denoise_node.location = (0, 0)  # Adjust the location as needed

    # Connect Denoise node to the Render Layers node and Composite node if not already connected
    render_layers_node = next(node for node in tree.nodes if node.type == 'R_LAYERS')
    composite_node = next(node for node in tree.nodes if node.type == 'COMPOSITE')

    tree.links.new(render_layers_node.outputs['Image'], denoise_node.inputs['Image'])
    tree.links.new(render_layers_node.outputs['Normal'], denoise_node.inputs['Normal'])
    tree.links.new(render_layers_node.outputs['Albedo'], denoise_node.inputs['Albedo'])
    tree.links.new(denoise_node.outputs['Image'], composite_node.inputs['Image'])

def add_glare_node():
    """Adds a Glare node to the compositor with default values."""
    # Ensure use of nodes is enabled
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree

    # Clear existing nodes
    # Comment out the next line if you don't want to remove existing nodes
    # tree.nodes.clear()

    # Create Glare node
    glare_node = tree.nodes.new(type='CompositorNodeGlare')
    glare_node.location = (200, 0)  # Adjust the location as needed
    # Default Glare node values are used, adjust as needed

    # Automatically connecting the Glare node assumes you know which node to connect it to
    # Here we connect it after the Denoise node if it exists, otherwise directly to Render Layers
    render_layers_node = next((node for node in tree.nodes if node.type == 'R_LAYERS'), None)
    denoise_node = next((node for node in tree.nodes if node.type == 'DENOISE'), None)
    composite_node = next(node for node in tree.nodes if node.type == 'COMPOSITE')

    if denoise_node:
        tree.links.new(denoise_node.outputs['Image'], glare_node.inputs['Image'])
    else:
        tree.links.new(render_layers_node.outputs['Image'], glare_node.inputs['Image'])

    tree.links.new(glare_node.outputs['Image'], composite_node.inputs['Image'])



def set_render_settings(hres=H_RES, res_percent=RES, engine='CYCLES', device='GPU', denoise=False, blur=True):
    """Configure render settings."""
    bpy.context.scene.render.engine = engine
    bpy.context.scene.render.resolution_x = 2*hres
    bpy.context.scene.render.resolution_y = hres
    bpy.context.scene.render.resolution_percentage = res_percent
    bpy.context.scene.render.engine = engine
    bpy.context.scene.cycles.device = device
    bpy.context.scene.cycles.use_denoising = denoise
    bpy.context.scene.render.use_motion_blur = blur
    bpy.context.scene.view_layers[0].cycles.use_denoising = denoise

def set_camera_to_panoramic(camera_name='Camera'):
    """Set the camera to panoramic and panoramic type to equirectangular."""
    camera = bpy.data.cameras[camera_name]  # Adjust if your camera is named differently
    camera.type = 'PANO'
    camera.panorama_type = 'EQUIRECTANGULAR'

def render_scene():
    """Render the current scene."""
    bpy.ops.render.render()

def setup_nodes_for_render_output(file_path, file_format='HDR'):
    """Set up compositing nodes to save the render result to a file."""
    scene = bpy.context.scene
    scene.use_nodes = True
    tree = scene.node_tree

    # Clear existing nodes
    tree.nodes.clear()

    # Create Render Layers node
    render_layers_node = tree.nodes.new('CompositorNodeRLayers')

    # Create Output node (File Output)
    output_node = tree.nodes.new('CompositorNodeOutputFile')
    output_node.base_path = ''
    output_node.file_slots[0].path = file_path  # File name and path
    output_node.format.file_format = file_format

    # Link nodes
    tree.links.new(render_layers_node.outputs[0], output_node.inputs[0])

def render_scene_and_save_image(output_file_name='Blender/pano'):
    """Render the scene and save the image using compositor nodes."""
    # Set output file path (relative to the current .blend file)
    output_file_path = f'//{output_file_name}'

    # Configure render settings and camera
    set_render_settings()
    set_camera_to_panoramic()

    #add_denoise_node()
    #add_glare_node()

    # Setup nodes to save render output
    setup_nodes_for_render_output(output_file_path)

    # Render the scene
    bpy.ops.render.render(write_still=True)  # 'write_still' ensures the File Output node writes the file

def register():
    bpy.utils.register_class(CamRigSetupOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    render_scene_and_save_image()

def unregister():
    bpy.utils.unregister_class(CamRigSetupOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
