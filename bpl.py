import bpy
import random
from mathutils import Vector, Euler
import bpy

def clear_scene():
    """
    Removes all objects from the current Blender scene.
    """
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def look_at(obj, target_point):
    """
    Rotates an object to look at a target point in 3D space.

    Args:
    - obj: The object to orient.
    - target_point: The location (Vector) to look at.
    """
    # Direction from the object to the target point
    direction = target_point - obj.location
    # Point the object's '-Z' and 'Y' towards the target
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def add_camera(x, y, z):
    """
    Adds a Camera to the scene at the specified location and makes it face towards the origin (0, 0, 0).

    Args:
    - x, y, z: The coordinates where the Camera will be placed.
    """
    # Create the Camera
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object  # Get the newly created Camera

    # Use the look_at function to orient the camera
    look_at(camera, Vector((0, 0, 0)))


def add_sun(x, y, z, strength=1.0):
    """
    Adds a Sun lamp to the scene at the specified location, makes it face towards the origin (0, 0, 0),
    and sets its light strength.

    Args:
    - x, y, z: The coordinates where the Sun lamp will be placed.
    - strength: The light strength of the Sun lamp.
    """
    # Create the Sun lamp
    bpy.ops.object.light_add(type='SUN', location=(x, y, z))
    sun = bpy.context.object  # Get the newly created Sun lamp

    # Calculate the direction vector from the Sun to the origin
    direction = Vector((0, 0, 0)) - sun.location
    # Point the Sun towards the origin
    sun.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()

    # Set the light strength
    sun.data.energy = strength


def create_bsdf_emission_material(name="BSDF_Emission_Material", color=(1.0, 1.0, 1.0, 1.0), metallic=0.0, roughness=0.5, emission_strength=1.0, default_fac=0.0):
    """
    Creates a new material with a Principled BSDF and Emission shader mixed together.

    Args:
    - name: The name of the new material.
    - color: The base color of the Principled BSDF shader.
    - metallic: The metallic property of the Principled BSDF shader.
    - roughness: The roughness property of the Principled BSDF shader.
    - emission_strength: The strength of the Emission shader.
    - default_fac: The default factor for the Mix Shader node.

    Returns:
    - The newly created material object.
    """
    # Create a new material
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Create Principled BSDF shader node
    principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_bsdf.location = (-200, 100)
    principled_bsdf.inputs['Base Color'].default_value = color
    principled_bsdf.inputs['Metallic'].default_value = metallic
    principled_bsdf.inputs['Roughness'].default_value = roughness

    # Create Emission shader node
    emission = nodes.new(type='ShaderNodeEmission')
    emission.location = (-200, -100)
    emission.inputs['Strength'].default_value = emission_strength

    # Create Mix Shader node
    mix_shader = nodes.new(type='ShaderNodeMixShader')
    mix_shader.location = (0, 0)
    mix_shader.inputs['Fac'].default_value = default_fac

    # Create Material Output node
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = (200, 0)

    # Link nodes
    links.new(principled_bsdf.outputs['BSDF'], mix_shader.inputs[1])
    links.new(emission.outputs['Emission'], mix_shader.inputs[2])
    links.new(mix_shader.outputs['Shader'], material_output.inputs['Surface'])

    return material


def set_mix_shader_fac(material, fac_value):
    """
    Sets the Fac value of the Mix Shader node in the given material.

    Args:
    - material: The material object to modify.
    - fac_value: The float value to set for the Mix Shader's Fac factor.
    """
    if material.use_nodes:
        # Try to find the Mix Shader node in the material's node tree
        mix_shader = next(
            (node for node in material.node_tree.nodes if node.type == 'MIX_SHADER'), None
        )

        if mix_shader:
            # Set the Fac value
            mix_shader.inputs['Fac'].default_value = fac_value


def create_sphere_with_material(material, radius=1.0, location=(0, 0, 0), subdivisions=2, name="SphereWithMaterial"):
    """
    Creates a sphere and applies the given material to it.

    Args:
    - material: The material to apply to the sphere.
    - radius: The radius of the sphere.
    - location: The location to place the sphere at.
    - subdivisions: The number of subdivisions for the Icosphere.
    - name: The name of the new sphere object.

    Returns:
    - The newly created sphere object.
    """
    # Create an Icosphere
    bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, subdivisions=subdivisions, location=location)

    # Get the newly created Icosphere
    sphere = bpy.context.object
    sphere.name = name

    # Ensure the sphere has a material slot and apply the material
    if len(sphere.data.materials) == 0:
        sphere.data.materials.append(material)
    else:
        sphere.data.materials[0] = material

    return sphere


