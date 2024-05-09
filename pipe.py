# Creating an L-shaped pipe programmatically in Blender
# involves several steps, including mesh editing,
# vertex beveling, converting the mesh to a curve,
# and then adjusting the curve's properties to give it
# depth and resolution before finally converting it back
# to a mesh.
# The following function encapsulates this process:import bpy

def create_l_shaped_pipe(plane_size=2, bevel_segments=8, curve_depth=0.5, curve_resolution=4):
    """
    Creates an L-shaped pipe from a plane by deleting two adjacent edges, beveling a vertex,
    converting to a curve, and adding depth and resolution to the curve.

    Parameters:
    - plane_size: The size of the initial plane.
    - bevel_segments: Number of segments in the bevel.
    - curve_depth: The depth of the curve to represent the pipe's thickness.
    - curve_resolution: The resolution of the curve.
    """
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects

    # Add a plane and enter edit mode
    bpy.ops.mesh.primitive_plane_add(size=plane_size, location=(0, 0, 0))
    plane = bpy.context.object
    bpy.ops.object.mode_set(mode='EDIT')

    # Delete two adjacent edges to create an L shape
    bpy.ops.mesh.select_mode(type='EDGE')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete(type='EDGE')
    bpy.ops.mesh.select_all(action='SELECT')

    # Bevel the vertex
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.bevel(offset=plane_size / 2, segments=bevel_segments, vertex_only=True)

    # Return to object mode and convert to curve
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.convert(target='CURVE')

    # Set curve properties
    curve = bpy.context.object
    curve.data.dimensions = '3D'
    curve.data.fill_mode = 'FULL'
    curve.data.bevel_depth = curve_depth
    curve.data.bevel_resolution = curve_resolution
    curve.data.resolution_u = curve_resolution

    # Convert the curve to a mesh and rename to "Pipe"
    bpy.ops.object.convert(target='MESH')
    pipe = bpy.context.object
    pipe.name = "Pipe"

    return pipe

# Example usage
pipe = create_l_shaped_pipe(plane_size=2, bevel_segments=8, curve_depth=0.25, curve_resolution=4)

