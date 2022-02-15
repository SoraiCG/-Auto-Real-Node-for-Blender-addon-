bl_info = {
    "name": "Auto Real Node",
    "author": "Sorai",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar",
    "description": "Nodes are automatically assembled to provide a simple and realistic representation",
    "warning": "",
    "doc_url": "",
    "category": "Node",
}

import bpy


class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Auto Real Node"
    bl_idname = "RealSTART"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Auto Real Node"

    def draw(self, context):
      self.layout.row().operator("object.simple_operator", icon= 'FUND')


class SimpleOperator(bpy.types.Operator):
    
    bl_idname = "object.simple_operator"
    bl_label = "Connect automatically"
    
    
    def execute(self, context):
                #新しいマテリアルをつくる
        material_real = bpy.data.materials.new('RealMaterial')
        #ノードを使えるようにする
        material_real.use_nodes = True

        #ノードの値を設定していく
        #変数p_BSDFをつくって書く量を減らす
        p_BSDF = material_real.node_tree.nodes["Principled BSDF"]


        image = material_real.node_tree.nodes.new('ShaderNodeTexImage')
        image.location = (-900,200)

        Mapping = material_real.node_tree.nodes.new('ShaderNodeMapping')
        Mapping.location = (-1100,200)

        tex = material_real.node_tree.nodes.new('ShaderNodeTexCoord')
        tex.location = (-1300,200)

        Color1 = material_real.node_tree.nodes.new('ShaderNodeValToRGB')
        Color1.location = (-300,100)

        Color2 = material_real.node_tree.nodes.new('ShaderNodeValToRGB')
        Color2.location = (-500,-300)


        Bump = material_real.node_tree.nodes.new('ShaderNodeBump')
        Bump.location = (-200,-200)
        
        Bump.inputs[0].default_value = 0.15

        Color1.color_ramp.elements[0].position = 0.7
        Color1.color_ramp.elements[1].position = 0.12

        Color2.color_ramp.elements[0].position = 0.44
        Color2.color_ramp.elements[1].position = 0.2
        
        

        #挿していく
        material_real.node_tree.links.new(image.outputs[0],p_BSDF.inputs[0])
        material_real.node_tree.links.new(Mapping.outputs[0],image.inputs[0])
        material_real.node_tree.links.new(tex.outputs[2],Mapping.inputs[0])
        material_real.node_tree.links.new(Color1.outputs[0],p_BSDF.inputs[9])
        material_real.node_tree.links.new(image.outputs[0],Color1.inputs[0])
        material_real.node_tree.links.new(Bump.outputs[0],p_BSDF.inputs[22])
        material_real.node_tree.links.new(Color2.outputs[0],Bump.inputs[2])
        material_real.node_tree.links.new(image.outputs[0],Color2.inputs[0])


        bpy.context.object.data.materials.append(material_real)
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(HelloWorldPanel)
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