def create_icosphere_grid(n, r, d, subs, name):
    """
    Creates an n x n x n grid of Icospheres with increased subdivisions and applies an existing material named 'SimpleStar' to them.

    Args:
    - n: The number of Icospheres along each axis.
    - r: Radius of each Icosphere.
    - d: Distance between the centers of adjacent Icospheres.
    - subdivisions: The subdivision level for each Icosphere.
    """
    spheres = []
    materials = []

    # Calculate the start position so that the grid is centered at the origin
    start_pos = -(n - 1) * d / 2

    # Loop over each dimension
    for i in range(n):
        for j in range(n):
            for k in range(n):
                # Calculate the position for the current Icosphere
                x = start_pos + i * d
                y = start_pos + j * d
                z = start_pos + k * d

                # Example usage:
                new_material = create_bsdf_emission_material(
                    name="CustomMaterial",
                    color=(0.9, 0.1, 0.1, 1.0),  # Reddish color
                    metallic=0.3,
                    roughness=0.15,
                    emission_strength=9.9,
                    default_fac=0.0
                )

                # Create an sphere at the calculated position
                ico_sphere = create_sphere_with_material(
                    new_material, radius=r,
                    location=(x, y, z), subdivisions=subs,
                    name=name+str(x)+str(y)+str(z)
                )
                spheres.append(ico_sphere)
                materials.append(new_material)
    return spheres, materials


def create_list_activated_points(original_list, step):
    """
    Processes a list of objects based on specified rules and returns a modified copy.

    Args:
    - original_list: The list of objects to process.
    - step: The base step value used to determine the skip count.

    Returns:
    - A modified copy of the original list based on the processing rules.
    """
    if not original_list:
        return []

    # Initialize the resulting list with the first object
    result_list = [original_list[0]]
    i = 0  # Start with the first object

    while i < len(original_list) - 1:
        rand_choice = random.randint(0, 2)  # Get a random number (0, 1, or 2)

        if rand_choice == 0:
            # Copy the next object
            i += 1
        elif rand_choice == 1:
            # Skip step-1 objects
            i += step
        elif rand_choice == 2:
            # Skip step^2-1 objects
            i += step**2

        # Check if the index is within the bounds of the list
        if i < len(original_list):
            result_list.append(original_list[i])
        else:
            # If the index goes beyond the list, stop the loop
            break

    return result_list

def animate_fac_for_materials(materials, start_frame, step):
    """
    Animate the 'Fac' property of the Mix Shader node in each material. Sets 'Fac' to 0.0 at frame 0,
    then to 1.0 for each material starting from 'start_frame', incrementing by 'step'. The interpolation
    type for these keyframes is set to 'CONSTANT' for a step-like transition.

    Args:
    - materials: A list of Blender material objects.
    - start_frame: The starting frame for the animation.
    - step: The step between keyframes for successive materials.
    """
    bpy.context.scene.frame_set(0)  # Start at frame 0

    for index, material in enumerate(materials):
        if not material.use_nodes:
            print(f"Material '{material.name}' does not use nodes.")
            continue

        mix_shader = next((node for node in material.node_tree.nodes if node.type == 'MIX_SHADER'), None)
        if not mix_shader:
            print(f"No Mix Shader found in material '{material.name}'.")
            continue

        # Set 'Fac' to 0.0 at frame 0 for all materials
        mix_shader.inputs['Fac'].default_value = 0.0
        mix_shader.inputs['Fac'].keyframe_insert(data_path="default_value", frame=0)

        # Find the F-Curve for the 'Fac' property and set interpolation to 'CONSTANT'
        fcurve = material.node_tree.animation_data.action.fcurves.find('nodes["' + mix_shader.name + '"].inputs[0].default_value')
        if fcurve:  # Check if the F-Curve exists
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'CONSTANT'

        # Set 'Fac' to 1.0 at the specified frame for each material
        frame = start_frame + (index * step)
        bpy.context.scene.frame_set(frame)  # Go to the specified frame
        mix_shader.inputs['Fac'].default_value = 1.0
        mix_shader.inputs['Fac'].keyframe_insert(data_path="default_value", frame=frame)

        # Again, set interpolation to 'CONSTANT' for the new keyframe
        if fcurve:  # Ensure the F-Curve still exists
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'CONSTANT'

n = 5  # Grid size
r = 0.8  # Icosphere radius
d = 3  # Distance between the centers of adjacent Icospheres
start_frame=2
subdivisions = 4  # Subdivision level to increase mesh density

# Call the function to create the grid
clear_scene()
add_camera(25, -35, 20)
add_sun(60, 60, 60, 10)
add_sun(-30, -80, -30, 10)
add_sun(30, -80, 30, 10)
_, mats = create_icosphere_grid(n, r, d, subdivisions,"SimpleStar")
modified_materials = create_list_activated_points(mats, n)
animate_fac_for_materials(modified_materials , start_frame=start_frame, step=1)

