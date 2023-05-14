from gendiff.lib.stylish import diffed_for_stylish
import json


def json_like(diffed_dict):
    working_dict = diffed_for_stylish(diffed_dict)
    return json.dumps(working_dict, indent=4)
