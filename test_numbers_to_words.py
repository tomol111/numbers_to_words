from numbers_to_words import (
    convert_number,
    disassemble_group,
    generate_words_for_group,
    GrammaticalCases,
    split_to_groups,
)

import pytest


@pytest.mark.parametrize("number, text", [
    (0, "zero"),
    (35_302, "trzydzieści pięć tysięcy trzysta dwa"),
    (2*10**75 + 1, "dwa duodecyliardy jeden"),
])
def test_should_convert_number_to_text(number, text):
    assert convert_number(number) == text


@pytest.mark.parametrize("number, text", [
    (0, "zero metrów"),
    (1, "jeden metr"),
    (3, "trzy metry"),
    (5, "pięć metrów"),
    (12, "dwanaście metrów"),
    (1_000, "tysiąc metrów"),
    (1_001, "tysiąc jeden metrów"),
    (35_302, "trzydzieści pięć tysięcy trzysta dwa metry"),
])
def test_should_convert_number_with_unit_to_text(number, text):
    unit = GrammaticalCases("metr", "metry", "metrów")
    assert convert_number(number, unit) == text


@pytest.mark.parametrize("elements, text", [
    ([1], "jeden"),
    ([20, 1], "dwadzieścia jeden"),
    ([100, 4], "sto cztery"),
    ([800, 70], "osiemset siedemdziesiąt"),
    ([300, 12], "trzysta dwanaście"),
    ([400, 50, 6], "czterysta pięćdziesiąt sześć"),
])
def test_should_generate_words_for_group_elements(elements, text):
    assert generate_words_for_group(elements) == text.split()


@pytest.mark.parametrize("elements, text", [
    ([1], "tysiąc"),
    ([3], "trzy tysiące"),
    ([5], "pięć tysięcy"),
    ([20, 1], "dwadzieścia jeden tysięcy"),
    ([100, 4], "sto cztery tysiące"),
    ([800, 70], "osiemset siedemdziesiąt tysięcy"),
    ([300, 12], "trzysta dwanaście tysięcy"),
    ([400, 50, 6], "czterysta pięćdziesiąt sześć tysięcy"),
])
def test_should_generate_words_for_group_elements_with_extra_word(elements, text):
    extra = GrammaticalCases("tysiąc", "tysiące", "tysięcy")
    assert generate_words_for_group(elements, extra) == text.split()


@pytest.mark.parametrize("number, elements", [
    (0, []),
    (3, [3]),
    (206, [206]),
    (1_390, [1, 390]),
    (103_390, [103, 390]),
    (200_000, [200, 0]),
    (3_040_000, [3, 40, 0]),
])
def test_should_split_number_to_groups(number, elements):
    assert split_to_groups(number) == elements


@pytest.mark.parametrize("number, elements", [
    (2, [2]),
    (30, [30]),
    (36, [30, 6]),
    (11, [11]),
    (100, [100]),
    (102, [100, 2]),
    (270, [200, 70]),
    (853, [800, 50, 3]),
    (212, [200, 12]),
])
def test_should_disasemble_group(number, elements):
    assert disassemble_group(number) == elements
