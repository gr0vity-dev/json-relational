import pytest
from json_relational.src.main import JsonRelational
import json


def read_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def read_lines(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()


def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


@pytest.mark.parametrize("test_id", range(1, 6))
def test_flatten_lines(test_id):
    sample_json_lines = read_text(f'unit_tests/data/{test_id}_data.txt')
    expected_result = read_json(f'unit_tests/data/{test_id}_expected.json')
    actual_result = JsonRelational().flatten_lines(sample_json_lines)
    assert actual_result == expected_result


def test_flatten_lines_6():
    sample_json_lines = read_text(f'unit_tests/data/6_data.txt')
    expected_result = read_json(f'unit_tests/data/6_expected.json')

    flattener = JsonRelational()
    flattener.add_key_mappings({"entry": "entries"})

    actual_result = flattener.flatten_lines(sample_json_lines)
    assert actual_result == expected_result


def test_flatten_lines_7():
    sample_json_lines = read_json(f'unit_tests/data/7_data.json')
    expected_result = read_json(f'unit_tests/data/7_expected.json')
    flattener = JsonRelational()
    actual_tables = flattener.flatten_lines([sample_json_lines], is_json=True)
    assert actual_tables == expected_result
