import bpy
from mathutils import Vector

import bpy
from mathutils import Vector

def update_camera_focal_length(camera, target_object, frame, max_frame_coverage=0.7):
    """
    Updates the camera's focal length to ensure the target object occupies a specified maximum
    percentage of the frame.

    Args:
    - camera: The camera object.
    - target_object: The target object to focus on.
    - frame: The current frame number.
    - max_frame_coverage: The maximum percentage of the frame's width or height the object should occupy.
    """
    # Switch to the given frame to calculate current positions
    bpy.context.scene.frame_set(frame)
    
    # Calculate the dimensions of the target object's bounding box in world space
    bbox_corners = [target_object.matrix_world @ Vector(corner) for corner in target_object.bound_box]
    bbox_dimensions = Vector((max(corner.x for corner in bbox_corners) - min(corner.x for corner in bbox_corners),
                              max(corner.y for corner in bbox_corners) - min(corner.y for corner in bbox_corners),
                              max(corner.z for corner in bbox_corners) - min(corner.z for corner in bbox_corners)))
    
    # Calculate the distance from the camera to the target object
    distance_to_target = (camera.location - target_object.location).length
    
    # Calculate the sensor width and height based on the camera's sensor fit
    if camera.data.sensor_fit == 'HORIZONTAL':
        sensor_width = camera.data.sensor_width
        sensor_height = camera.data.sensor_width * camera.data.sensor_height / camera.data.sensor_width
    else:
        sensor_height = camera.data.sensor_height
        sensor_width = camera.data.sensor_height * camera.data.sensor_width / camera.data.sensor_height
    
    # Determine the object's largest dimension and corresponding sensor dimension
    largest_dimension = max(bbox_dimensions)
    sensor_dimension = sensor_width if bbox_dimensions.x == largest_dimension or bbox_dimensions.y == largest_dimension else sensor_height
    
    # Calculate the desired coverage in Blender units on the sensor
    desired_coverage = sensor_dimension * max_frame_coverage
    
    # Calculate the necessary focal length to achieve the desired object coverage
    # Using similar triangles: (largest_dimension / 2) / distance_to_target = (desired_coverage / 2) / focal_length
    new_focal_length = (desired_coverage / 2) * distance_to_target / (largest_dimension / 2)
    
    # Update the camera's focal length
    camera.data.lens = new_focal_length

def setup_camera_rig(curve_name, target_object_name, num_frames, fps, initial_focal_length=50, max_frame_coverage=0.7):
    """
    Enhances the initial setup_camera_rig function with dynamic focal length adjustment
    to keep the target object within a specified frame coverage.

    Additional Args:
    - max_frame_coverage: The maximum percentage of the frame's width or height the target object should occupy.
    """
    # Previous setup_camera_rig implementation...
    
    # Inside the loop that iterates through each frame, call update_camera_focal_length:
    for frame in range(1, num_frames + 1):
        # Existing operations to animate the camera...
        
        # Update the camera's focal length for the current frame
        update_camera_focal_length(camera, target_object, frame, max_frame_coverage)
        
        # Keyframe the new focal length
        camera.data.keyframe_insert(data_path="lens", frame=frame)

# Example usage remains the same...


def setup_camera_rig(curve_name, target_object_name, num_frames, fps, initial_focal_length=50):
    """
    Sets up a camera rig that moves along a Bézier curve focusing on a specified object.

    Args:
    - curve_name (str): The name of the Bézier curve object.
    - target_object_name (str): The name of the object to focus on.
    - num_frames (int): The total number of frames for the animation.
    - fps (int): The frames per second value for the animation.
    - initial_focal_length (float): The initial focal length of the camera.
    """
    
    # Ensure the curve and target object exist
    curve = bpy.data.objects.get(curve_name)
    target_object = bpy.data.objects.get(target_object_name)
    if not curve or not target_object:
        print("Curve or target object does not exist.")
        return
    
    # Create a camera if it doesn't exist
    if "CameraRig" not in bpy.data.objects:
        bpy.ops.object.camera_add()
        camera = bpy.context.object
        camera.name = "CameraRig"
    else:
        camera = bpy.data.objects["CameraRig"]
    
    # Set camera data properties
    camera.data.lens = initial_focal_length
    camera.data.sensor_fit = 'HORIZONTAL'
    
    # Set the animation start and end
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = num_frames
    bpy.context.scene.render.fps = fps
    
    # Create a follow path constraint and attach the camera to the curve
    follow_path_constraint = camera.constraints.new(type='FOLLOW_PATH')
    follow_path_constraint.target = curve
    follow_path_constraint.use_curve_follow = True
    bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner='OBJECT', frame_start=1, length=num_frames)
    
    # Make the camera look at the target object by adding a Track To constraint
    track_to_constraint = camera.constraints.new(type='TRACK_TO')
    track_to_constraint.target = target_object
    track_to_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    track_to_constraint.up_axis = 'UP_Y'
    
    # Animate focal length and DOF distance based on the distance to the target object
    for frame in range(1, num_frames + 1):
        bpy.context.scene.frame_set(frame)
        distance = (camera.location - target_object.location).length
        camera.data.lens = initial_focal_length + distance * 0.1  # Example focal length adjustment
        camera.data.dof.focus_distance = distance
        
        camera.data.keyframe_insert(data_path="lens", frame=frame)
        camera.data.keyframe_insert(data_path="dof.focus_distance", frame=frame)

    print("Camera rig setup complete.")

# Example usage
setup_camera_rig("BezierCurve", "Cube", num_frames=120, fps=24, initial_focal_length=35)
