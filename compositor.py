import bpy

class COMPOSITOR_OT_setup_basic_nodes(bpy.types.Operator):
    """Set up basic compositing nodes"""
    bl_idname = "compositor.setup_basic_nodes"
    bl_label = "Setup Basic Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Enable use_nodes on the scene
        context.scene.use_nodes = True
        tree = context.scene.node_tree
        
        # Clear existing nodes
        for node in tree.nodes:
            tree.nodes.remove(node)

        # Create nodes
        nodes = tree.nodes
        links = tree.links
        
        # Adding denoise node
        denoise_node = nodes.new(type='CompositorNodeDenoise')
        denoise_node.location = (0, 300)
        
        # Adding glare node
        glare_node = nodes.new(type='CompositorNodeGlare')
        glare_node.location = (200, 300)
        
        # Adding color balance for color temperature adjustment
        color_temp_node = nodes.new(type='CompositorNodeColorBalance')
        color_temp_node.location = (400, 300)
        color_temp_node.correction_method = 'LIFT_GAMMA_GAIN'
        
        # Adding RGB curves node
        rgb_curves_node = nodes.new(type='CompositorNodeRGBCurves')
        rgb_curves_node.location = (600, 300)
        
        # Adding lens distortion node
        lens_dist_node = nodes.new(type='CompositorNodeLensDist')
        lens_dist_node.location = (800, 300)
        lens_dist_node.inputs['Distort'].default_value = 0.01  # Minimal distortion

        # Connect nodes
        links.new(denoise_node.outputs['Image'], glare_node.inputs['Image'])
        links.new(glare_node.outputs['Image'], color_temp_node.inputs['Image'])
        links.new(color_temp_node.outputs['Image'], rgb_curves_node.inputs['Image'])
        links.new(rgb_curves_node.outputs['Image'], lens_dist_node.inputs['Image'])
        
        # Add a composite node to connect the final output
        composite_node = nodes.new(type='CompositorNodeComposite')
        composite_node.location = (1000, 300)
        links.new(lens_dist_node.outputs['Image'], composite_node.inputs['Image'])

        # Render layer node
        render_layers = nodes.new('CompositorNodeRLayers')
        render_layers.location = (-200, 300)
        links.new(render_layers.outputs['Image'], denoise_node.inputs['Image'])
        
        return {'FINISHED'}

class COMPOSITOR_PT_custom_panel(bpy.types.Panel):
    """Creates a Panel in the Compositor context"""
    bl_label = "Basic Compositor Setup"
    bl_idname = "COMPOSITOR_PT_custom_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_context = "compositing"

    def draw(self, context):
        layout = self.layout
        layout.operator(COMPOSITOR_OT_setup_basic_nodes.bl_idname)

def register():
    bpy.utils.register_class(COMPOSITOR_OT_setup_basic_nodes)
    bpy.utils.register_class(COMPOSITOR_PT_custom_panel)

def unregister():
    bpy.utils.unregister_class(COMPOSITOR_OT_setup_basic_nodes)
    bpy.utils.unregister_class(COMPOSITOR_PT_custom_panel)

if __name__ == "__main__":
    register()