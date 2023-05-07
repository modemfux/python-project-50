import json


def check_key_in_dicts(key, dict1, dict2):
    key0 = '  ' + key
    key1 = '- ' + key
    key2 = '+ ' + key
    if key in dict1 and key in dict2 and dict1[key] == dict2[key]:
        return key0, dict1[key]
    elif key in dict1 and key in dict2 and dict1[key] != dict2[key]:
        return (key1, dict1[key], key2, dict2[key])
    elif key in dict1 and key not in dict2:
        return key1, dict1.get(key)
    elif key in dict2 and key not in dict1:
        return key2, dict2.get(key)


def generate_diff(file1, file2):
    with open(file1) as src:
        item1 = json.load(src)
    with open(file2) as src:
        item2 = json.load(src)
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
