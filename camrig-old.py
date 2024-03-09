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

def setup_camera_rig(curve_name, target_object_name, initial_focal_length=50):
    """
    Sets up a camera rig that moves along a Bézier curve focusing on a specified object,
    adjusting the camera's focal length to keep the target object occupying roughly 70%
    of the frame width or height, depending on its orientation. The animation end frame
    is taken from the current scene settings.

    Args:
    - curve_name (str): The name of the Bézier curve object.
    - target_object_name (str): The name of the object to focus on.
    - initial_focal_length (float): The initial focal length of the camera.
    """
    
    # Ensure the curve and target object exist
    curve = bpy.data.objects.get(curve_name)
    target_object = bpy.data.objects.get(target_object_name)
    if not curve or not target_object:
        print("Curve or target object does not exist.")
        return
    
    # Create or retrieve the camera
    if "CameraRig" not in bpy.data.objects:
        bpy.ops.object.camera_add()
        camera = bpy.context.object
        camera.name = "CameraRig"
    else:
        camera = bpy.data.objects["CameraRig"]
    
    camera.data.sensor_fit = 'HORIZONTAL'
    
    # Use scene's current frame range
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    
    follow_path_constraint = camera.constraints.new(type='FOLLOW_PATH')
    follow_path_constraint.target = curve
    follow_path_constraint.use_curve_follow = True
    bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner='OBJECT', frame_start=start_frame, length=end_frame - start_frame + 1)
    
    track_to_constraint = camera.constraints.new(type='TRACK_TO')
    track_to_constraint.target = target_object
    track_to_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    track_to_constraint.up_axis = 'UP_Y'
    
    # Calculate and animate the focal length
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        
        # Calculate distance to target object and adjust focal length to keep object within frame
        camera_loc = camera.matrix_world.translation
        target_loc = target_object.matrix_world.translation
        direction = (target_loc - camera_loc).normalized()
        distance = (target_loc - camera_loc).length

        # Calculate dimensions of the target object
        dimensions = target_object.dimensions
        max_dimension = max(dimensions.x, dimensions.y, dimensions.z)
        
        # Assuming a sensor width of 36mm (default in Blender) and frame aspect ratio to determine whether to use width or height
        sensor_width = camera.data.sensor_width
        aspect_ratio = bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y
        frame_dimension = sensor_width if aspect_ratio >= 1 else sensor_width / aspect_ratio
        
        # Calculate focal length to fit the object within 70% of the frame's largest dimension
        scale_factor = 0.7  # Target to occupy 70% of the frame
        focal_length = (distance * initial_focal_length) / (max_dimension / frame_dimension * scale_factor)
        camera.data.lens = focal_length

        camera.data.keyframe_insert(data_path="lens", frame=frame)

    print("Camera rig setup complete.")

# Example usage
setup_camera_rig("BezierCurve", "Cube", initial_focal_length=35)

