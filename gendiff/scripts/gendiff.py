from gendiff.lib.funcs import file_to_collection
from gendiff.lib.funcs import difference_gen
from gendiff.lib.stylish import stylish


def generate_diff(file1, file2, formatter=stylish):
    dict1 = file_to_collection(file1)
    dict2 = file_to_collection(file2)
    result_dict = difference_gen(dict1, dict2)
    return formatter(result_dict)
