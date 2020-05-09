import bpy
import os

from . import utils, key_utils, cur_utils, slider_tools, magnet
from bpy.props import StringProperty, EnumProperty, BoolProperty, \
    IntProperty, FloatProperty
from bpy.types import Operator


# ###############  SLIDERS  ###############


class AAT_OT:
    """Slider Operators Preset"""
    bl_options = {'UNDO_GROUPED'}

    slope: FloatProperty(default=2.0)
    factor: FloatProperty(default=0.0)
    slot_index: IntProperty(default=-1)
    op_context: StringProperty(default='INVOKE_DEFAULT', options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        return slider_tools.poll(context)

    def __init__(self):
        self.animaide = bpy.context.scene.animaide
        self.slots = self.animaide.slider_slots
        self.item = self.animaide.slider
        self.init_mouse_x = None

    def __del__(self):
        pass

    def execute(self, context):
        utils.update_keyframe_points(context)
        return slider_tools.looper(self, context)

    def modal(self, context, event):
        return slider_tools.modal(self, context, event)

    def invoke(self, context, event):
        return slider_tools.invoke(self, context, event)


class AAT_OT_ease_to_ease(Operator, AAT_OT):
    """Transition selected keys - or current key - from the neighboring\n""" \
        """ones with a "S" shape manner (ease-in and ease-out simultaneously).\n""" \
        """It doesn't take into consideration the current key values."""
    bl_idname = "animaide.ease_to_ease"
    bl_label = "Ease To Ease"

    slider_type = 'EASE_TO_EASE'


class AAT_OT_ease(Operator, AAT_OT):
    """Transition selected keys - or current key - from the neighboring\n""" \
        """ones with a "C" shape manner (ease-in or ease-out). It doesn't\n""" \
        """take into consideration the current key values."""
    bl_idname = "animaide.ease"
    bl_label = "Ease"

    slider_type = 'EASE'


class AAT_OT_blend_neighbor(Operator, AAT_OT):
    """Blend selected keys - or current key - to the value of the neighboring\n""" \
        """left and right keys."""
    bl_idname = "animaide.blend_neighbor"
    bl_label = "Blend Neighbor"

    slider_type = 'BLEND_NEIGHBOR'


class AAT_OT_blend_frame(Operator, AAT_OT):
    """Blend selected keys - or current key - to the value of the chosen\n""" \
        """left and right frames."""
    bl_idname = "animaide.blend_frame"
    bl_label = "Blend Frame"

    slider_type = 'BLEND_FRAME'


class AAT_OT_blend_ease(Operator, AAT_OT):
    """Blend selected keys - or current key - to the ease-in or ease-out\n""" \
        """curve using the neighboring keys."""
    bl_idname = "animaide.blend_ease"
    bl_label = "Blend Ease"

    slider_type = 'BLEND_EASE'


class AAT_OT_blend_offset(Operator, AAT_OT):
    """Blend selected keys - or current key - to the\n""" \
        """value of the chosen left and right frames."""
    bl_idname = "animaide.blend_offset"
    bl_label = "Blend Offset"

    slider_type = 'BLEND_OFFSET'


class AAT_OT_tween(Operator, AAT_OT):
    """Set lineal relative value of the selected keys - or current key -\n""" \
        """in relationship to the neighboring ones. It doesn't take into\n""" \
        """consideration the current key values."""
    bl_idname = "animaide.tween"
    bl_label = "Tween"

    slider_type = 'TWEEN'


class AAT_OT_push_pull(Operator, AAT_OT):
    """Exagerates or decreases the value of the selected keys - or current key -"""
    bl_idname = "animaide.push_pull"
    bl_label = "Push Pull"

    slider_type = 'PUSH_PULL'


class AAT_OT_smooth(Operator, AAT_OT):
    """Averages values of selected keys creating a smoother fcurve"""
    bl_idname = "animaide.smooth"
    bl_label = "Smooth"

    slider_type = 'SMOOTH'


class AAT_OT_time_offset(Operator, AAT_OT):
    """Shift the value of selected keys - or current key -\n""" \
        """to the ones of the left or right in the same fcurve"""
    bl_idname = "animaide.time_offset"
    bl_label = "Time Offset"

    slider_type = 'TIME_OFFSET'


class AAT_OT_noise(Operator, AAT_OT):
    """Set random values to the selected keys - or current key -"""
    bl_idname = "animaide.noise"
    bl_label = "Noise"

    slider_type = 'NOISE'


class AAT_OT_scale_left(Operator, AAT_OT):
    """Increase or decrease the value of selected keys - or current key -\n""" \
        """in relationship to the left neighboring one."""
    bl_idname = "animaide.scale_left"
    bl_label = "Scale Left"

    slider_type = 'SCALE_LEFT'


class AAT_OT_scale_right(Operator, AAT_OT):
    """Increase or decrease the value of selected keys - or current key -\n""" \
        """in relationship to the right neighboring one."""
    bl_idname = "animaide.scale_right"
    bl_label = "Scale Right"

    slider_type = 'SCALE_RIGHT'


class AAT_OT_scale_average(Operator, AAT_OT):
    """Increase or decrease the value of selected keys - or current key -\n""" \
        """in relationship to the average point of those affected"""
    bl_idname = "animaide.scale_average"
    bl_label = "Scale Average"

    slider_type = 'SCALE_AVERAGE'


# ------- sliders extra operators ------


class AAT_OT_sliders_settings(Operator):
    """Options related to the current tool on the slider"""
    bl_idname = "animaide.sliders_settings"
    bl_label = "Sliders Settings"

    slot_index: IntProperty()

    @classmethod
    def poll(cls, context):
        return slider_tools.poll(context)

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=150)

    def draw(self, context):
        animaide = context.scene.animaide
        if self.slot_index < 0:
            slider = animaide.slider
        else:
            slider = animaide.slider_slots[self.slot_index]

        layout = self.layout
        col = layout.column(align=False)
        col.label(text='Settings')
        # if slider.selector == 'EASE_TO_EASE' or
        #     slider.selector == 'EASE' or
        #     slider.selector == 'BLEND_EASE':
        if 'EASE' in slider.selector:
            col.prop(slider, 'slope', text='Slope', slider=False)
        # if 'BLEND' not in slider.selector and slider.selector != 'SMOOTH':
        col.prop(slider, 'overshoot', text='Overshoot', toggle=False)
        if slider.selector == 'BLEND_FRAME':
            col.prop(slider, 'use_markers', text='Use Markers', toggle=False)
        if slider.selector == 'NOISE':
            col.prop(slider, 'noise_phase', text='Phase', slider=True)

        # col.prop(animaide.slider, 'affect_non_selected_frame', text='Not selected frames', toggle=False)


