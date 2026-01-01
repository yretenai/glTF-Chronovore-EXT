from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
from io_scene_gltf2.io.imp.gltf2_io_binary import BinaryData
from .NEPTUWUNIUM_material_attributes import NEPTUWUNIUM_material_attributes
import numpy as np

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
			Extension(name="NEPTUWUNIUM_small_bones", extension={}, required=True),
			Extension(name="NEPTUWUNIUM_bone_palette", extension={}, required=True)
		]


	def gather_import_material_after_hook(self, pymaterial, vertex_color, mat, gltf):
		exts = pymaterial.extensions or {}
		if 'CHRONOVORE_material_attributes' in exts:
			NEPTUWUNIUM_material_attributes(exts['CHRONOVORE_material_attributes'], pymaterial, vertex_color, mat, gltf)
		if 'NEPTUWUNIUM_material_attributes' in exts:
			NEPTUWUNIUM_material_attributes(exts['NEPTUWUNIUM_material_attributes'], pymaterial, vertex_color, mat, gltf)

	def decode_accessor_after_hook(self, pyaccessor, array, gltf):
		exts = pyaccessor.extensions or {}
		name = pyaccessor.name
		mutated = array.value

		if 'NEPTUWUNIUM_bone_palette' in exts and name.startswith('JOINTS_'):
			palette = BinaryData.decode_accessor(gltf, exts['NEPTUWUNIUM_bone_palette']['palette'], cache=True)
			mutated = palette[mutated]

		if 'NEPTUWUNIUM_small_bones' in exts and (name.startswith("JOINTS_") or name.startswith("WEIGHTS_")) and mutated.shape[1] < 4:
			newMutated = np.zeros((mutated.shape[0], 4), dtype=mutated.dtype)
			newMutated[:, :mutated.shape[1]] = mutated
			mutated = newMutated

		array.value = mutated


def register(): pass


def unregister(): pass
