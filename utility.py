import bpy

def find_curve_and_target():
    """
    Identifies the selected curve and target object from the Blender scene.

    Returns:
    - curve_name (str): The name of the selected curve.
    - target_object_name (str): The name of the selected target object.

    If the correct selection is not made, returns None for both.
    """
    selected_objects = bpy.context.selected_objects
    if len(selected_objects) != 2:
        print("Please select exactly two objects: one curve and one target object.")
        return None, None

    # Determine which object is the curve and which is the target
    curve = next((obj for obj in selected_objects if obj.type == 'CURVE'), None)
    target_object = next((obj for obj in selected_objects if obj.type != 'CURVE'), None)

    if not curve or not target_object:
        print("Selection does not include a curve and another object.")
        return None, None

    return curve.name, target_object.name

# Example usage
curve_name, target_object_name = find_curve_and_target()
if curve_name and target_object_name:
    print(f"Curve: {curve_name}, Target Object: {target_object_name}")
    # You can now use curve_name and target_object_name with the setup_camera_rig function
