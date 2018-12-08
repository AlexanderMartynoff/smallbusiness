"""
Base idea is split number to groups by 3 chars.
For example 12_345_789 will split as ['12', '345', '789']
or 1_234_567 will split as ['1', '234', '567'].

Functions `_1_number_to_word`, `_2_number_to_word`, `_3_number_to_word`
"""


from typing import Tuple, Dict, Union, Any
from dataclasses import dataclass
from logging import getLogger
import re


def normal_fraction(number, size):
    pass


class Word:
    def resolve(self, *args, **kwargs):
        raise NotImplementedError


@dataclass
class WordGenus(Word):
    """ See `_runk` for detail """

    male: str = None
    female: str = None

    def resolve(self, number, rank):

        if rank == 1 and self.female is not None:
            return self.female

        return self.male


@dataclass
class WordCase(Word):

    first: str = None
    second: str = None
    third: str = None

    def resolve(self, number, _rank=None):
        return self._resolve_case(number, [self.first, self.second, self.third])

    def _resolve_case(self, number, after):
        return after[2 if (4 < number % 100 < 20) else [2, 0, 1, 1, 1, 2][min(number % 10, 5)]]


def _force_str_length(string, length, placeholder='0'):
    if len(string) < length:
        return placeholder * (length - len(string)) + string

    return string


def _1_number_to_word(number):
    """ For N numbers """

    return [_numbers[1][number]]


def _2_number_to_word(number):
    """ For NN numbers """

    if number == '00':
        return []

    if number[0] == '0':
        return _1_number_to_word(number[1:])

    words = []

    # case for 11 ... 19
    if number[0] == '1' and number[1] != '0':
        words.append(_numbers[2][number])
    else:
        words.append(_numbers[2][number[0]])

        if number[1] != '0':
            words += _1_number_to_word(number[1])

    return words


def _3_number_to_word(number):
    """ For NNN numbers """

    words = []

    if number[0] != '0':
        words.append(_numbers[3][number[0]])

    return words + _2_number_to_word(number[1:])


def _number_to_group(number: Union[int, float, str]) -> Tuple[Dict[int, str], Dict[int, str], str, str]:
    """ Example:
          >>> _number_to_group('12_345_789.12_345')
          >>> {2: '12', 1: '345', 0: '789'}, {1: '12', 0: '345'}, '12_345_789', '12_345'
    """

    try:
        integer, fraction = str(number).split('.', maxsplit=2)
    except ValueError:
        integer, fraction = str(number), '0'

    def calculate_rank(groups):
        """ See `_ranks` for more.
            Example::
              >>> calculate_rank(['12', '345', '789'])
              >>> {2: '12', 1: '345', 0: '789'}
        """

        return {len(groups) - key: value for key, value in enumerate(groups, 1)}

    def number_to_group(number):
        """
            Use case::
              >>> number_to_group('12_345_789')
              >>> ['12', '345', '789']
        """

        # TODO: replace this with `for in number[::-1]`
        # cause this hard for understanding
        return [group[::-1] for group in re.findall('.{1,3}', number[::-1])][::-1]

    return (
        # groups for integer part number
        calculate_rank(number_to_group(integer)),
        # groups for fraction part number
        calculate_rank(number_to_group(fraction)),
        # integer part number
        integer,
        # fraction part number
        fraction,
    )


def number_to_word(number: Union[int, float],
                   uom_integer: WordCase,
                   uom_fraction: WordCase,
                   uom_fraction_size=2) -> str:

    words = []
    integers, fractions, integer_part, fraction_part = _number_to_group(round(number, uom_fraction_size))

    for rank, integer in integers.items():
        _words = []

        rank_size = len(integer)

        if rank_size == 1:
            _words += _1_number_to_word(integer)

        elif rank_size == 2:
            _words += _2_number_to_word(integer)

        elif rank_size == 3:
            _words += _3_number_to_word(integer)

        if rank in _ranks.keys() and int(integer) > 0:
            _words.append(_ranks[rank])

        # resolve words variants and case

        words += [word.resolve(int(integer), rank) for word in _words]

    if len(fraction_part) > uom_fraction_size:
        fraction_part = fraction_part[:uom_fraction_size]
    elif len(fraction_part) < uom_fraction_size:
        fraction_part = fraction_part + '0' * (uom_fraction_size - len(fraction_part))

    return ' '.join(
        words +
        [uom_integer.resolve(int(integer_part))] +
        [fraction_part] +
        [uom_fraction.resolve(int(fraction_part))]
    ).capitalize()


_numbers = {
    1: {
        '0': WordGenus(male='ноль'),
        '1': WordGenus(male='один', female='одна'),
        '2': WordGenus(male='два', female='две'),
        '3': WordGenus(male='три'),
        '4': WordGenus(male='четыре'),
        '5': WordGenus(male='пять'),
        '6': WordGenus(male='шесть'),
        '7': WordGenus(male='семь'),
        '8': WordGenus(male='восемь'),
        '9': WordGenus(male='девять'),
    },

    2: {
        '11': WordGenus(male='одиннадцать'),
        '12': WordGenus(male='двенадцать'),
        '13': WordGenus(male='тринадцать'),
        '14': WordGenus(male='четырнадцать'),
        '15': WordGenus(male='пятнадцать'),
        '16': WordGenus(male='шестнадцать'),
        '17': WordGenus(male='семнадцать'),
        '18': WordGenus(male='восемнадцать'),
        '19': WordGenus(male='девятнадцать'),
        '1': WordGenus(male='десять'),
        '2': WordGenus(male='двадцать'),
        '3': WordGenus(male='тридцать'),
        '4': WordGenus(male='сорок'),
        '5': WordGenus(male='пятьдесят'),
        '6': WordGenus(male='шестьдесят'),
        '7': WordGenus(male='семьдесят'),
        '8': WordGenus(male='восемьдесят'),
        '9': WordGenus(male='девяносто'),
    },

    3: {
        '1': WordGenus(male='сто'),
        '2': WordGenus(male='двести'),
        '3': WordGenus(male='триста'),
        '4': WordGenus(male='четыреста'),
        '5': WordGenus(male='пятьсот'),
        '6': WordGenus(male='шестьсот'),
        '7': WordGenus(male='семьсот'),
        '8': WordGenus(male='восемьсот'),
        '9': WordGenus(male='девятьсот'),
    }
}

_ranks = {
    1: WordCase(first='тысяча', second='тысячи', third='тысяч'),
    2: WordCase(first='миллион', second='миллиона', third='миллионов'),
    3: WordCase(first='миллиард', second='миллиарда', third='миллиардов'),
    4: WordCase(first='триллиард', second='триллиарда', third='триллиардов'),
}


ruble = WordCase(first='рубль', second='рубля', third='рублей')
kopeck = WordCase(first='копейка', second='копейки', third='копеек')