class AAT_OT_global_settings(Operator):
    """Options for the entire sliders tool"""
    bl_idname = "animaide.global_settings"
    bl_label = "Global Settings"

    slot_index: IntProperty()

    @classmethod
    def poll(cls, context):
        return slider_tools.poll(context)

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=200)

    def draw(self, context):
        animaide = context.scene.animaide

        layout = self.layout
        col = layout.column(align=False)
        col.label(text='Settings')
        col.prop(animaide.slider, 'affect_non_selected_fcurves', text='Non-selected fcurves', toggle=False)
        col.prop(animaide.slider, 'affect_non_selected_keys', text='Non-selected keys on frame', toggle=False)


class AAT_OT_add_slider(Operator):
    """Add aditional slider to the panel"""
    bl_idname = 'animaide.add_slider'
    bl_label = "add_slider"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        animaide = context.scene.animaide
        slots = animaide.slider_slots
        slot = slots.add()
        slot.index = len(slots) - 1

        return {'FINISHED'}


class AAT_OT_remove_slider(Operator):
    """Removes last slider of the list"""
    bl_idname = 'animaide.remove_slider'
    bl_label = "remove_slider"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        animaide = context.scene.animaide
        slots = animaide.slider_slots
        # if len(slots) > 1:
        index = len(slots) - 1
        slots.remove(index)
        slider_tools.remove_marker(index + 2)

        return {'FINISHED'}


