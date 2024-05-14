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



