from collections import Collection
from typing import Dict, Any
from os.path import join
from ruamel import yaml
import gettext

from . resource import FRAMEWORK_RESOURCE_DIR


def setup_translation():
    return gettext.translation(
        domain='framework',
        localedir=join(FRAMEWORK_RESOURCE_DIR, 'i18n/locale'),
        languages=['en', 'ru']
    )


def _(message: str, context: Dict[str, Any]):
    pass


def dictionary_extractor(file, keywords, comment_tags, options):
    dictionary = yaml.load(file.read(), yaml.RoundTripLoader)

    for _group, messages in dictionary.items():
        assert isinstance(messages, list)

        for message in messages:
            yield (20, None, message, [])
