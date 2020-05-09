import bpy

from . import key_utils, cur_utils, utils

from bpy.props import StringProperty, BoolProperty, EnumProperty, \
    IntProperty, FloatProperty, PointerProperty, CollectionProperty
from bpy.types import PropertyGroup, AddonPreferences


icons = {'EASE_TO_EASE': 'IPO_EASE_IN_OUT',
         'EASE': 'ANIM_DATA',
         'BLEND_EASE': 'TRACKING',
         'BLEND_NEIGHBOR': 'TRACKING_FORWARDS',
         'BLEND_FRAME': 'TRACKING_FORWARDS_SINGLE',
         'BLEND_OFFSET': 'CURVE_PATH',
         'PUSH_PULL': 'UV_SYNC_SELECT',
         'SCALE_AVERAGE': 'FULLSCREEN_EXIT',
         'SCALE_LEFT': 'IMPORT',
         'SCALE_RIGHT': 'EXPORT',
         'SMOOTH': 'SMOOTHCURVE',
         'NOISE': 'RNDCURVE',
         'TIME_OFFSET': 'CENTER_ONLY',
         'TWEEN': 'DRIVER_DISTANCE'}


names = {'EASE_TO_EASE': 'Ease To Ease',
         'EASE': 'Ease',
         'BLEND_EASE': 'Blend Ease',
         'BLEND_NEIGHBOR': 'Blend Neighbor',
         'BLEND_FRAME': 'Blend Frame',
         'BLEND_OFFSET': 'Blend Offset',
         'PUSH_PULL': 'Push Pull',
         'SCALE_AVERAGE': 'Scale Average',
         'SCALE_LEFT': 'Scale Left',
         'SCALE_RIGHT': 'Scale Right',
         'SMOOTH': 'Smooth',
         'NOISE': 'Noise',
         'TIME_OFFSET': 'Time Offset',
         'TWEEN': 'Tween'}


def update_clone_move(self, context):

    objects = context.selected_objects

    cur_utils.move_clone(objects)

    return


def update_overshoot(self, context):
    # change values when overshoot property is changed

    if self.overshoot:
        self.min_value = -2.0
        self.max_value = 2.0
    else:
        self.min_value = -1.0
        self.max_value = 1.0


def update_selector(self, context):
    # change values when selector property is changed

    key_utils.get_sliders_globals()
    self.overshoot = False
    self.modal_switch = False


class AnimAideAnimTransform(PropertyGroup):

    active: BoolProperty()

    use_mask: BoolProperty()

    # use_markers: BoolProperty(default=True,
    #                           description='Let you choose to use markers for the mask',
    #                           update=toggle_anim_trans_markers)

    mask_margin_l: IntProperty(default=0,
                               description="Margin for the mask")
    mask_blend_l: IntProperty(default=0, max=0,
                              description="Fade value for the left margin")
    mask_margin_r: IntProperty(default=0,
                               description="Margin for the mask")
    mask_blend_r: IntProperty(default=0, min=0,
                              description="Fade value for the right margin")

    mask_blend_mapping: FloatProperty()

    interp: EnumProperty(
        items=[('LINEAR', ' ', 'Linear transition', 'IPO_LINEAR', 1),
               ('SINE', ' ', 'Curve slope 1', 'IPO_SINE', 2),
               ('CUBIC', ' ', 'Curve slope 3', 'IPO_CUBIC', 3),
               ('QUART', ' ', 'Curve Slope 4', 'IPO_QUART', 4),
               ('QUINT', ' ', 'Curve Slope 5', 'IPO_QUINT', 5)],
        name="Interpolation",
        default='SINE'
    )

    easing: EnumProperty(
        items=[('EASE_IN', 'Sharp', 'Sets Mask transition type', 'SHARPCURVE', 1),
               ('EASE_IN_OUT', 'Smooth', 'Sets Mask transition type', 'SMOOTHCURVE', 2),
               ('EASE_OUT', 'Round', 'Sets Mask transition type', 'INVERSESQUARECURVE', 3)],
        name="Easing",
        default='EASE_IN_OUT'
    )


