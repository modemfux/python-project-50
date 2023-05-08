from gendiff.scripts.gendiff import generate_diff
from gendiff.scripts.gendiff import check_key_in_dicts
from gendiff.scripts.gendiff import get_extension
from gendiff.scripts.gendiff import file_to_collection
import yaml
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
def dict3():
    with open('tests/fixtures/file3.yaml') as src:
        dict3 = yaml.safe_load(src)
    return dict3


@pytest.fixture
def dict4():
    with open('tests/fixtures/file4.yaml') as src:
        dict4 = yaml.safe_load(src)
    return dict4


@pytest.fixture
def dict5():
    with open('tests/fixtures/file5.yml') as src:
        dict5 = yaml.safe_load(src)
    return dict5


@pytest.fixture
def keys():
    with open('tests/fixtures/file1.json') as src:
        dict1 = json.load(src)
    with open('tests/fixtures/file2.json') as src:
        dict2 = json.load(src)
    key_list = list(sorted(set(list(dict1.keys()) + list(dict2.keys()))))
    return key_list


@pytest.fixture
def diff_expected_output():
    with open('tests/fixtures/expected_output.txt') as src:
        exp_result = src.read()
    return exp_result


@pytest.fixture
def files():
    return ('tests/fixtures/file1.json',
            'tests/fixtures/file2.json',
            'tests/fixtures/file3.yaml',
            'tests/fixtures/file4.yaml')


@pytest.fixture
def get_extensions_probe():
    return (['test01.txt', 'test.with.many.dots.json', 'test_without_dots'],
            ['txt', 'json', None])


@pytest.fixture
def file_to_collection_probe():
    return ('tests/fixtures/file1.json',
            'tests/fixtures/file2.json',
            'tests/fixtures/file3.yaml',
            'tests/fixtures/file4.yaml',
            'tests/fixtures/file5.yml')


def test_get_extension(get_extensions_probe):
    files, exts = get_extensions_probe
    result_list = list(map(get_extension, files))
    assert result_list == exts


def test_file_to_collection(
        diff_expected_output,
        file_to_collection_probe,
        dict1,
        dict2,
        dict3,
        dict4,
        dict5):
    txt = 'tests/fixtures/expected_output.txt'
    assert file_to_collection(txt) == diff_expected_output
    pairs = list(zip(
        file_to_collection_probe, [dict1, dict2, dict3, dict4, dict5]))
    for filename, result in pairs:
        assert file_to_collection(filename) == result
    with pytest.raises(Exception):
        file_to_collection('')


def test_check_key_in_dicts(keys, dict1, dict2):
    key0, key1, key2, key3, key4 = keys
    assert check_key_in_dicts(key0, dict1, dict2) == ('- follow', False)
    assert check_key_in_dicts(key1, dict1, dict2) == ('  host', 'hexlet.io')
    assert check_key_in_dicts(key2, dict1, dict2) == ('- proxy',
                                                      '123.234.53.22')
    assert check_key_in_dicts(key3, dict1, dict2) == ('- timeout', 50,
                                                      '+ timeout', 20)
    assert check_key_in_dicts(key4, dict1, dict2) == ('+ verbose', True)


def test_generate_diff(files, diff_expected_output):
    file1, file2, file3, file4 = files
    assert generate_diff(file1, file2) == diff_expected_output
    assert generate_diff(file3, file4) == diff_expected_output
