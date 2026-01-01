from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
from .NEPTUWUNIUM_material_attributes import NEPTUWUNIUM_material_attributes

bl_info = {
	"name": "glTF Neptuwunium Importer Extension",
	"category": "Generic",
	"version": (1, 1, 0),
	"blender": (4, 3, 0),
	'location': 'File > Import > glTF 2.0',
	'description': 'Neptuwunium\'s glTF extensions.',
	'tracker_url': "https://github.com/neptuwunium/glTF-Neptuwunium-EXT/issues/",
	'isDraft': False,
	'developer': "Neptuwunium",
	'url': 'https://github.com/neptuwunium/glTF-Neptuwunium-EXT',
}


class glTF2ImportUserExtension:
	def __init__(self):
		self.extensions = [
			Extension(name="CHRONOVORE_material_attributes", extension={}, required=False),
			Extension(name="NEPTUWUNIUM_material_attributes", extension={}, required=False),
			# Extension(name="NEPTUWUNIUM_terrain_tile", extension={}, required=False),
			Extension(name="NEPTUWUNIUM_small_bones", extension={}, required=False),
		]


	def gather_import_material_after_hook(self, pymaterial, vertex_color, mat, gltf):
		exts = pymaterial.extensions or {}
		if 'CHRONOVORE_material_attributes' in exts:
			NEPTUWUNIUM_material_attributes(exts['CHRONOVORE_material_attributes'], pymaterial, vertex_color, mat, gltf)
		if 'NEPTUWUNIUM_material_attributes' in exts:
			NEPTUWUNIUM_material_attributes(exts['NEPTUWUNIUM_material_attributes'], pymaterial, vertex_color, mat, gltf)


def register(): pass


def unregister(): pass
