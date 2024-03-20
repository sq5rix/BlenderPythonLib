import bpy

def animate_camera_along_path(camera_name, path_name, start_frame, end_frame):
    # Get the camera and path objects
    camera = bpy.data.objects.get(camera_name)
    path = bpy.data.objects.get(path_name)

    if not camera:
        print(f"Camera '{camera_name}' not found.")
        return
    
    if not path:
        print(f"Path '{path_name}' not found.")
        return

    # Add or find the Follow Path constraint on the camera
    follow_path_constraint = next((c for c in camera.constraints if c.type == 'FOLLOW_PATH'), None)
    if not follow_path_constraint:
        follow_path_constraint = camera.constraints.new(type='FOLLOW_PATH')

    follow_path_constraint.target = path
    follow_path_constraint.use_curve_follow = True
    follow_path_constraint.forward_axis = 'FORWARD_Y'
    follow_path_constraint.up_axis = 'UP_Z'

    # Clear any existing animation on the camera or path
    camera.animation_data_clear()
    path.animation_data_clear()

    # Set the path to be used for animation
    path.data.use_path = True
    path.data.path_duration = end_frame - start_frame

    # Animate the offset factor of the Follow Path constraint to move the camera along the path
    camera.constraints.update()
    follow_path_constraint.offset_factor = 0.0
    follow_path_constraint.keyframe_insert(data_path="offset_factor", frame=start_frame)
    follow_path_constraint.offset_factor = 1.0
    follow_path_constraint.keyframe_insert(data_path="offset_factor", frame=end_frame)

    print(f"Camera '{camera_name}' is animated along the path '{path_name}' from frame {start_frame} to {end_frame}.")

# Example usage:
camera_name = "Camera"
path_name = "CamPath"
start_frame = 1
end_frame = 800
animate_camera_along_path(camera_name, path_name, start_frame, end_frame)
