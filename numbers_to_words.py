from typing import Mapping, NamedTuple, Final


NUMBERS_DICT: Final[Mapping[int, str]] = {
    0: "zero",
    1: "jeden",
    2: "dwa",
    3: "trzy",
    4: "cztery",
    5: "pięć",
    6: "sześć",
    7: "siedem",
    8: "osiem",
    9: "dziewięć",

    10: "dziesięć",
    11: "jedenaście",
    12: "dwanaście",
    13: "trzynaście",
    14: "czternaście",
    15: "piętnaście",
    16: "szesnaście",
    17: "siedemnaście",
    18: "osiemnaście",
    19: "dziewiętnaście",

    20: "dwadzieścia",
    30: "trzydzieści",
    40: "czterdzieści",
    50: "pięćdziesiąt",
    60: "sześćdziesiąt",
    70: "siedemdziesiąt",
    80: "osiemdziesiąt",
    90: "dziewięćdziesiąt",

    100: "sto",
    200: "dwieście",
    300: "trzysta",
    400: "czterysta",
    500: "pięćset",
    600: "sześćset",
    700: "siedemset",
    800: "osiemset",
    900: "dziewięćset",
}


class GrammaticalCases(NamedTuple):
    nominative_singular: str
    nominative_plural: str
    genitive_plural: str


GROUPS_EXTRAS: Final[tuple[GrammaticalCases | None, ...]] = (
    GrammaticalCases("duodecyliard", "duodecyliardy", "duodecyliardów"),
    GrammaticalCases("duodecylion", "duodecyliony", "duodecylionów"),
    GrammaticalCases("undecyliard", "undecyliardy", "undecyliardów"),
    GrammaticalCases("undecylion", "undecyliony", "undecylionów"),
    GrammaticalCases("decyliard", "decyliardy", "decyliardów"),
    GrammaticalCases("decylion", "decyliony", "decylionów"),
    GrammaticalCases("noniliard", "noniliardy", "noniliardów"),
    GrammaticalCases("nonilion", "noniliony", "nonilionów"),
    GrammaticalCases("oktyliard", "oktyliardy", "oktyliardów"),
    GrammaticalCases("oktylion", "oktyliony", "oktylionów"),
    GrammaticalCases("septyliard", "septyliardy", "septyliardów"),
    GrammaticalCases("septylion", "septyliony", "septylionów"),
    GrammaticalCases("sekstyliard", "sekstyliardy", "sekstyliardów"),
    GrammaticalCases("sekstylion", "sekstyliony", "sekstylionów"),
    GrammaticalCases("kwintyliard", "kwintyliardy", "kwintyliardów"),
    GrammaticalCases("kwintylion", "kwintyliony", "kwintylionów"),
    GrammaticalCases("kwadryliard", "kwadryliardy", "kwadryliardów"),
    GrammaticalCases("kwadrylion", "kwadryliony", "kwadryliardów"),
    GrammaticalCases("tryliard", "tryliardy", "tryliardów"),
    GrammaticalCases("trylion", "tryliony", "trylionów"),
    GrammaticalCases("biliard", "biliardy", "biliardów"),
    GrammaticalCases("bilion", "biliony", "bilionów"),
    GrammaticalCases("miliard", "miliardy", "miliardów"),
    GrammaticalCases("milion", "miliony", "milionów"),
    GrammaticalCases("tysiąc", "tysiące", "tysięcy"),
    None  # unity group
)


def convert_number(number: int, unit: GrammaticalCases | None = None) -> str:
    return " ".join(convert_number_to_words(number, unit))


def convert_number_to_words(
    number: int, unit: GrammaticalCases | None = None
) -> list[str]:
    words: list[str] = []

    if number == 0:
        groups = [[0]]
    else:
        groups = [disassemble_group(group) for group in split_to_groups(number)]

    for group, extra in zip(groups, GROUPS_EXTRAS[-len(groups):]):
        if group:
            words.extend(generate_words_for_group(group, extra))

    if unit:
        if number == 1:
            words.append(unit.nominative_singular)
        elif (unity_group := groups[-1]) and 2 <= unity_group[-1] <= 4:
            words.append(unit.nominative_plural)
        else:
            words.append(unit.genitive_plural)

    return words


def generate_words_for_group(
    elements: list[int], extra: GrammaticalCases | None = None
) -> list[str]:
    assert elements

    if extra and elements == [1]:
        return [extra.nominative_singular]

    words = [NUMBERS_DICT[element] for element in elements]

    if extra:
        if 2 <= elements[-1] <= 4:
            words.append(extra.nominative_plural)
        else:
            words.append(extra.genitive_plural)

    return words


def disassemble_group(group: int) -> list[int]:
    assert 0 <= group < 1000

    elements: list[int] = []

    tail = group % 100
    if (hundreds := group - tail) != 0:
        elements.append(hundreds)

    if 1 <= tail <= 20:
        elements.append(tail)
    else:
        units = tail % 10
        tens = tail - units
        if tens != 0:
            elements.append(tens)
        if units != 0:
            elements.append(units)
    return elements


def split_to_groups(number: int) -> list[int]:
    groups: list[int] = []
    while number != 0:
        tail = number % 1000
        number = (number - tail) // 1000
        groups.insert(0, tail)
    return groups
