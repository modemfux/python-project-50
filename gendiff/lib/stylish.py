import json


def diffed_for_stylish(diffed_dict):
    result_dict = {}
    for key, value in diffed_dict.items():
        state = value['state']
        rem_key = '- ' + str(key)
        add_key = '+ ' + str(key)
        match state:
            case 'keep':
                result_dict[key] = value['value']
            case 'remove':
                result_dict[rem_key] = value['value']
            case 'add':
                result_dict[add_key] = value['value']
            case 'swap':
                rem_val, add_val = value['value']
                result_dict[rem_key] = rem_val
                result_dict[add_key] = add_val
            case 'inner':
                result_dict[key] = diffed_for_stylish(value['value'])
    return result_dict


def stylish(diffed_dict):
    normalized_dict = diffed_for_stylish(diffed_dict)
    string = json.dumps(normalized_dict, indent=4)
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
