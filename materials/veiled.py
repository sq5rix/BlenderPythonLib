import bpy

def create_porcelain_material(name, texture_path=None):
    # Create a new material
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    nodes.clear()

    # Create Principled BSDF shader node
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 1, 1)  # Slightly bluish white
    bsdf.inputs['Subsurface'].default_value = 0.5  # Some subsurface scattering
    bsdf.inputs['Subsurface Radius'].default_value = (1, 1, 1)
    bsdf.inputs['Subsurface Color'].default_value = (0.95, 0.95, 1, 1)
    bsdf.inputs['Roughness'].default_value = 0.1  # Porcelain is quite smooth
    bsdf.inputs['Sheen'].default_value = 0.3  # Gives a soft sheen typical for porcelain

    # Check if a texture path is provided for blue patterns
    if texture_path:
        # Image texture node for blue patterns
        texture = nodes.new('ShaderNodeTexImage')
        texture.location = (-300, 0)
        texture.image = bpy.data.images.load(texturepath)
        
        # Mix the texture with the base color
        mix = nodes.new('ShaderNodeMixRGB')
        mix.location = (-150, 0)
        mix.inputs['Color1'].default_value = (0.95, 0.95, 1, 1)  # Base color
        mix.inputs['Fac'].default_value = 0.2  # Mix factor
        nodes.links.new(texture.outputs['Color'], mix.inputs['Color2'])
        nodes.links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])

    # Output node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)
    nodes.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

def assign_material_to_active_object(material):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

# Example usage
porcelain_mat = create_porcelain_material("BlueWhitePorcelain", texture_path="path/to/your/texture.jpg")
assign_material_to_active_object(porcelain_mat)