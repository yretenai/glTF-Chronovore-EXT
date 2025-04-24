# glTF-Chronovore-EXT

This started off because I basically wanted to exert more control over materials in the [glTF Blender addon](https://github.com/KhronosGroup/glTF-Blender-IO).
While I am much too insignificant to even bother requesting a prefix, I still wanted to properly document the format of the schemas should people want to implement them.

Prefix: `CHRONOVORE_` (unapproved, unreserved as of 2024/02/05)

- CHRONOVORE_material_attributes
- CHRONOVORE_terrain_tile

## CHRONOVORE_material_attributes

unassociated material reference values, usually from shader pipelines.

```json
{
	"materials": [
		{
			"name": "Nya",
			"extensions": {
				"CHRONOVORE_material_attributes": {
					"workflow": "Node Graph Shader", // Shader name or node graph name (in blender)
					"textures": {
						"Albedo": { // TextureInfo
							"index": 0,
							"texCoord": 0,
						}
					},
					"scalars": {
						"Emission Intensity": 1.0 // double
					},
					"colors": {
						"Emission Color": [1.0, 0.0, 1.0, 1.0] // double * 4
					}
				}
			}
		}
	]
}
```

## CHRONOVORE_terrain_tile

A reference to a 2D heightmap for terrian. (Still unimplemented.)

```json
{
	"nodes": [
		{
			"name": "Nya",
			"extensions": {
				"CHRONOVORE_terrain_tile": {
					"tile": 0,
				}
			}
		}
	],
	"extensions": {
		"CHRONOVORE_terrain_tile": {
			"tile": [
				{
					"heightmap": { // TextureInfo
						"index": 0,
						"texCoord": 0,
					},
					"material": 0,
					"resolution": 1024, // grid density
					"size": [128.0, 128.0], // x and y units
					"range": [0.0, 16.0] // min to max height
				}
			]
		}
	}
}
```
