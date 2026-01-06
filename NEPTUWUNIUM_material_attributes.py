import bpy
from io_scene_gltf2.io.com.gltf2_io import TextureInfo
from io_scene_gltf2.blender.imp.texture import texture
from io_scene_gltf2.blender.imp.material_utils import MaterialHelper


def NEPTUWUNIUM_material_attributes(material_attr, pymaterial, vertex_color, mat, gltf):
	workflow_name = material_attr.get('workflow', 'Basic Shader').strip()

	if len(workflow_name) == 0:
		workflow_name = 'Basic Shader'

	x = -200
	y = 0
	height = 460
	while mat.node_tree.nodes:
		mat.node_tree.nodes.remove(mat.node_tree.nodes[0])

	mh = MaterialHelper(gltf, pymaterial, mat, vertex_color)

	group_node = mh.nodes.new('ShaderNodeGroup')
	group_node.label = workflow_name

	out_node = mh.nodes.new('ShaderNodeOutputMaterial')
	group_node.location = 10, 300
	out_node.location = 300, 300
	if workflow_name in bpy.data.node_groups:
		group_node.node_tree = bpy.data.node_groups[workflow_name]
		mh.links.new(group_node.outputs[0], out_node.inputs[0])
	else:
		gltf.log.warning('unknown workflow "%s" on material "%s"' % (workflow_name, mat.name))

	texture_list = material_attr.get('textures', {})
	for texture_name in texture_list:
		alpha_node_name = texture_name + ' Alpha'
		texture(
			mh,
			tex_info=TextureInfo.from_dict(texture_list[texture_name]),
			label=texture_name,
			location=(x, y),
			is_data=True,
			color_socket=group_node.inputs[texture_name] if texture_name in group_node.inputs else None,
			alpha_socket=group_node.inputs[alpha_node_name] if alpha_node_name in group_node.inputs else None)
		y -= height

	height = 125
	scalar_list = material_attr.get('scalars', {})
	for scalar_name in scalar_list:
		value_node = mh.nodes.new('ShaderNodeValue')
		value_node.label = scalar_name
		value_node.location = x, y
		value_node.outputs[0].default_value = scalar_list[scalar_name]
		if scalar_name in group_node.inputs:
			mh.links.new(value_node.outputs[0], group_node.inputs[scalar_name])
		y -= height

	height = 275
	color_list = material_attr.get('colors', {})
	for color_name in color_list:
		value_node = mh.nodes.new('ShaderNodeRGB')
		value_node.label = color_name
		value_node.location = x, y
		value_node.outputs[0].default_value = color_list[color_name]
		if color_name in group_node.inputs:
			mh.links.new(value_node.outputs[0], group_node.inputs[color_name])
		y -= height
