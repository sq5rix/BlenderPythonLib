import bpy
from mathutils import Vector

def create_scene_bounding_cube():
    """
    Initial min and max vectors
    """
    min_coord = Vector((float('inf'), float('inf'), float('inf')))
    max_coord = Vector((float('-inf'), float('-inf'), float('-inf')))

    # Calculate the bounding box of all objects in the scene
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            for vertex in obj.bound_box:
                world_vertex = obj.matrix_world @ Vector(vertex)
                min_coord = Vector(map(min, zip(min_coord, world_vertex)))
                max_coord = Vector(map(max, zip(max_coord, world_vertex)))

    # Calculate center and dimensions
    center = (min_coord + max_coord) / 2
    dimensions = max_coord - min_coord

    # Scale dimensions by 1.5
    dimensions *= 1.5

    # Create a cube
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    cube = bpy.context.object
    cube.name = "SceneBoundingCube"

    # Scale the cube to the calculated dimensions
    cube.scale = dimensions / 2  # Cube size is in diameters, but we calculate in radius

    # Hide cube faces in the viewport
    for polygon in cube.data.polygons:
        polygon.hide = True

    return cube

def main():
    cube = create_scene_bounding_cube()

if __name__ == "__main__":
    main()

