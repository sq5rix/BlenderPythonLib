import bpy
from mathutils import Vector

def update_camera_focal_length(camera, target_object, scale_factor=0.7):
    """
    Updates the camera's focal length based on the target object's size and distance,
    aiming to keep the target object's largest dimension within a specified percentage
    of the frame's width or height.

    Args:
    - camera: The camera object to update.
    - target_object: The target object the camera focuses on.
    - scale_factor (float): Determines how much of the frame's width or height
      the target object should occupy. Defaults to 0.7 (70%).
    """
    camera_loc = camera.matrix_world.translation
    target_loc = target_object.matrix_world.translation
    distance = (target_loc - camera_loc).length

    # Calculate dimensions of the target object
    dimensions = target_object.dimensions
    max_dimension = max(dimensions.x, dimensions.y, dimensions.z)

    # Assuming a sensor width of 36mm (default in Blender) and frame aspect ratio
    sensor_width = camera.data.sensor_width
    aspect_ratio = bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y
    frame_dimension = sensor_width if aspect_ratio >= 1 else sensor_width / aspect_ratio

    # Calculate focal length to fit the object within the specified scale factor of the frame
    focal_length = (distance * camera.data.lens) / (max_dimension / frame_dimension * scale_factor)
    camera.data.lens = focal_length

def setup_camera_rig(curve_name, target_object_name, initial_focal_length=50):
    """
    Sets up a camera rig that moves along a Bézier curve focusing on a specified object,
    adjusting the camera's focal length dynamically.

    Args:
    - curve_name (str): The name of the Bézier curve object.
    - target_object_name (str): The name of the object to focus on.
    - initial_focal_length (float): The initial focal length of the camera.
    """
    curve = bpy.data.objects.get(curve_name)
    target_object = bpy.data.objects.get(target_object_name)
    if not curve or not target_object:
        print("Curve or target object does not exist.")
        return

    camera = bpy.data.objects.get("CameraRig") or bpy.ops.object.camera_add().name
    camera.data.sensor_fit = 'HORIZONTAL'
    camera.data.lens = initial_focal_length

    follow_path_constraint = camera.constraints.new(type='FOLLOW_PATH')
    follow_path_constraint.target = curve
    follow_path_constraint.use_curve_follow = True

    track_to_constraint = camera.constraints.new(type='TRACK_TO')
    track_to_constraint.target = target_object
    track_to_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    track_to_constraint.up_axis = 'UP_Y'

    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end

    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        update_camera_focal_length(camera, target_object)
        camera.data.keyframe_insert(data_path="lens", frame=frame)

    print("Camera rig setup complete.")

# Example usage
setup_camera_rig("BezierCurve", "Cube", initial_focal_length=35)
