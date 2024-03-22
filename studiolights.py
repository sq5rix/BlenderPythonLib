def add_front_spotlight(object_size, collection_name="StudioLights"):
    """Adds a front spotlight to light the main object."""
    # Calculate the spotlight's location based on the main object's size
    location = (0, -object_size * 2, object_size / 2)  # Adjust multiplier for desired distance

    # Create the spotlight
    bpy.ops.object.light_add(type='SPOT', location=location)
    light = bpy.context.object
    light.name = "Front Spotlight"
    light.data.energy = 500  # Adjust energy as needed
    light.data.color = (1, 1, 1)  # White, adjust color as needed
    light.data.spot_size = 1.0  # Adjust spot size (radians) as needed
    light.data.spot_blend = 0.1  # Adjust spot blend (softness) as needed
    light.data.show_cone = True  # Optionally show the light's cone in the viewport

    # Point the light towards the main object (0,0,0)
    light.rotation_euler[0] = 1.5708  # 90 degrees in radians

    # Ensure the light is added to the specified collection
    collection = ensure_collection(collection_name)
    for col in light.users_collection:
        col.objects.unlink(light)
    collection.objects.link(light)