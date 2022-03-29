import bpy

bl_info = {
    "name": "KHR_materials_volume",
    "category": "Import-Export",
    "version": (1, 0, 7),
    "blender": (2, 80, 0),
    'location': 'File > Export > glTF 2.0',
    'description': 'Add KHR_materials_volume and KHR_materials_ior to glTF exporter.',
    'tracker_url': "https://github.com/stmaccarelli/io_GLTF_KHR_materials_extensions/issues/",
    'isDraft': False,
    'developer': "stmaccarelli", 
    'url': 'https://stefano-maccarelli.com', 
}

# glTF extensions are named following a convention with known prefixes.
# See: https://github.com/KhronosGroup/glTF/tree/master/extensions#about-gltf-extensions
# also: https://github.com/KhronosGroup/glTF/blob/master/extensions/Prefixes.md

# Support for an extension is "required" if a typical glTF viewer cannot be expected
# to load a given model without understanding the contents of the extension.
# For example, a compression scheme or new image format (with no fallback included)
# would be "required", but physics metadata or app-specific settings could be optional.
extension_is_required = False

class VolumeExtensionsProperties(bpy.types.PropertyGroup):
    khr_materials_volume_enabled: bpy.props.BoolProperty(
        name='HKR_materials_volume',
        description='Include HKR_materials_volume extension',
        default = True
        )
    export_thickness_factor: bpy.props.BoolProperty(
        name = 'export thicknessFactor',
        description = 'export thicknessFactor from Refraction Depth',
        default = True
        )
    export_attenuation_color: bpy.props.BoolProperty(
        name = 'export attenuationColor',
        description = 'export attenuationColor from Volume Absorption node',
        default = True
        )
    export_attenuation_dist: bpy.props.BoolProperty(
        name = 'export attenuationDistance',
        description = 'export attenuationDistance from Volume Absorption node',
        default = True
        )
    export_ior: bpy.props.BoolProperty(
        name = 'export_ior',
        description = 'export IOR (Index Of Refraction) from Principled BSDF property',
        default = True
        )
    

def register():
    bpy.utils.register_class(VolumeExtensionsProperties)
    bpy.types.Scene.VolumeExtensionsProperties = bpy.props.PointerProperty(type=VolumeExtensionsProperties)

def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(GLTF_PT_UserExtensionPanel)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister_panel():
    # Since panel is registered on demand, it is possible it is not registered
    try:
        bpy.utils.unregister_class(GLTF_PT_UserExtensionPanel)
    except Exception:
        pass


def unregister():
    unregister_panel()
    bpy.utils.unregister_class(VolumeExtensionsProperties)
    del bpy.types.Scene.VolumeExtensionsProperties

class GLTF_PT_UserExtensionPanel(bpy.types.Panel):

    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "More KHR Extensions"
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"


    def draw(self, context):
        self.layout.alignment = 'LEFT'
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False  # No animation.

        props = bpy.context.scene.VolumeExtensionsProperties
        # self.layout.active = props.khr_materials_volume_enabled
       
        # box = self.layout.box()
        # box.label(text="This addon is intended to export models for real-time engines")

        col1 = self.layout.column(heading = "Extensions", align = True)
        # row1.alignment = 'LEFT'
        col1.prop(props, 'khr_materials_volume_enabled', text = "KHR_materials_volume")
        col1.prop(props, 'export_ior', text = "KHR_materials_ior")

        col1 = self.layout.column(heading = "Properties", align = True)
        # col1.alignment = 'EXPAND'
        col1.active = props.khr_materials_volume_enabled
        col1.prop(props, 'export_thickness_factor', text="thicknessFactor")
        col1.prop(props, 'export_attenuation_color', text="attenuationColor")
        col1.prop(props, 'export_attenuation_dist', text="attenuationDistance")
    

class glTF2ExportUserExtension:

    def __init__(self):
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.Extension = Extension
        self.properties = bpy.context.scene.VolumeExtensionsProperties

    def gather_material_hook(self, gltf2_object, blender_material, export_settings):

            if gltf2_object.extensions["KHR_materials_transmission"] and self.properties.export_ior and blender_material.node_tree.nodes["Principled BSDF"]:
                gltf2_object.extensions["KHR_materials_ior"] = self.Extension(
                name="KHR_materials_ior",
                extension={"ior": blender_material.node_tree.nodes["Principled BSDF"].inputs["IOR"].default_value },
                required=extension_is_required
                )

            if gltf2_object.extensions["KHR_materials_transmission"] and self.properties.khr_materials_volume_enabled:

                # If we want to export thickness and / or absorption, we must define KHR_materials_volume extension
                # if self.properties.export_thickness_factor or self.properties.export_attenuation_data:
                gltf2_object.extensions["KHR_materials_volume"] = self.Extension(
                name="KHR_materials_volume",
                extension={ },
                required=extension_is_required
                )

                if self.properties.export_thickness_factor:
                    gltf2_object.extensions["KHR_materials_volume"].extension.update({
                    "thicknessFactor": blender_material.refraction_depth
                    })
                    
                #  if we would export absorption only if Volume Absorption node is connected, we must use this:
                #  bpy.context.object.material_slots[0].material.node_tree.nodes['Volume Absorption'].outputs['Volume'].is_linked
                if self.properties.export_attenuation_color and blender_material.node_tree.nodes["Volume Absorption"]:
                    vc = blender_material.node_tree.nodes["Volume Absorption"].inputs['Color'].default_value
                    gltf2_object.extensions["KHR_materials_volume"].extension.update({
                    "attenuationColor": [ vc[0], vc[1], vc[2] ]
                    }) 

                if self.properties.export_attenuation_dist and blender_material.node_tree.nodes["Volume Absorption"]:
                    vd = blender_material.node_tree.nodes["Volume Absorption"].inputs['Density'].default_value
                    # this is quite arbitrary and empiric, looks like a decent compromise to uniform
                    # Blender (eevee-ish), Three.js, Filament.js, Babylon.js
                    vd = ( 10.0 - min( vd, 10.0 ) ) + 0.1
                    gltf2_object.extensions["KHR_materials_volume"].extension.update({
                    "attenuationDistance": vd
                    }) 

# this is how to get shader connected so Surface input of the final output Blender node
# bpy.data.objects['1642174861.3846831'].material_slots[0].material.node_tree.nodes['Material Output'].inputs['Surface'].links[0].from_node.inputs['Subsurface'].