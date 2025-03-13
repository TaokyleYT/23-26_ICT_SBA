import pytest
from helpers import *


@pytest.mark.parametrize("instance, _type, expected", [
    (10, int, True),  # Integer type
    ("hello", str, True),  # String type
    (3.14, float, True),  # Float type
    ([1, 2, 3], list, True),  # List type
    ((1, 2, 3), tuple, True),  # Tuple type
    ({"a": 1, "b": 2}, dict, True),  # Dictionary type
    (10, str, False),  # Type mismatch
    ("hello", int, False),  # Type mismatch
    ([1, 2, "3"], list[int], False),  # Generic type mismatch
    ((1, 2, "3"), tuple[int, int, int], False),  # Tuple element type mismatch
    (10, int | str, True),  # Union type match (int)
    ("hello", int | str, True),  # Union type match (str)
    (3.14, int | str, False),  # Union type mismatch
    ([1, 2, 3], list[int], True),  # Generic type match
    ([1, 2, "3"], list[int], False),  # Generic type mismatch
    ((1, 2, 3), tuple[int, int, int], True),  # Tuple type match
    ((1, "2", 3), tuple[int, str, int], True),  # Tuple with mixed types
    ((1, 2, "3"), tuple[int, int, int], False),  # Tuple type mismatch
])
def test_type_check(instance, _type, expected):

    # Act
    result = type_check(instance, _type)

    # Assert
    assert result == expected

@pytest.mark.parametrize("instance, _type", [
    (10, "int"),  # Invalid _type (string)
    ("hello", 10),  # Invalid _type (integer)
    (3.14, [float]),  # Invalid _type (list)
])
def test_type_check_invalid_type(instance, _type):
    with pytest.raises(TypeError):
        type_check(instance, _type)


@pytest.mark.parametrize("input_list, ascending, expected_output, test_id", [
    ([5, 2, 8, 1, 9, 4], True, [1, 2, 4, 5, 8, 9], "ascending_basic"),
    ([5, 2, 8, 1, 9, 4], False, [9, 8, 5, 4, 2, 1], "descending_basic"),
    ([1, 2, 3, 4, 5], True, [1, 2, 3, 4, 5], "already_ascending"),
    ([5, 4, 3, 2, 1], False, [5, 4, 3, 2, 1], "already_descending"),
    ([], True, [], "empty_list"),
    ([1], True, [1], "single_element"),
    ([1, 1, 1, 1], True, [1, 1, 1, 1], "duplicate_elements"),
    ([5, 2, 8, 1, 9, 4, -3, 0, 10], True, [-3, 0, 1, 2, 4, 5, 8, 9, 10], "negative_and_positive"),
])
def test_quick_sort(input_list, ascending, expected_output, test_id):

    # Act
    sorted_list = quick_sort(input_list, ascending)

    # Assert
    assert sorted_list == expected_output




@pytest.mark.parametrize("input_list, value, start, stop, expected_output, test_id", [
    ([1, 2, 3, 4, 5], 3, 0, 5, 2, "middle_element"),
    ([1, 2, 3, 4, 5], 1, 0, 5, 0, "first_element"),
    ([1, 2, 3, 4, 5], 5, 0, 5, 4, "last_element"),
    ([1, 2, 3, 4, 5], 0, 0, 5, -1, "element_not_present"),
    ([1, 2, 3, 4, 5], 6, 0, 5, -1, "element_greater_than_all"),
    ([1, 3, 5, 7, 9], 4, 0, 5, -1, "element_between_elements"),
    ([], 3, 0, 0, -1, "empty_list"),
    ([1], 1, 0, 1, 0, "single_element_list_present"),
    ([1], 2, 0, 1, -1, "single_element_list_not_present"),
    ([1, 1, 1, 1, 1], 1, 0, 5, 0, "duplicate_elements"),
    ([1, 2, 3, 4, 5], 3, 1, 4, 2, "start_and_stop_within_range"),
    ([1, 2, 3, 4, 5], 3, 3, 5, -1, "start_after_element"),
    ([1, 2, 3, 4, 5], 3, 0, 2, -1, "stop_before_element"),
    ([1, 2, 3, 4, 5], 3, 0, 10, 2, "stop_beyond_list_length"),
])
def test_linear_search(input_list, value, start, stop, expected_output, test_id):

    # Act
    index = linear_search(input_list, value, start, stop)

    # Assert
    assert index == expected_output


