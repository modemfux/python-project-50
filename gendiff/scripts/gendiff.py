import os
import json
import yaml


def check_key_in_dicts(key, dict1, dict2):
    keys = {
        '0': '  ' + key,
        '1': '- ' + key,
        '2': '+ ' + key
        }
    if key in dict1.keys() and key in dict2.keys():
        return (keys['0'], dict1[key]) if dict1[key] == dict2[key] else (
            keys['1'], dict1[key], keys['2'], dict2[key])
    elif key in dict1.keys() and key not in dict2.keys():
        return keys['1'], dict1.get(key)
    elif key in dict2.keys() and key not in dict1.keys():
        return keys['2'], dict2.get(key)


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


def generate_diff(file1, file2):
    item1 = file_to_collection(file1)
    item2 = file_to_collection(file2)
    all_keys = list(sorted(set(item1.keys()) | set(item2.keys())))
    new_dict = {}
    for key in all_keys:
        mid_res = check_key_in_dicts(key, item1, item2)
        if len(mid_res) == 2:
            n_key, n_value = mid_res
            new_dict[n_key] = n_value
        else:
            n_key1, n_value1, n_key2, n_value2 = mid_res
            new_dict[n_key1] = n_value1
            new_dict[n_key2] = n_value2
    return json.dumps(new_dict, indent=4).replace('"', '')
