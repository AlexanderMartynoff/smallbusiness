from typing import List, Dict, Optional, AnyStr, Any, Tuple
from itertools import groupby
from collections import defaultdict
import num2words


ItemType = Dict[AnyStr, Any]
ItemsType = List[ItemType]


def groupbycrud(source_items: ItemsType,
                update: Optional[ItemType] = None,
                key: AnyStr = '_crud') -> Tuple[ItemsType, ItemsType, ItemsType]:

    groups: Dict[AnyStr, ItemsType] = defaultdict(list)

    for operation, grouped_items in groupby(source_items, lambda source_item: source_item.get('_crud', None)):

        if operation is not None:
            groups[operation] = [{**grouped_item, **update} for grouped_item in grouped_items]

    return groups['insert'], groups['update'], groups['delete']


def number2words(*args, **kwargs):
    return num2words.num2words(*args, **kwargs).capitalize()
