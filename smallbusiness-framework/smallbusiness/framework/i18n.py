from collections import Collection
from typing import Dict, Any
from os.path import join
from ruamel import yaml
import gettext

from . resource import FRAMEWORK_RESOURCE_DIR


class Translator:
    def __init__(self):
        self._translation = gettext.translation(
            domain='framework',
            localedir=join(FRAMEWORK_RESOURCE_DIR, 'i18n/locale'),
            languages=['ru', 'en']
        )

    def __call__(self, *args, **kwargs):
        return self._translation.gettext(*args, *kwargs)


def dictionary_extractor(file, keywords, comment_tags, options):
    dictionary = yaml.load(file.read(), yaml.RoundTripLoader)

    for _group, messages in dictionary.items():
        assert isinstance(messages, list)

        for message in messages:
            yield (20, None, message, [])
