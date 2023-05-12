from gendiff.scripts.gendiff import file_to_collection
from gendiff.scripts.gendiff import generate_diff
from gendiff.lib.funcs import get_extension
from gendiff.lib.funcs import get_unique_keys
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
def dict11():
    with open('tests/fixtures/recursive/file1.json') as src:
        dict11 = json.load(src)
    return dict11


@pytest.fixture
def dict12():
    with open('tests/fixtures/recursive/file2.json') as src:
        dict12 = json.load(src)
    return dict12


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
def diff_expected_recursive_output():
    with open('tests/fixtures/recursive/recursive_expected_result.txt') as src:
        exp_result = src.read()
    return exp_result


@pytest.fixture
def files():
    return ('tests/fixtures/file1.json',
            'tests/fixtures/file2.json',
            'tests/fixtures/file3.yaml',
            'tests/fixtures/file4.yaml',
            'tests/fixtures/recursive/file1.json',
            'tests/fixtures/recursive/file2.json')


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


@pytest.fixture
def plain_probe():
    filename = 'tests/fixtures/recursive/recursive_expected_result_plain.txt'
    with open(filename) as src:
        probe = src.read()
    return probe


@pytest.fixture
def recursive_files():
    file1 = 'tests/fixtures/recursive/file1.json'
    file2 = 'tests/fixtures/recursive/file2.json'
    return file1, file2


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


def test_get_unique_keys(dict1, dict2):
    assert get_unique_keys(dict1, dict2) == ['follow', 'host',
                                             'proxy', 'timeout', 'verbose']
    assert get_unique_keys(dict1, {}) == ['follow', 'host', 'proxy', 'timeout']
    assert get_unique_keys({}, {}) == []


def test_generate_diff(files, diff_expected_output,
                       diff_expected_recursive_output,
                       plain_probe):
    file1, file2, file3, file4, file11, file12 = files
    assert generate_diff(file1, file2) == diff_expected_output
    assert generate_diff(file3, file4) == diff_expected_output
    assert generate_diff(file11, file12) == diff_expected_recursive_output
    assert generate_diff(file11, file12, 'plain') == plain_probe
