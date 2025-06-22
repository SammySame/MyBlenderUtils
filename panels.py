# panels.py
"""
This module contains the UI panels.
"""

import bpy
from bpy.types import Panel

class VIEW3D_PT_utilities_panel(Panel):
    bl_label = "My Utilities"
    bl_idname = "VIEW3D_PT_utilities_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        selected_object_count = len(context.selected_objects)
        row.operator("object.rename_data_to_object", text=f"Rename Object Data({selected_object_count})")
        row.enabled = selected_object_count > 0

        row = layout.row()
        row.operator("uv.batch_unwrap", text=f"Unwrap objects({selected_object_count})")
        row.enabled = selected_object_count > 0


# Registration
classes = (
    VIEW3D_PT_utilities_panel,
)