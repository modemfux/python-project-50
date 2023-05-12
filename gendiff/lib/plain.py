def normalize_value_for_plain(value):
    if isinstance(value, (dict, set, list, tuple)):
        return '[complex value]'
    elif isinstance(value, str):
        return "'" + value + "'"
    else:
        return value


def get_string_for_normalize(state, value, accum):
    match state:
        case 'keep':
            pass
        case 'remove':
            result = f'Property \'{accum}\' was removed\n'
        case 'add':
            value = normalize_value_for_plain(value)
            result = f'Property \'{accum}\' was added with value: {value}\n'
        case 'swap':
            old = normalize_value_for_plain(value[0])
            new = normalize_value_for_plain(value[1])
            result = f'Property \'{accum}\' was updated. From {old} to {new}\n'
    normalizing_dict = {'False': 'false',
                        'None': 'null',
                        'True': 'true'}
    for key, value in normalizing_dict.items():
        result = result.replace(key, value)
    return result


def plain(diffed_dict, accumulator=''):
    result_text = ''
    for key, value in diffed_dict.items():
        state = value['state']
        end_value = value['value']
        new_accum = '.'.join((accumulator, key))
        if new_accum.startswith('.'):
            new_accum = new_accum[1:]
        match state:
            case 'inner':
                result_text += plain(end_value, new_accum)
            case 'keep':
                pass
            case _:
                result_text += get_string_for_normalize(state,
                                                        end_value,
                                                        new_accum)
    return result_text
