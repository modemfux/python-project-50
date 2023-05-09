import json
import yaml
import os


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


def get_unique_keys(dict1, dict2):
    return list(sorted(set(list(dict1.keys()) + list(dict2.keys()))))


def get_new_kv_pairs(key, dict1, dict2):
    key0 = key
    key1 = '- ' + key
    key2 = '+ ' + key

    value1 = dict1.get(key)
    value2 = dict2.get(key)

    if all([key in dict1, key in dict2]):
        if value1 == value2:
            return ((key0, value1),)
        elif all([isinstance(value1, dict), isinstance(value2, dict)]):
            return ((key0, difference_gen(value1, value2)),)
        else:
            return ((key1, value1), (key2, value2))
    elif key in dict1:
        return ((key1, value1), )
    else:
        return ((key2, value2), )


def difference_gen(dict1, dict2):
    resulting_dict = {}
    keys_list = get_unique_keys(dict1, dict2)
    for key in keys_list:
        pairs = get_new_kv_pairs(key, dict1, dict2)
        for pair in pairs:
            new_key, value = pair
            resulting_dict[new_key] = value
    return resulting_dict


def stylish(dict0):
    string = json.dumps(dict0, indent=4)
    result = ''
    for line in string.split('\n'):
        line = line.replace('"', '')
        for end_sign in [',', ' ']:
            while line.endswith(end_sign):
                line = line[:-1]
        line = line.replace('  +', '+')
        line = line.replace('  -', '-')
        line += '\n'
        result += line
    return result[:-1]


def generate_diff(file1, file2, formatter=stylish):
    dict1 = file_to_collection(file1)
    dict2 = file_to_collection(file2)
    result_dict = difference_gen(dict1, dict2)
    return formatter(result_dict)
