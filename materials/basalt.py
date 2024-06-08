import bpy

def create_basalt_material(name):
    # Create a new material
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    nodes.clear()

    # Create Principled BSDF shader node
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1)  # Dark gray, almost black
    bsdf.inputs['Roughness'].default_value = 0.9  # Basalt is quite rough
    bsdf.inputs['Specular'].default_value = 0.1  # Low specular for rocks

    # Create a Noise Texture for displacement
    noise_tex = nodes.new('ShaderNodeTexNoise')
    noise_tex.location = (-300, 100)
    noise.tex.inputs['Scale'].default_value = 16.0  # Texture scale
    noise.tex.inputs['Detail'].default_value = 2.0  # Texture detail
    noise.tex.inputs['Distortion'].default_value = 0.5  # Texture distortion

    # Create a Bump node to connect noise to BSDF
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-300, -100)
    bump.inputs['Strength'].default_value = 0.8  # The strength of the bumps

    # Link nodes
    links = mat.node_tree.links
    links.new(noise_tex.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Output node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

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

# Example usage
basalt_mat = create_basalt_material("BasaltRock")
assign_material_to_active_action(basalt_mat)