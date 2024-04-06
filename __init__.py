import bpy
from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
from io_scene_gltf2.io.com.gltf2_io import TextureInfo
from io_scene_gltf2.blender.imp.gltf2_blender_texture import texture
from io_scene_gltf2.blender.imp.gltf2_blender_material_utils import MaterialHelper


bl_info = {
	"name": "glTF Chronovore Importer Extension",
	"category": "Generic",
	"version": (1, 0, 0),
	"blender": (4, 1, 0),
	'location': 'File > Import > glTF 2.0',
	'description': '',
	'tracker_url': "https://github.com/yretenai/glTF-Chronovore-EXT/issues/",
	'isDraft': False,
	'developer': "chronovore",
	'url': 'https://github.com/yretenai/glTF-Chronovore-EXT',
}


glTF_extension_name = "CHRONOVORE_material_attributes"


class ChronovoreImporterExtensionProperties(bpy.types.PropertyGroup):
	enabled: bpy.props.BoolProperty(
		name=bl_info["name"],
		description='Run this extension while importing glTF file.',
		default=True)


class GLTF_PT_UserExtensionPanel(bpy.types.Panel):

	bl_space_type = 'FILE_BROWSER'
	bl_region_type = 'TOOL_PROPS'
	bl_label = "Enabled"
	bl_parent_id = "GLTF_PT_import_user_extensions"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(cls, context):
		sfile = context.space_data
		operator = sfile.active_operator
		return operator.bl_idname == "IMPORT_SCENE_OT_gltf"

	def draw_header(self, context):
		props = bpy.context.scene.ChronovoreImporterExtensionProperties
		self.layout.prop(props, 'enabled')

	def draw(self, context):
		layout = self.layout
		layout.use_property_split = True
		layout.use_property_decorate = False

		props = bpy.context.scene.ChronovoreImporterExtensionProperties
		layout.active = props.enabled


class glTF2ImportUserExtension:
	def __init__(self):
		self.properties = bpy.context.scene.ChronovoreImporterExtensionProperties
		self.extensions = [Extension(name="CHRONOVORE_material_attributes", extension={}, required=False)]

	def gather_import_material_after_hook(self, pymaterial, vertex_color, mat, gltf):
		if not self.properties.enabled:
			return

		exts = pymaterial.extensions or {}
		if not 'CHRONOVORE_material_attributes' in exts:
			return

		material_attr = exts['CHRONOVORE_material_attributes']

		workflow_name = material_attr.get('workflow', 'Basic Shader')

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
			print('unknown workflow "%s" on material "%s"' % (workflow_name, mat.name))

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

		height2 = 275
		color_list = material_attr.get('colors', {})
		for color_name in color_list:
			value_node = mh.nodes.new('ShaderNodeRGB')
			value_node.label = color_name
			value_node.location = x, y
			value_node.outputs[0].default_value = color_list[color_name]
			if color_name in group_node.inputs:
				mh.links.new(value_node.outputs[0], group_node.inputs[color_name])
			y -= height2

			alpha_node_name = color_name + ' Alpha'
			value_node = mh.nodes.new('ShaderNodeValue')
			value_node.label = alpha_node_name
			value_node.location = x, y
			value_node.outputs[0].default_value = color_list[color_name][3]
			if alpha_node_name in group_node.inputs:
				mh.links.new(value_node.outputs[0], group_node.inputs[alpha_node_name])
			y -= height


def register():
	bpy.utils.register_class(ChronovoreImporterExtensionProperties)
	bpy.types.Scene.ChronovoreImporterExtensionProperties = bpy.props.PointerProperty(type=ChronovoreImporterExtensionProperties)


def unregister():
	unregister_panel()
	bpy.utils.unregister_class(ChronovoreImporterExtensionProperties)
	del bpy.types.Scene.ChronovoreImporterExtensionProperties


def register_panel():
	try:
		bpy.utils.register_class(GLTF_PT_UserExtensionPanel)
	except Exception:
		pass

	return unregister_panel


def unregister_panel():
	try:
		bpy.utils.unregister_class(GLTF_PT_UserExtensionPanel)
	except Exception:
		pass
