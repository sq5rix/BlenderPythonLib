import bpy

def create_aluminum_material(name):
    # Create a new material
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node-tree.nodes

    # Clear default nodes
    nodes.clear()

    # Create Principled BSDF shader node
    shader = nodes.new('ShaderNodeBsdfPrincipled')
    shader.location = (0, 0)
    
    # Configure the shader for aluminum
    shader.inputs['Metallic'].default_value = 1.0  # Full metallic
    shader.inputs['Roughness'].default_value = 0.4  # Slightly rough
    shader.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1)  # Light gray color of aluminum

    # Add a noise texture for scratches
    noise_tex = nodes.new('ShaderNodeTexNoise')
    noise_tex.location = (-400, 0)
    noise_tex.inputs['Scale'].default_value = 25.0  # Scale of the noise
    noise_tex.inputs['Detail'].default_value = 16.0  # Detail of the noise
    noise_tex.inputs['Distortion'].default_value = 0.5  # Distortion of the noise texture

    # Add a bump node to apply the scratches
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, 0)
    bump.inputs['Strength'].default_value = 0.1  # Strength of the bump effect
    bump.inputs['Distance'].default_value = 0.1  # Distance for bump effect (affects the height of the scratches)

    # Link nodes
    links = mat.node_tree.links
    links.new(noise_tex.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], shader.inputs['Normal'])

    # Output node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)
    links.new(shader.outputs['BSDF'], output.inputs['Surface'])

    return mat

def assign_material_to_active_object(material):
    obj = bpy.context.active_object
    # Ensure the object has a mesh to assign material to
    if obj.type == 'MESH':
        # Assign it to the object's active material slot or add a new slot
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

# Create and assign the material
aluminum_mat = create_aluminum_material("AluminumScratched")
assign_material_to_active_object(aluminum_mat)