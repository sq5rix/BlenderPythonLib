import bpy
import random
from mathutils import Vector

# Function to create an icosphere
def create_icosphere(size):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=size, location=(0, 0, 0))
    icosphere = bpy.context.object
    icosphere.name = "EmittingIcosphere"
    return icosphere

# Function to create an emission material
def create_emission_material(intensity):
    mat = bpy.data.materials.new(name="EmissionMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    nodes.clear()

    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Strength'].default_value = intensity
    emission.inputs['Color'].default_value = (1, 1, 1, 1)  # White color

    output = nodes.new(type='ShaderNodeOutputMaterial')

    links.new(emission.outputs['Emission'], output.inputs['Surface'])

    return mat

# Function to generate a random direction vector
def generate_random_direction():
    direction = Vector((random.choice([1, -1]), random.choice([1, -1]), random.choice([1, -1])))
    return direction

# Main function to create the animation
def animate_icosphere_in_fog(steps, size, intensity):
    # Create the icosphere
    icosphere = create_icosphere(size)

    # Create the emission material and assign it to the icosphere
    emission_material = create_emission_material(intensity)
    if len(icosphere.data.materials):
        icosphere.data.materials[0] = emission_material
    else:
        icosphere.data.materials.append(emission_material)

    # Create the fog cube
    bpy.ops.mesh.primitive_cube_add(size=10, location=(0, 0, 0))
    fog_cube = bpy.context.object
    fog_cube.name = "FogCube"
    fog_cube.display_type = 'WIRE'
    fog_cube.hide_render = True  # Hide the cube in renders

    # Create a volume scatter material for the fog
    fog_material = bpy.data.materials.new(name="FogMaterial")
    fog_material.use_nodes = True
    nodes = fog_material.node_tree.nodes
    links = fog_material.node_tree.links

    nodes.clear()

    volume_scatter = nodes.new(type='ShaderNodeVolumeScatter')
    volume_scatter.inputs['Density'].default_value = 0.1
    volume_scatter.inputs['Color'].default_value = (0.8, 0.8, 0.8, 1)  # Light gray

    volume_output = nodes.new(type='ShaderNodeOutputMaterial')

    links.new(volume_scatter.outputs['Volume'], volume_output.inputs['Volume'])

    fog_cube.data.materials.append(fog_material)

    # Set initial position
    initial_position = Vector((-4.5, -4.5, -4.5))
    icosphere.location = initial_position
    icosphere.keyframe_insert(data_path="location", frame=0)

    # Animate the icosphere
    current_position = initial_position
    for step in range(1, steps + 1):
        direction = generate_random_direction()
        current_position += direction * size  # Move by the size of the icosphere
        icosphere.location = current_position
        icosphere.keyframe_insert(data_path="location", frame=step * 10)  # 10 frames per step