"""
@pytest.mark.parametrize("text, sep, expected_output, test_id", [
    ("hello world", " ", ["hello", "world"], "basic_split"),
    ("hello world", "", ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd'], "empty_separator"),
    ("hello world", [" "], ["hello", "world"], "list_separator"),
    ("hello world", (" ",), ["hello", "world"], "tuple_separator"),
    ("hello world", "o", ["hell", " w", "rld"], "character_separator"),
    ("hello world", "world", ["hello "], "word_separator"),
    ("hello world", "abc", ["hello world"], "separator_not_found"),
    ("", " ", [""], "empty_string"),
    ("hello world", [" ", "w"], ["hello", "orld"], "multiple_separators"),
    ("hello world", (" ", "w"), ["hello", "orld"], "multiple_separators_tuple"),
    ("hello world", ["o", "w"], ["hell", " ", "rld"], "multiple_separators_overlap"),
    ("hello world", ("o", "w"), ["hell", " ", "rld"], "multiple_separators_overlap_tuple"),
])
def test_split_exclude_ANSI(text, sep, expected_output, test_id):

    # Act
    result = split_exclude_ANSI(text, sep)

    # Assert
    assert result == expected_output

"""

@pytest.mark.parametrize("args, expected_output, test_id", [
    ([1, 2, 3, 4, 5], 5, "basic_max"),
    ([5, 4, 3, 2, 1], 5, "reverse_order"),
    ([1, 5, 2, 4, 3], 5, "mixed_order"),
    ([5, 5, 5, 5, 5], 5, "all_same"),
    ([-1, -2, -3, -4, -5], -1, "negative_numbers"),
    ([1.1, 2.2, 3.3, 4.4, 5.5], 5.5, "float_numbers"),
    ([1, 2, 3, 4, 5], 5, "integer_numbers"),
    ([5], 5, "single_element"),
    ((1, 2, 3, 4, 5), 5, "tuple_input"),
    ({1, 2, 3, 4, 5}, 5, "set_input"),
])
def test_max(args, expected_output, test_id):

    # Act
    result = max(*args)

    # Assert
    assert result == expected_output

@pytest.mark.parametrize("args, expected_output, test_id", [
    ([1, 2, 3, 4, 5], 1, "basic_min"),
    ([5, 4, 3, 2, 1], 1, "reverse_order"),
    ([1, 5, 2, 4, 3], 1, "mixed_order"),
    ([5, 5, 5, 5, 5], 5, "all_same"),
    ([-1, -2, -3, -4, -5], -5, "negative_numbers"),
    ([1.1, 2.2, 3.3, 4.4, 5.5], 1.1, "float_numbers"),
    ([1, 2, 3, 4, 5], 1, "integer_numbers"),
    ([5], 5, "single_element"),
    ((1, 2, 3, 4, 5), 1, "tuple_input"),
    ({1, 2, 3, 4, 5}, 1, "set_input"),
])
def test_min(args, expected_output, test_id):

    # Act
    result = min(*args)

    # Assert
    assert result == expected_output

@pytest.mark.parametrize("args, expected_output, test_id", [
    ([True, True, True], True, "all_true"),
    ([True, False, True], False, "one_false"),
    ([False, False, False], False, "all_false"),
    ([1, 2, 3, 4, 5], True, "all_positive_integers"),
    ([0, 1, 2, 3, 4], False, "one_zero"),
    ([-1, -2, -3, -4, -5], True, "all_negative_integers"),
    ([1.1, 2.2, 3.3, 4.4, 5.5], True, "all_positive_floats"),
    ([0.0, 1.1, 2.2, 3.3, 4.4], False, "one_zero_float"),
    (["a", "b", "c"], True, "all_non_empty_strings"),
    (["", "a", "b"], False, "one_empty_string"),
    ([True], True, "single_true"),
    ([False], False, "single_false"),
    ([], True, "empty_iterable"),
    ((True, True, True), True, "tuple_input"),
    ({True, True, True}, True, "set_input"),
])
def test_all(args, expected_output, test_id):

    # Act
    result = all(*args)

    # Assert
    assert result == expected_output

@pytest.mark.parametrize("args, expected_output, test_id", [
    ([True, True, True], True, "all_true"),
    ([True, False, True], True, "one_false"),
    ([False, False, False], False, "all_false"),
    ([1, 2, 3, 4, 5], True, "all_positive_integers"),
    ([0, 1, 2, 3, 4], True, "one_zero"),
    ([-1, -2, -3, -4, -5], True, "all_negative_integers"),
    ([1.1, 2.2, 3.3, 4.4, 5.5], True, "all_positive_floats"),
    ([0.0, 1.1, 2.2, 3.3, 4.4], True, "one_zero_float"),
    (["a", "b", "c"], True, "all_non_empty_strings"),
    (["", "a", "b"], True, "one_empty_string"),
    ([True], True, "single_true"),
    ([False], False, "single_false"),
    ([], False, "empty_iterable"),
    ((True, True, True), True, "tuple_input"),
    ({True, True, True}, True, "set_input"),
])
def test_any(args, expected_output, test_id):

    # Act
    result = any(*args)

    # Assert
    assert result == expected_output
