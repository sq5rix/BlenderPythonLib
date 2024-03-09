# BPL - Blender Python Library Wrapper

Welcome to BPL, the Blender Python Library Wrapper, an open-source project designed to simplify the process of creating 3D objects, animations, procedural materials, and composition tools in Blender, the renowned open-source 3D creation suite. By abstracting the comprehensive bpy library, BPL offers an easy-to-use interface for both beginners and experienced Blender developers, streamlining the development of Blender scripts and add-ons.

## Features

- **Easy 3D Object Creation**: Simplified functions to create and manipulate 3D objects within Blender scenes.
- **Intuitive Animation Tools**: Streamlined methods for animating objects, making it easier to bring your scenes to life.
- **Procedural Material Generation**: High-level functions to create and apply procedural materials to objects, enhancing visual aesthetics with minimal effort.
- **Advanced Composition Capabilities**: Tools to facilitate complex composition tasks, improving the efficiency of scene setup and rendering.
- **User-Friendly API**: Designed with usability in mind, providing a clear and concise API that abstracts away the complexities of bpy.

## Getting Started

### Prerequisites

- Blender 4.0 or newer installed on your machine.

### Installation

1. Download the latest version of BPL from the [GitHub repository](https://github.com/sq5rix/BlenderPythonLibrary).
2. Open Blender
3. Copy the code in the Scripng scene
4. Run code - some functions will requre clicking active object 

pip install bpl is planned. 

### Configuration

After installation, BPL does not require additional configuration to start using its features.
You can add a useful function as a plugin to Blender in the usual way.

## Usage 

### Creating a 3D Object

```python
from bpl import ObjectCreator

# Create a new cube with default dimensions
cube = ObjectCreator.create_cube(name="MyCube")

# Move the cube to a specific location
cube.location = (1, 2, 3)
```

### Animating an Object

```python
from bpl import Animator

# Animate the cube's rotation over 60 frames
Animator.rotate_object(cube, rotation=(90, 0, 0), start_frame=1, end_frame=60)
```

### Generating a Procedural Material

```python
from bpl import MaterialGenerator

# Create a new procedural material and apply it to the cube
material = MaterialGenerator.create_procedural_material(name="MyMaterial", color=(0.8, 0.2, 0.2))
cube.materials.append(material)
```

### Complex Scene Composition

```python
from bpl import SceneComposer

# Automatically set up lighting and camera for a basic scene
SceneComposer.setup_basic_scene(objects=[cube])
```

## Documentation

For a comprehensive guide and API reference, please refer to the [BPL Documentation](https://github.com/sq5rix/BlenderPythonLibrary/wiki). The documentation is planned it will be continuously updated to reflect new features and improvements.

## Contributing

Contributions to BPL are warmly welcomed, whether it's in the form of bug reports, feature requests, or pull requests. Please see our [CONTRIBUTING.md](https://github.com/sq5rix/BlenderPythonLibrary/CONTRIBUTING.md) for more information on how to contribute.

## License

BPL is licensed under the MIT License. See the [LICENSE](https://github.com/your-repo/bpl/LICENSE) file for more details.

## Acknowledgments

- Special thanks to Ryan King for fantastic Blender tutorials on [YouTube](https://youtube.com/@RyanKingArt?si=wmYyGDFKGZ-_FPmM)
- Shoutout and thanks to Victor Stepano for opening up scripting in Blender [YouTube](https://youtube.com/@CGPython?si=Y_rGrNoMJbe141b1)
- The Blender Foundation, for developing and maintaining Blender.
- The Blender community, for their invaluable contributions and support.

We hope BPL will enhance your Blender scripting experience by providing an easier and more intuitive way to create, animate, and compose in Blender. For questions, feedback, or support, please reach out through our GitHub repository.

