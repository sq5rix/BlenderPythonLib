import bpy

def create_brushed_metal_material(name, base_color=(0.8, 0.8, 0.8, 1), roughness=0.2, anisotropic=0.8, rotation=0.5):
    # Create a new material
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    nodes.clear()

    # Create Principled BSDF shader node
    shader = nodes.new('ShaderNodeBsdfPrincipled')
    shader.location = (0, 0)
    
    # Set properties for brushed metal
    shader.inputs['Base Color'].default_value = base_color
    shader.inputs['Metallic'].default_value = 1.0  # Fully metallic
    shader.inputs['Roughness'].default_value = roughness
    shader.inputs['Anisotropic'].default_value = anisotropic
    shader.inputs['Anisotropic Rotation'].default_value = rotation

    # Create a Texture Coordinate node
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-400, 0)

    # Create a Noise Texture node to vary the anisotropic rotation
    noise_tex = nodes.new('ShaderNodeTexNoise')
    noise_tex.location = (-200, 0)
    noise_tex.inputs['Scale'].default_value = 100  # Texture scale
    noise_tex.inputs['Detail'].default_value = 2  # Texture detail
    noise_tex.inputs['Distortion'].default_value = 0.1  # Texture distortion

    # Link nodes
    links = mat.node_tree.links
    links.new(tex_coord.outputs['Object'], noise_tex.inputs['Vector'])
    links.new(noise_tex.outputs['Fac'], shader.inputs['Anisotropic Rotation'])

    # Output node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)
    links.new(shader.outputs['BSDF'], output.inputs['Surface'])

    return mat

def assign_material_to_active_object(material):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

# Example usage
brushed_metal_mat = create_brushed_metal_material("BrushedMetal", base_color=(0.8, 0.8, 0.8, 1), roughness=0.2, anisotropic=0.8, rotation=0.5)
assign_material_to_active_object(brushed_metal_mat)