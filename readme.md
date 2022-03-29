adding KHR_materials_volume and KHR_materials_ior to glTF files exported from Blender
===
This addon adds KHR_materials_volume and KHR_materials_ior extensions to glTF files exported from Blender, working as a "plugin" for the official Khronos Group Blender I/O addon.

KHR_materials_volume and KHR_materials_ior are official glTF extensions, that work along KHR_materials_transmission to render "correct" refractions of materials like water, glass, crystal, etc.

It can also export attenuationDistance and attenuationColor from a Volume Absorption node that must be into the Eevee Material node tree, even if disconnected.
The attenuationDistance is converted from the Volume Absorption Densidy with this formula:
> attenuationDistance = ( 10.0 - min( volume_absorption_density, 10.0 ) ) + 0.1

This addon does not exports thicknessTexture property; still looking for a straightforward way to do it.


Installation
---
Install this addon from Blender Preferences > Addons > Install... > Select the file, load it > activate the addon by checking it.


Blender Scene
---
Set the scene, meshes, materials as you'd normally do in Blender.
Set the refractive materials' transmission and ior properties the way you need.
Set the thicknessFactor by setting material's refraction depth in material Settings panel.
Note that different objects that need different thicknessFactor must have a unique material.

--

I provide another addon ( set_refraction_depth_from_active_volume.py ) that's only to set refraction depth from active object bounding box volume in Blender.
After installing, you'll find "Refraction Depth From Volume" under Object menu.

_If you want to actually see refractions in Blender, enable "screen space reflections" and its sub-property "refraction" in Render Properties tab, and enable "Screen Space Refraction" in material Settings panel._


The Exporter
---
This addon is enabled by default, and in the glTF Export window you can disable it entirely or selectively, under the Extensions panel.

--


Working Example
---
The esported model rendered with three.js, from glTF Tools addon for Visual Studio Code.




License
---

As a Blender addon, this addon is licensed under the GNU General Public License, Version 3.

See [blender.org/about/license](https://www.blender.org/about/license) for details.