class AAT_OT_get_ref_frame(Operator):
    """Sets a refernce frame that will be use by the BLEND FRAME\n""" \
        """slider. The one at the left sets the left reference, and the\n""" \
        """one on the right sets the right reference"""
    bl_idname = 'animaide.get_ref_frame'
    bl_label = "get_ref_frames"
    bl_options = {'REGISTER'}

    slot_index: IntProperty(default=-1)
    side: StringProperty()
    # is_collection: BoolProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        animaide = context.scene.animaide

        # if self.slot_index == -1:
        #     slider_num = '1'
        # else:
        #     slider_num = '%s' % (self.slot_index + 2)
        #
        # if self.is_collection:

        if self.slot_index == -1:
            slider = animaide.slider
            slider_num = 1
        else:
            slider = animaide.slider_slots[self.slot_index]
            slider_num = self.slot_index + 2

        current_frame = bpy.context.scene.frame_current

        # if self.is_collection:
        #     slider_num = self.slot_index + 2
        # else:
        #     slider_num = 1

        if self.side == 'L':
            slider.left_ref_frame = current_frame

        if self.side == 'R':
            slider.right_ref_frame = current_frame

        if slider.use_markers:
            slider_tools.add_marker(
                name_a='F',
                name_b=slider_num,
                side=self.side,
                frame=current_frame
            )
        else:
            for side in ['L', 'R']:
                slider_tools.remove_marker(
                    name_a='F',
                    name_b=slider_num,
                    side=side
                )
            # utils.remove_marker(slider_num)

        # key_utils.get_ref_frame_globals(slider.left_neighbor, slider.right_neighbor)

        # else:
        #
        #     if self.side == 'L':
        #         item.left_ref_frame = current_frame
        #
        #     if self.side == 'R':
        #         item.right_ref_frame = current_frame
        #
        #     left_ref_frame = item.left_ref_frame
        #     right_ref_frame = item.right_ref_frame
        #     key_utils.get_ref_frame_globals(left_ref_frame, right_ref_frame)

        return {'FINISHED'}


# ###############  ANIM TRANSFORM  ###############


class AAT_OT_create_anim_trans_mask(Operator):
    """Adds a mask to the AnimTransform. It determins the influence\n""" \
        """over the keys in the object being manipulated in the 3D View"""
    bl_idname = "animaide.create_anim_trans_mask"
    bl_label = "Create Mask"
    # bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return magnet.poll(context)

    def execute(self, context):
        scene = context.scene
        animaide = scene.animaide

        # key_utils.get_anim_transform_globals(obj)

        cur_frame = bpy.context.scene.frame_current

        animaide.anim_transform.mask_margin_l = cur_frame
        animaide.anim_transform.mask_margin_r = cur_frame
        animaide.anim_transform.mask_blend_l = -5
        animaide.anim_transform.mask_blend_r = 5

        magnet.add_anim_trans_mask()

        # context.scene.tool_settings.use_keyframe_insert_auto = False

        if magnet.anim_trans_mask_handlers not in bpy.app.handlers.depsgraph_update_pre:
            bpy.app.handlers.depsgraph_update_pre.append(magnet.anim_trans_mask_handlers)

        return {'FINISHED'}


class AAT_OT_anim_transform_on(Operator):
    """Enables AnimTransform. Modify the entire animation\n""" \
        """based on the object manipulation in the 3D View.\n""" \
        """This tool desables auto-key"""
    bl_idname = "animaide.anim_transform_on"
    bl_label = "Activate"
    # bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return magnet.poll(context)

    def execute(self, context):
        animaide = context.scene.animaide
        animaide.anim_transform.active = True
        magnet.user_auto_animate = context.scene.tool_settings.use_keyframe_insert_auto
        context.scene.tool_settings.use_keyframe_insert_auto = False
        # context.area.tag_redraw()
        # bpy.ops.wm.redraw_timer()
        # bpy.data.window_managers['WinMan'].windows.update()

        if magnet.anim_transform_handlers not in bpy.app.handlers.depsgraph_update_pre:
            bpy.app.handlers.depsgraph_update_pre.append(magnet.anim_transform_handlers)

        bpy.data.window_managers['WinMan'].update_tag()

        return {'FINISHED'}


class AAT_OT_anim_transform_off(Operator):
    """Disable AnimTransform. Objects can be animated again"""
    bl_idname = "animaide.anim_transform_off"
    bl_label = "Deactivate"
    # bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return magnet.poll(context)

    def execute(self, context):
        animaide = context.scene.animaide
        animaide.anim_transform.active = False

        if magnet.anim_transform_handlers in bpy.app.handlers.depsgraph_update_pre:
            bpy.app.handlers.depsgraph_update_pre.remove(magnet.anim_transform_handlers)

        if magnet.anim_trans_mask_handlers in bpy.app.handlers.depsgraph_update_pre:
            bpy.app.handlers.depsgraph_update_pre.remove(magnet.anim_trans_mask_handlers)

        magnet.remove_anim_trans_mask()

        context.scene.tool_settings.use_keyframe_insert_auto = magnet.user_auto_animate
        # context.area.tag_redraw()
        # bpy.ops.wm.redraw_timer()
        # bpy.data.window_managers['WinMan'].windows.update()
        bpy.data.window_managers['WinMan'].update_tag()

        return {'FINISHED'}


