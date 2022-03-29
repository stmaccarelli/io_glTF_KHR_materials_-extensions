bl_info = {
    "name": "assign_reftaction_depth_from_volume",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "category": "Material",
    'location': 'Object > Refraction Depth From Volume',
    'description': 'Calculate and assign "refraction depth" material setting from active object bounding box volume.',
    'tracker_url': "https://github.com/stmaccarelli/blender_utils/issues/",
    'isDraft': False,
    'developer': "stmaccarelli", 
    'url': 'https://stefano-maccarelli.com', 
}


import bpy


class RefractionDepthFromVolume(bpy.types.Operator):
    """Assign Active Material's refraction depth from Active Object volume"""
    bl_idname = "object.ref_depth_from_active_volume"
    bl_label = "Refraction Depth From Volume"
    bl_options = {'REGISTER', 'UNDO'}

    def get_bounding_volume( self, object ):
        x = object.dimensions.x
        y = object.dimensions.y
        z = object.dimensions.z
        volume = x * y * z
        return volume ** (1. / 3)

    def execute(self, context):
        # what is the arvolume ea of active
        active_volume = self.get_bounding_volume( bpy.context.active_object )
        bpy.context.active_object.active_material.refraction_depth = active_volume / 2.0

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(RefractionDepthFromVolume.bl_idname)

def register():
    bpy.utils.register_class(RefractionDepthFromVolume)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(RefractionDepthFromVolume)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()