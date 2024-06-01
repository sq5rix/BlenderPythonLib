import bpy

def create_glass_material(name, ior, roughness):
    # Create a new material
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    nodes.clear()

    # Create a Principled BSDF shader node
    shader = nodes.new('ShaderNodeBsdfPrincipled')
    shader.location = (0, 0)

    # Set the shader properties for glass
    shader.inputs['Transmission'].default_value = 1.0  # Enable full transmission
    shader.inputs['Roughness'].default_vsalue = roughness  # Control the roughness of the glass
    shader.inputs['IOR'].default_value = ior  # Index of Refraction

    # Create an Output material node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)

    # Link Principled BSDF to Output
    links = mat.node_tree.links
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

# Example usage
glass_mat = create_glass_material("CustomGlass", ior=1.45, roughness=0.0)
assign_material_to_active_object(glass_mat)