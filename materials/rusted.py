import bpy

def create_rusted_metal_material(name):
    # Create a new material
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    nodes.clear()

    # Create Principled BSDF shader node for the base metal
    metal_shader = nodes.new('ShaderNodeBsdfPrincipled')
    metal_shader.location = (0, 0)
    metal_shader.inputs['Base Color'].default_value = (0.6, 0.5, 0.5, 1)  # Dark grey metallic
    metal_shader.inputs['Metallic'].default_value = 1.0  # Fully metallic
    metal_shader.inputs['Roughness'].default_value = 0.5  # Slightly rough

    # Create Principled BSDF shader for rust
    rust_shader = nodes.new('ShaderNodeBsdfPrincipled')
    rust_shader.location = (0, -200)
    rust_shader.inputs['Base Color'].default_value = (0.8, 0.2, 0.1, 1)  # Rust color
    rust_shader.inputs['Roughness'].default_value = 1.0  # Very rough
    rust_shader.inputs['Metallic'].default_value = 0.0  # Non-metallic

    # Geometry node to detect edges
    geometry = nodes.new('ShaderNodeNewGeometry')
    geometry.location = (-400, 100)

    # Pointiness to control rust effect
    pointiness = nodes.new('ShaderNodeValToRGB')
    pointiness.location = (-200, 100)
    pointiness.color_ramp.elements[0].position = 0.4  # Adjust these to control the edge detection sensitivity
    pointiness.color_ramp.elements[1].position = 0.6
    nodes.links.new(geometry.outputs['Pointiness'], pointiness.inputs['Fac'])

    # Mix shader to combine metal and rust based on edges
    mix_shader = nodes.new('ShaderNodeMixShader')
    mix_shader.location = (200, 0)
    nodes.links.new(pointiness.outputs['Color'], mix_fr.input[0])
    nodes.links.new(metal_shader.outputs['BSDF'], mix_shader.inputs[1])
    nodes.links.new(rust_shader.outputs['BSDF'], mix_shader.inputs[2])

    # Output node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    nodes.links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

    return mat

def assign_material_to_active_object(material):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

# Example usage
rusted_metal_mat = create_rusted_metal_material("RustedMetal")
assign_material_to_active_object(rusted_metal_mat)