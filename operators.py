# operators.py
"""
This module handles all of the operations.
"""

import bpy
from bpy.types import Operator


class OBJECT_OT_rename_data_to_object(Operator):
    """Rename selected objects data to the object name."""
    bl_idname = "object.rename_data_to_object"
    bl_label = "Rename Selected Object Data"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def pool(cls, context):
        """Enable only if object data is mesh, curve, or metaball."""
        return any(obj.type in ['MESH', 'CURVE', 'META'] for obj in context.selected_objects)
    
    def execute(self, context):
        objects = [
            obj for obj in context.selected_objects if obj.type in ['MESH', 'CURVE', 'META']
        ]

        objects_sharing_data: list[bpy.types.Object] = []
        objects_to_rename: list[bpy.types.Object] = []
        for obj in objects:
            if obj.data.users == 1:
                objects_to_rename.append(obj)
            else:
                objects_sharing_data.append(obj)
        
        if objects_sharing_data:
            object_names = [ obj.name for obj in objects_sharing_data ]
            self.report({'WARNING'}, f"The objects share data and cannot be renamed [{', '.join(object_names)}]")

        if not objects_to_rename:
            self.report({'WARNING'}, "No mesh, curve, or metaball objects selected.")
            return {'CANCELLED'}

        for obj in objects_to_rename:
            obj.data.name = obj.name
        
        return {'FINISHED'}


class UV_OT_batch_unwrap(Operator):
    """Unwrap selected objects that contain mesh"""
    bl_idname = "uv.batch_unwrap"
    bl_label = "Batch Unwrap"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def pool(cls, context):
        """Enable only if object data is mesh"""
        return any(obj.type in ['Mesh'] for obj in context.selected_objects)

    def execute(self, context):
        objects_to_unwrap = [
            obj for obj in context.selected_objects if obj.type in ['MESH']
        ]
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects_to_unwrap:
            # Select the object and enter edit mode
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')

            # Select all faces
            bpy.ops.mesh.select_all(action='SELECT')

            # Unwrap the object
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.05)

            # Exit edit mode
            bpy.ops.object.mode_set(mode='OBJECT')
        
        return {'FINISHED'}


classes = (
    OBJECT_OT_rename_data_to_object,
    UV_OT_batch_unwrap,
)