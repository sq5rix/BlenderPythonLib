import bpy

def create_lizard_skin_material(name):
    # Create a new material
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    nodes.clear()

    # Create Principled BSDF shader node
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.2, 0.5, 0.1, 1)  # Greenish color
    bsdf.inputs['Roughness'].default_value = 0.5  # Semi-rough for a matte finish
    bsdf.inputs['Specular'].default_value = 0.5  # Moderate specular reflection

    # Create Voronoi texture for scales pattern
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-400, 0)
    voronoi.feature = 'DISTANCE_TO_EDGE'  # Use distance to edge for clear scale patterns
    voronoi.inputs['Scale'].default_value = 100.0  # Controls the density of the scales

    # Create a Bump node to give the scales texture
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.8  # Adjust strength for more pronounced scales

    # Connect Voronoi to Bump
    nodes.links.new(voronoi.outputs['Distance'], bump.inputs['Height'])

    # Connect Bump to BSDF Normal
    nodes.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

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
lizard_skin_mat = create_lizard_skin_material("LizardSkin")
assign_material_to_active_object(lizard_skin_mat)