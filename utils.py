import bpy


def gradual(key_y, target_y, delta=1.0, factor=0.15):
    """
    Gradualy transition the value of key_y to target_y
    :param key_y: value "y" of the afected key
    :param target_y: neighbor key from where is taking the destination "y" value
    :param delta: relationship of the distance between the afected key and the neighbors
    :param factor: Value from 0 to 1
    :return: new "y" value of the afected key
    """
    print('source: ', key_y)
    print('target: ', target_y)
    print('factor: ', factor)
    step = abs(key_y - target_y) * (delta * factor)
    print('gap: ', key_y - target_y)
    print('step: ', step)

    if target_y > key_y:
        return key_y + step

    else:
        return key_y - step


def clamp(value, minimum, maximum, to_none=False):
    """
    Take a value and if it goes beyond the minimum and maximum it would replace it with those.
    :param value: number to check
    :param minimum: top possible value
    :param maximum: lower possible value
    :param to_none: if True then it would return None if the value goe beyond the minimum and maximum
    :return: clamped value
    """

    if value < minimum:
        if to_none is True:
            return None
        else:
            return minimum

    if value > maximum:
        if to_none is True:
            return None
        else:
            return maximum

    return value


def floor(value, minimum, to_none=False):
    """
    Take the value and if it goes lower than the minimum it would replace it with it
    :param value: number to check
    :param minimum: lower possible value
    :param to_none: if True then it would return None if the value goes lower than the minimum
    :return: clamped value
    """
    if value < minimum:
        if to_none is True:
            return None
        else:
            return minimum

    return value


def ceiling(value, maximum, to_none=False):
    """
    Take the value and if it goes over the maximum it would replace it with it
    :param value: number to check
    :param maximum: higher possible value
    :param to_none: if True then it would return None if the value goes higher than the maximum
    :return: clamped value
    """
    if value > maximum:
        if to_none is True:
            return None
        else:
            return maximum

    return value


def toggle(to_toggle, value_a, value_b):
    """
    Change "to_toggle" to one of the tow values it doesn't have at the moment
    :param to_toggle: parameter to be afected
    :param value_a: option 1
    :param value_b: option 2
    :return: one of the options (the one it doesn't have at the moment
    """
    if to_toggle == value_a:
        return value_b
    elif to_toggle == value_b:
        return value_a


def update_keyframe_points(context):
    """# The select operator(s) are bugged, and can fail to update selected keys(irmitya)"""
    area = context.area.type
    if area != 'GRAPH_EDITOR':
        context.area.type = 'GRAPH_EDITOR'

    bpy.ops.transform.transform()

    if area != 'GRAPH_EDITOR':
        context.area.type = area
