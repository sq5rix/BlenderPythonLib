import bpy

def create_birch_bark_material(name):
    # Create a new material
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    nodes.clear()

    # Create Principled BSDF shader node
    shader = nodes.new('ShaderNodeBsdfPrincipled')
    shader.location = (0, 0)

    # Set base color and roughness
    shader.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1)  # Light grayish color of birch
    shader.inputs['Roughness'].default_value = 0.5  # Moderately rough

    # Create Musgrave texture for general bark texture
    musgrave = nodes.new('ShaderNodeTexMusgrave')
    musgrave.location = (-300, 100)
    musgrave.inputs['Scale'].default_value = 150.0
    musgrave.inputs['Detail'].default_value = 16.0
    musgrave.inputs['Dimension'].default_value = 0.0
    musgrave.inputs['Lacunarity'].default_value = 1.0

    # Create Wave texture for stripes
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-300, -100)
    wave.inputs['Scale'].default_value = 60.0
    wave.inputs['Distortion'].default_value = 5.0

    # Create Color Ramp to control the wave bands
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-100, -100)
    color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)  # Black
    color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)  # White

    # Link nodes
    links = mat.node_tree.links
    links.new(wave.outputs['Color'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], shader.inputs['Base Color'])
    links.new(musgrave.outputs['Fac'], shader.inputs['Roughness'])

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

# Create and assign the material
birch_bark_mat = create_birch_bark_material("BirchBarkMaterial")
assign_material_to_active_object(birch_bark_mat)