class AAT_OT_delete_anim_trans_mask(Operator):
    """Removes the anim_trans_mask from the scene"""
    bl_idname = "animaide.delete_anim_trans_mask"
    bl_label = "Delete Mask"
    # bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return magnet.poll(context)

    def execute(self, context):

        if magnet.anim_trans_mask_handlers in bpy.app.handlers.depsgraph_update_pre:
            bpy.app.handlers.depsgraph_update_pre.remove(magnet.anim_trans_mask_handlers)

        magnet.remove_anim_trans_mask()

        return {'FINISHED'}


class AAT_OT_anim_transform_settings(Operator):
    """Options related to the anim_transform"""
    bl_idname = "animaide.anim_transform_settings"
    bl_label = "Anim Transform Settings"
    # bl_options = {'REGISTER'}

    slot_index: IntProperty()

    @classmethod
    def poll(cls, context):
        return magnet.poll(context)

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=150)

    def draw(self, context):
        animaide = context.scene.animaide

        layout = self.layout

        row = layout.row(align=False)
        row.prop(animaide.anim_transform, 'easing', text='', icon_only=False)
        row = layout.row(align=False)
        row.prop(animaide.anim_transform, 'interp', text=' ', expand=True)
        # row = layout.row(align=False)
        # row.prop(animaide.anim_transform, 'use_markers', text='Use Markers')
        # row.prop(animaide.anim_transform, 'interp', text='', icon_only=False)


# ###############  HELP  ###############


class AAT_OT_help(Operator):
    """Shows all the shortuts for the tool"""
    bl_idname = "animaide.help"
    bl_label = "Shortcuts"

    slot_index: IntProperty()

    @classmethod
    def poll(cls, context):
        return slider_tools.poll(context)

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=200)

    def draw(self, context):
        animaide = context.scene.animaide

        layout = self.layout
        col = layout.column(align=False)
        col.label(text='Shortcuts')
        col.label(text='')
        col.label(text='Ease To Ease    (1)')
        col.label(text='Tween           (shift 1)')
        col.label(text='Ease-In-Out     (2)')
        col.label(text='Blend Ease      (shift 2)')
        col.label(text='Blend Neighbor  (3)')
        col.label(text='Blend Frame     (shift 3)')
        col.label(text='Push-Pull       (4)')
        col.label(text='Scale Average   (shift 4)')
        col.label(text='Scale Left      (5)')
        col.label(text='Scale Right     (shift 5)')
        col.label(text='Smooth          (6)')
        col.label(text='Noise           (shift 6)')
        col.label(text='Time Offset     (7)')
        col.label(text='Blend Offset    (shift 7)')
        col.label(text='')
        col.label(text='Toward Left Neighbor    (-)')
        col.label(text='Toward Right Neighbor   (+)')
        col.label(text='')
        col.label(text='To Left Neighbor    (shift -)')
        col.label(text='To Right Neighbor   (shift +)')
        col.label(text='')
        col.label(text='pie_menu-1  (alt 1)')
        col.label(text='pie_menu-2  (alt 2)')


class AAT_OT_manual(Operator):
    """Opens Animaide manual"""
    bl_idname = "animaide.manual"
    bl_label = "Manual"

    slot_index: IntProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "readme.html")
        url = 'file://' + path
        bpy.ops.wm.url_open(url=url)
        # bpy.ops.wm.url_open(url="https://github.com/aresdevo/animaide/blob/master/readme.md")
        return {'FINISHED'}


# Variable to register Classes

classes = (
    AAT_OT_add_slider,
    AAT_OT_remove_slider,
    AAT_OT_anim_transform_on,
    AAT_OT_anim_transform_off,
    AAT_OT_help,
    AAT_OT_manual,
    AAT_OT_sliders_settings,
    AAT_OT_global_settings,
    AAT_OT_anim_transform_settings,
    AAT_OT_get_ref_frame,
    AAT_OT_ease_to_ease,
    AAT_OT_ease,
    AAT_OT_blend_ease,
    AAT_OT_blend_neighbor,
    AAT_OT_blend_frame,
    AAT_OT_blend_offset,
    AAT_OT_push_pull,
    AAT_OT_scale_average,
    AAT_OT_scale_left,
    AAT_OT_scale_right,
    AAT_OT_smooth,
    AAT_OT_noise,
    AAT_OT_time_offset,
    AAT_OT_tween,
    AAT_OT_create_anim_trans_mask,
    AAT_OT_delete_anim_trans_mask
)
