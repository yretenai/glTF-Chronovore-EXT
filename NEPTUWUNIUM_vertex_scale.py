import bpy
from io_scene_gltf2.io.com.gltf2_io import TextureInfo
from io_scene_gltf2.blender.imp.texture import texture
from io_scene_gltf2.blender.imp.material_utils import MaterialHelper
import numpy as np


def NEPTUWUNIUM_vertex_scale(vtx_scale, name, mutated, gltf):
	if 'component' in vtx_scale:
		component = vtx_scale["component"]
		multiplier = mutated[:, component:component+1] * vtx_scale.get("componentScale", 1.0)
		mutated = np.delete(mutated, component, axis=1) * multiplier

	if 'scale' in vtx_scale:
		multiplier_base = np.array(vtx_scale['scale'])
		multiplier = np.ones((mutated.shape[1],))
		amount = min([multiplier_base.shape[0], mutated.shape[1]])
		multiplier[:amount] = multiplier[:amount] * multiplier_base
		mutated = mutated * multiplier

	if 'offset' in vtx_scale:
		addend_base = np.array(vtx_scale['offset'])
		addend = np.ones((mutated.shape[1],))
		amount = min([addend_base.shape[0], mutated.shape[1]])
		addend[:amount] = addend[:amount] * addend_base
		mutated = mutated + addend

	return mutated
