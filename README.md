# glTF-Neptuwunium-EXT

This started off because I basically wanted to exert more control over materials in the [glTF Blender addon](https://github.com/KhronosGroup/glTF-Blender-IO).
While I can't get a prefix due to these not being contained to a single project and I'm not an organization, I still wanted to properly document the format of the schemas should people want to implement them.

A vague implementation exists in my project [glTFScaffold](https://github.com/neptuwunium/glTFScaffold/tree/develop/Extensions).

Prefix: `NEPTUWUNIUM_` (unapproved, unreserved as of 2024/02/05)

- NEPTUWUNIUM_material_attributes
- NEPTUWUNIUM_terrain_tile
- NEPTUWUNIUM_small_bones*
- NEPTUWUNIUM_bone_palette*

Entries marked with * need [my fork of the blender glTF addon](https://github.com/neptuwunium/glTF-Blender-IO) as it relies on accessor extensions, which are not ([yet](https://github.com/KhronosGroup/glTF-Blender-IO/issues/2634)) supported.

## NEPTUWUNIUM_material_attributes

unassociated material reference values, usually from shader pipelines.

```jsonc
{
  "materials": [
    {
      "name": "Nya",
      "extensions": {
        "NEPTUWUNIUM_material_attributes": {
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

## NEPTUWUNIUM_terrain_tile

A reference to a 2D heightmap for terrian. (Still unimplemented.)

```jsonc
{
  "nodes": [
    {
      "name": "Nya",
      "extensions": {
        "NEPTUWUNIUM_terrain_tile": {
          "tile": 0,
        }
      }
    }
  ],
  "extensions": {
    "NEPTUWUNIUM_terrain_tile": {
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

## NEPTUWUNIUM_small_bones

Support for VEC3, VEC2, and SCALAR bone weights and bone indices.

```jsonc
{
  "accessors": [
    {
      "bufferView": 1,
      "byteOffset": 7032,
      "componentType": 5123,
      "count": 585,
      "type": "VEC2",
      "normalized": false,
      "name": "JOINTS_0", // note: this must be present or accessors may not be properly recognized
      "extensions": {
        "NEPTUWUNIUM_small_bones": { }
      }
    },
    {
      "bufferView": 1,
      "byteOffset": 9372,
      "componentType": 5123,
      "count": 585,
      "type": "VEC2",
      "normalized": true,
      "name": "WEIGHTS_0", // note: this must be present or accessors may not be properly recognized
      "extensions": {
        "NEPTUWUNIUM_small_bones": { }
      }
    }
  ],
  "extensionsRequired": [
    "NEPTUWUNIUM_small_bones"
  ]
}
```

## NEPTUWUNIUM_bone_palette

Remaps bone indices based on a secondary lookup list.

```jsonc
{
  "accessors": [
    {
      "bufferView": 1,
      "byteOffset": 7032,
      "componentType": 5123,
      "count": 585,
      "type": "VEC4",
      "normalized": false,
    },
    {
      "bufferView": 1,
      "byteOffset": 11712,
      "componentType": 5126,
      "count": 585,
      "type": "VEC4",
      "extensions": {
        "NEPTUWUNIUM_bone_palette": {
          "palette": 2 // accessorId
        }
      }
    },
    {
      "bufferView": 1,
      "byteOffset": 21072,
      "componentType": 5123,
      "count": 64,
      "type": "SCALAR",
      "normalized": false,
    }
  ],
  "extensionsRequired": [
    "NEPTUWUNIUM_bone_palette"
  ]
}
```
