from gendiff.lib.funcs import file_to_collection
from gendiff.lib.funcs import difference_gen
from gendiff.lib.stylish import stylish
from gendiff.lib.plain import plain
from gendiff.lib.json_like import json_like


def generate_diff(file1, file2, formatter='stylish'):
    formatter_dict = {'stylish': stylish, 'plain': plain, 'json': json_like}
    formatter_func = formatter_dict[formatter]
    dict1 = file_to_collection(file1)
    dict2 = file_to_collection(file2)
    result_dict = difference_gen(dict1, dict2)
    return formatter_func(result_dict)
