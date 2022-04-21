Adding KHR_materials_volume and KHR_materials_ior to glTF files exported from Blender - Eevee
===
This addon adds KHR_materials_volume and KHR_materials_ior extensions to glTF files exported from Blender with Eeevee renderer, adding this functionalitier to the [official Khronos Group Blender IO addon](https://github.com/KhronosGroup/glTF-Blender-IO).

KHR_materials_volume and KHR_materials_ior are official glTF extensions, that work along KHR_materials_transmission to render "correct" refractions of materials like water, glass, crystal, etc.
[glTF Extensions Reference](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos)

This addon can also export attenuationDistance and attenuationColor from a Volume Absorption node that must be into the Eevee Material node tree, even if disconnected.
The attenuationDistance is converted from the Volume Absorption Densidy with this formula:
> attenuationDistance = ( 10.0 - min( volume_absorption_density, 10.0 ) ) + 0.1

This addon does not exports thicknessTexture property; still looking for a straightforward way to do it.

I provide another addon in this repo [ set_refraction_depth_from_active_volume.py ] that's useful to set refraction depth from active object bounding box volume in Blender - Eevee. After installing, you'll find "Refraction Depth From Volume" under Object menu.



Installation
---
Install this addon from Blender Preferences > Addons > Install... > Select the file, load it > activate the addon by checking it.
This addon works correctly with Eevee only.


Blender Scene
---
-Set Eevee as Render Engine in Blender.
-Set the scene, meshes, materials as you'd normally do.
-The refractive materials must have a Principled BSDF material.
-Set the Transmission and IOR properties of that Principled BSDF material the way you need.
-Set the material's refraction depth in material Settings panel, this will set thicknessFactor in KHR_materials_volume extension. 
-Note that different objects that need different thicknessFactor(s) must have unique materials.

<img width="1271" alt="Blender Scene - material" src="https://user-images.githubusercontent.com/1394193/160586341-f4e63966-076e-4750-9f74-cce5128748f9.png">
<img width="1271" alt="Blender Scene - materia settings" src="https://user-images.githubusercontent.com/1394193/160586366-25ccecf7-7965-45fb-99da-ae902e2a5eab.png">

I provide another addon [ set_refraction_depth_from_active_volume.py ] that's only to set refraction depth from active object bounding box volume in Blender.
After installing, you'll find "Refraction Depth From Volume" under Object menu.

_If you want to actually see refractions in Blender, enable "screen space reflections" and its sub-property "refraction" in Render Properties tab, and enable "Screen Space Refraction" in material Settings panel._



The Exporter
---
This addon is enabled by default, and in the glTF Export window you can disable it entirely or selectively, under the Extensions panel.

<img width="1227" alt="Blender glTF Exporter" src="https://user-images.githubusercontent.com/1394193/160586291-a0af8c82-31cb-45c4-a474-a3b9201053fd.png">



Working Example
---
The exported model is rendered with [three.js](https://github.com/mrdoob/three.js/), from glTF Tools addon [by [CesiumGS](https://github.com/CesiumGS)] in [Visual Studio Code](https://github.com/microsoft/vscode).

<img width="1276" alt="three.js via glTF Tools by CesiumGS in VSCode" src="https://user-images.githubusercontent.com/1394193/160586164-1a72badf-fe28-40e7-a39b-1c065c13fe1d.png">


License
---

This is licensed under the GNU General Public License, Version 3.
See [blender.org/about/license](https://www.blender.org/about/license) for details.