class AnimAideClone(PropertyGroup):

    move_factor: FloatProperty(default=0.0,
                               min=-2.0,
                               max=2.0,
                               update=update_clone_move)

    cycle_options = [('NONE', 'None', '', '', 1),
                     ('REPEAT', 'Repeat', '', '', 2),
                     ('REPEAT_OFFSET', 'Repeat with Offset', '', '', 3),
                     ('MIRROR', 'Mirrored', '', '', 4)]

    cycle_before: EnumProperty(
        items=cycle_options,
        name='Before',
        default='NONE'
    )

    cycle_after: EnumProperty(
        items=cycle_options,
        name='Before',
        default='NONE'
    )


class AnimSlider(PropertyGroup):

    use_markers: BoolProperty(default=True,
                              description='use markers for the reference frames')

    affect_non_selected_fcurves: BoolProperty(default=True,
                                              description='Affect non-selected fcurves')

    affect_non_selected_keys: BoolProperty(default=False,
                                           description='Affect non-selected keys when cursor is over them')

    min_value: FloatProperty(default=-1)

    max_value: FloatProperty(default=1)

    index: IntProperty(default=-1)

    modal_switch: BoolProperty()

    noise_phase: IntProperty(default=1,
                             min=1,
                             max=10,
                             description='Change noise shape')

    slope: FloatProperty(default=2.0,
                         min=1.0,
                         max=10.0,
                         description='Determine how sharp the trasition is')

    overshoot: BoolProperty(update=update_overshoot,
                            description='Allows for higher values')

    left_ref_frame: IntProperty()

    right_ref_frame: IntProperty()

    selector: EnumProperty(
        items=[('EASE_TO_EASE', names['EASE_TO_EASE'], 'S shape transition', icons['EASE_TO_EASE'], 1),
               ('EASE', names['EASE'], 'C shape transition', icons['EASE'], 2),
               ('BLEND_EASE', names['BLEND_EASE'], 'From current to C shape', icons['BLEND_EASE'], 3),
               ('BLEND_NEIGHBOR', names['BLEND_NEIGHBOR'], 'From current to neighbors', icons['BLEND_NEIGHBOR'], 4),
               ('BLEND_FRAME', names['BLEND_FRAME'], 'From current to set frames', icons['BLEND_FRAME'], 5),
               ('BLEND_OFFSET', names['BLEND_OFFSET'], 'Offset key values to neighbors', icons['BLEND_OFFSET'], 6),
               ('PUSH_PULL', names['PUSH_PULL'], 'Overshoots key values', icons['PUSH_PULL'], 7),
               ('SCALE_AVERAGE', names['SCALE_AVERAGE'], 'Scale to average value', icons['SCALE_AVERAGE'], 8),
               ('SCALE_LEFT', names['SCALE_LEFT'], 'Scale anchor to left neighbor', icons['SCALE_LEFT'], 9),
               ('SCALE_RIGHT', names['SCALE_RIGHT'], 'Scale anchor to right neighbor', icons['SCALE_RIGHT'], 10),
               ('SMOOTH', names['SMOOTH'], 'Smooths out fcurve keys', icons['SMOOTH'], 11),
               ('NOISE', names['NOISE'], 'add random values to keys', icons['NOISE'], 12),
               ('TIME_OFFSET', names['TIME_OFFSET'], 'Slide fcurve in time without afecting keys frame value', icons['TIME_OFFSET'], 13),
               ('TWEEN', names['TWEEN'], 'Sets key value using neighbors as reference', icons['TWEEN'], 14)],
        name="Ease Slider Selector",
        default='EASE_TO_EASE',
        update=update_selector
    )

    factor: FloatProperty(default=0.0,
                          min=-1.0,
                          max=1.0
                          )

    factor_overshoot: FloatProperty(default=0.0,
                                    min=-2.0,
                                    max=2.0
                                    )


class AnimAideScene(PropertyGroup):
    anim_transform: PointerProperty(type=AnimAideAnimTransform)
    clone: PointerProperty(type=AnimAideClone)
    slider: PointerProperty(type=AnimSlider)
    slider_slots: CollectionProperty(type=AnimSlider)


def set_props():
    # to be used when registering

    bpy.types.Scene.animaide = PointerProperty(type=AnimAideScene)
    # bpy.types.Object.animaide = PointerProperty(type=AnimAideObject)


def del_props():
    # to be used when unregistreing

    del bpy.types.Scene.animaide


classes = (
    AnimAideAnimTransform,
    AnimAideClone,
    AnimSlider,
    AnimAideScene,
)
