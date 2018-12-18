from typing import List, Dict, Optional, AnyStr, Any, Tuple
from itertools import groupby
from collections import defaultdict
import num2words


CRUDItem = Dict[AnyStr, Any]
CRUDItems = List[CRUDItem]


def groupbycrud(source_items: CRUDItems,
                update: Optional[CRUDItem] = None,
                key: AnyStr = '_crud') -> Tuple[CRUDItems, CRUDItems, CRUDItems]:

    groups: Dict[AnyStr, CRUDItems] = defaultdict(list)

    for operation, grouped_items in groupby(source_items, lambda source_item: source_item.get('_crud', None)):

        if operation is not None:
            groups[operation] = [{**grouped_item, **update} for grouped_item in grouped_items]

    return groups['insert'], groups['update'], groups['delete']


def number2words(*args, **kwargs):
    return num2words.num2words(*args, **kwargs).capitalize()


def number2currency(number, lang, currency, cents=True):
    return number2words(number, lang=lang, to='currency', currency=currency, cents=cents, seperator=' ')
