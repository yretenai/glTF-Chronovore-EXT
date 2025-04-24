from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
from .CHRONOVORE_material_attributes import CHRONOVORE_material_attributes
# from .CHRONOVORE_terrain_tile import CHRONOVORE_terrain_tile

bl_info = {
	"name": "glTF Chronovore Importer Extension",
	"category": "Generic",
	"version": (1, 1, 0),
	"blender": (4, 3, 0),
	'location': 'File > Import > glTF 2.0',
	'description': 'Chronovore\'s glTF extensions.',
	'tracker_url': "https://github.com/yretenai/glTF-Chronovore-EXT/issues/",
	'isDraft': False,
	'developer': "chronovore",
	'url': 'https://github.com/yretenai/glTF-Chronovore-EXT',
}


class glTF2ImportUserExtension:
	def __init__(self):
		self.extensions = [
			Extension(name="CHRONOVORE_material_attributes", extension={}, required=False),
			Extension(name="CHRONOVORE_terrain_tile", extension={}, required=False),
		]


	def gather_import_material_after_hook(self, pymaterial, vertex_color, mat, gltf):
		exts = pymaterial.extensions or {}
		if 'CHRONOVORE_material_attributes' in exts:
			material_attr = exts['CHRONOVORE_material_attributes']
			CHRONOVORE_material_attributes(material_attr, pymaterial, vertex_color, mat, gltf)


def register(): pass


def unregister(): pass
