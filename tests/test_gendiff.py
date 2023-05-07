from gendiff.scripts.gendiff import check_key_in_dicts
import pytest
import json


@pytest.fixture
def dict1():
    with open('tests/fixtures/file1.json') as src:
        dict1 = json.load(src)
    return dict1


@pytest.fixture
def dict2():
    with open('tests/fixtures/file2.json') as src:
        dict2 = json.load(src)
    return dict2


@pytest.fixture
def keys():
    with open('tests/fixtures/file1.json') as src:
        dict1 = json.load(src)
    with open('tests/fixtures/file2.json') as src:
        dict2 = json.load(src)
    key_list = list(sorted(set(list(dict1.keys()) + list(dict2.keys()))))
    return key_list


def test_check_key_in_dicts(keys, dict1, dict2):
    key0, key1, key2, key3, key4 = keys
    assert check_key_in_dicts(key0, dict1, dict2) == ('- follow', False)
    assert check_key_in_dicts(key1, dict1, dict2) == ('  host', 'hexlet.io')
    assert check_key_in_dicts(key2, dict1, dict2) == ('- proxy',
                                                      '123.234.53.22')
    assert check_key_in_dicts(key3, dict1, dict2) == ('  timeout',
                                                      ('- timeout', 50,
                                                       '+ timeout', 20))
    assert check_key_in_dicts(key4, dict1, dict2) == ('+ verbose', True)
