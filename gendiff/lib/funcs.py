import os
import json
import yaml


def get_unique_keys(dict1, dict2):
    return list(sorted(set(list(dict1.keys()) + list(dict2.keys()))))


def get_new_kv_pairs(key, dict1, dict2):

    value1 = dict1.get(key)
    value2 = dict2.get(key)

    pairs_dict = {'state': None, 'value': None}

    if all([key in dict1, key in dict2]):
        if value1 == value2:
            pairs_dict['state'] = 'keep'
            pairs_dict['value'] = value1
        elif all([isinstance(value1, dict), isinstance(value2, dict)]):
            pairs_dict['state'] = 'inner'
            pairs_dict['value'] = difference_gen(value1, value2)
        else:
            pairs_dict['state'] = 'swap'
            pairs_dict['value'] = (value1, value2)
    elif key in dict1:
        pairs_dict['state'] = 'remove'
        pairs_dict['value'] = (value1)
    else:
        pairs_dict['state'] = 'add'
        pairs_dict['value'] = (value2)
    return pairs_dict


def difference_gen(dict1, dict2):
    resulting_dict = {}
    keys_list = get_unique_keys(dict1, dict2)
    for key in keys_list:
        resulting_dict[key] = get_new_kv_pairs(key, dict1, dict2)
    return resulting_dict


def get_extension(name):
    return name.split('.')[-1] if '.' in name else None


def file_to_collection(file):
    actions = {
        'json': json.load,
        'yml': yaml.safe_load,
        'yaml': yaml.safe_load
        }
    if not os.path.exists(file):
        path, name = os.path.split(file)
        raise Exception(f'There is no such file as "{name}" in "{path}"')
    else:
        ext = get_extension(file)
        with open(file) as src:
            return actions[ext](src) if actions.get(ext) else src.read()
