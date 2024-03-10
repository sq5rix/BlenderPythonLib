import bpy

def set_render_settings(res_x=2048, res_y=1024, res_percent=400, engine='CYCLES', device='GPU', denoise=True):
    """Configure render settings."""
    bpy.context.scene.render.engine = engine
    bpy.context.scene.render.resolution_x = res_x
    bpy.context.scene.render.resolution_y = res_y
    bpy.context.scene.render.resolution_percentage = res_percent
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'  # or 'OPENCL'
    bpy.context.scene.cycles.device = device
    bpy.context.scene.cycles.use_denoising = denoise
    bpy.context.scene.view_layers[0].cycles.use_denoising = denoise

def set_camera_to_panoramic(camera_name='Camera'):
    """Set the camera to panoramic and panoramic type to equirectangular."""
    camera = bpy.data.cameras[camera_name]  # Adjust if your camera is named differently
    camera.type = 'PANO'
    camera.cycles.panorama_type = 'EQUIRECTANGULAR'

def render_scene():
    """Render the current scene."""
    bpy.ops.render.render()

def save_hdr_image(file_name='pano.hdr', color_depth='16'):
    """Save the rendered scene as an HDR image."""
    output_path = bpy.path.abspath(f'//{file_name}')
    image = bpy.data.images['Render Result']
    image_settings = bpy.context.scene.render.image_settings
    image_settings.file_format = 'HDR'
    image_settings.color_depth = color_depth
    image_settings.color_mode = 'RGB'
    image.save_render(output_path, scene=bpy.context.scene, save_as_render=True)
    print(f"HDR image saved to: {output_path}")

def setup_and_render_hdr():
    """Main function to setup and render HDR image."""
    set_render_settings()
    set_camera_to_panoramic()
    render_scene()
    save_hdr_image()

# Execute the main function
setup_and_render_hdr()