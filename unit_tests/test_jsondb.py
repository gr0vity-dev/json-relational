import pytest
from json_relational.src.main import JsonRelational


@pytest.mark.parametrize("test_id", range(1, 6))
def test_flatten_lines(test_id):
    jr = JsonRelational()

    sample_json_lines = jr.read_text(
        f'unit_tests/data/{test_id}_data.txt')
    expected_result = jr.read_json(
        f'unit_tests/data/{test_id}_expected.json')
    actual_result = JsonRelational().flatten_lines(sample_json_lines)
    assert actual_result == expected_result


def test_flatten_lines_6():
    jr = JsonRelational()

    sample_json_lines = jr.read_text('unit_tests/data/6_data.txt')
    expected_result = jr.read_json('unit_tests/data/6_expected.json')

    jr.add_key_mappings({"entry": "entries"})
    actual_result = jr.flatten_lines(sample_json_lines)
    assert actual_result == expected_result


def test_flatten_lines_7():  # use flatten_lines
    jr = JsonRelational()

    sample_json_lines = jr.read_json('unit_tests/data/7_data.json')
    expected_result = jr.read_json('unit_tests/data/7_expected.json')

    actual_tables = jr.flatten_lines([sample_json_lines], is_json=True)
    assert actual_tables == expected_result


def test_flatten_lines_7_2():  # use flatten_json
    jr = JsonRelational()

    sample_json_lines = jr.read_json('unit_tests/data/7_data.json')
    expected_result = jr.read_json('unit_tests/data/7_expected.json')

    actual_tables = jr.flatten_json(sample_json_lines)
    assert actual_tables == expected_result


def test_flatten_lines_8():
    jr = JsonRelational()

    sample_json_lines = jr.read_json('unit_tests/data/8_data_json_array.json')
    expected_result = jr.read_json('unit_tests/data/8_expected.json')

    jr.add_key_mappings({"entry": "entries"})
    actual_result = jr.flatten_lines(sample_json_lines, is_json=True)
    assert actual_result == expected_result


def test_flatten_lines_9():
    # use actual json without reading
    jr = JsonRelational()

    sample_json_lines = [
        {"type": "employee", "id": 1, "entries": [
            {"hash": "X"}, {"hash": "Y"}, {"hash": "Z"}]},
        {"type": "else", "entry": {"hash": "X"}},
        {"type": "else", "entry": {"hash": "A"}}
    ]
    expected_result = jr.read_json('unit_tests/data/8_expected.json')

    jr.add_key_mappings({"entry": "entries"})
    actual_result = jr.flatten_lines(sample_json_lines, is_json=True)
    assert actual_result == expected_result
