# Libraries
import bpy
from mathutils import Vector

def create_collection(name):
    new_collection = bpy.data.collections.new(name)
    return bpy.context.scene.collection.children.link(new_collection)

def select_collection(number):
    view = bpy.context.view_layer
    view.active_layer_collection = view.layer_collection.children[number]
    
def new_GeometryNodes_group():
    node_group = bpy.data.node_groups.new('GeometryNodes', 'GeometryNodeTree')
    inNode = node_group.nodes.new('NodeGroupInput')
    inNode.outputs.new('NodeSocketGeometry', 'Geometry')
    outNode = node_group.nodes.new('NodeGroupOutput')
    outNode.inputs.new('NodeSocketGeometry', 'Geometry')
    node_group.links.new(inNode.outputs['Geometry'], outNode.inputs['Geometry'])
    inNode.location = Vector((-400, -300))
    outNode.location = Vector((1.5 * outNode.width, 0))
    return node_group

def create_environment():
    # Clear environment
    for coll in bpy.data.collections:
        bpy.data.collections.remove(coll)
        
    # Create the Collections
    create_collection("DISTRIBUTOR")
    create_collection("CONTENTS")
    
    # Select "CONTENTS" Collection
    select_collection(1)
    
    # Add Objects to the selected Colletion
    add_object = bpy.ops.mesh
    add_object.primitive_cube_add()
    add_object.primitive_uv_sphere_add()
    add_object.primitive_cone_add()
    add_object.primitive_cylinder_add()
    
    # Exclude "CONTENTS" Collection
    lc = bpy.context.view_layer.active_layer_collection
    lc.exclude = True
    
    # Select "DISTRIBUTOR" Collection
    select_collection(0)
    
def geometry_nodes():
    # Create Prmitive Object
    bpy.ops.curve.primitive_bezier_curve_add()
    curve = bpy.context.active_object
    
    # Add Modifier "Geometry Nodes"
    bpy.ops.object.modifier_add(type='NODES')
    
    # Create Geometry Nodes Group
    new_GeometryNodes_group()
    if curve.modifiers[-1].node_group:
        node_group = curve.modifiers[-1].node_group
    else:
        node_group = new_GeometryNodes_group()
        curve.modifiers[-1].node_group = node_group
    nodes = node_group.nodes
    
    group_in = nodes.get('Group Input')
    group_out = nodes.get('Group Output')
    
    # Add New Nodes
    mesh_line_node = nodes.new('GeometryNodeMeshLine')
    mesh_line_node.location = Vector((-200, 0))
    inst_on_p_node = nodes.new('GeometryNodeInstanceOnPoints')
    inst_on_p_node.location = Vector((0, -100))
    col_info_node = nodes.new('GeometryNodeCollectionInfo')
    col_info_node.location = Vector((-200, -300))
    rand_val_node = nodes.new('FunctionNodeRandomValue')
    rand_val_node.location = Vector((-200, -500))
    
    # Set Default Nodes values
    mesh_line_node.inputs[0].default_value = 8
    mesh_line_node.inputs[3].default_value = (3,0,0)
    col_info_node.inputs[1].default_value = True
    col_info_node.inputs[2].default_value = True
    inst_on_p_node.inputs[3].default_value = True
    rand_val_node.data_type = 'INT' 
    
    # Create New Nodes Links
    links = node_group.links.new
    links(mesh_line_node.outputs[0], inst_on_p_node.inputs[0])
    links(col_info_node.outputs[0], inst_on_p_node.inputs[2])
    links(inst_on_p_node.outputs[0], group_out.inputs[0])
    links(rand_val_node.outputs[2], inst_on_p_node.inputs[4])
    
    # Add New Group Input Sockets
    group_in_inputs = bpy.data.node_groups[-1].inputs
    group_in_inputs.new('NodeSocketCollection', 'Collection')
    group_in_inputs.new('NodeSocketInt', 'Min')
    group_in_inputs.new('NodeSocketInt', 'Max')
    group_in_inputs.new('NodeSocketInt', 'Count')
    
    # Set Socket Boarder Values
    group_in_inputs['Min'].min_value = 1
    group_in_inputs['Min'].max_value = 3
    group_in_inputs['Max'].min_value = 4
    group_in_inputs['Max'].max_value = 6
    group_in_inputs['Count'].min_value = 0
    
    # Create Group Input Links
    links(group_in.outputs[1], col_info_node.inputs[0])
    links(group_in.outputs[2], rand_val_node.inputs[4])
    links(group_in.outputs[3], rand_val_node.inputs[5])
    links(group_in.outputs[4], mesh_line_node.inputs[0])
    
    # Set Default Group Input Values
    input_data = bpy.context.object.modifiers['GeometryNodes']
    input_data['Input_2'] = bpy.data.collections['CONTENTS']
    input_data['Input_3'] = 1
    input_data['Input_4'] = 4
    input_data['Input_5'] = 4
    
def main():
    create_environment()
    geometry_nodes()


if __name__ == "__main__":
    main()