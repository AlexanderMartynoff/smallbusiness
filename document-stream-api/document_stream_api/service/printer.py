from os.path import join
from functools import partial
import copy

import weasyprint
import jinja2

from .. environment import RESOURCE_DIR
from . import number_to_word


environment = jinja2.Environment(loader=jinja2.FileSystemLoader(
    join(RESOURCE_DIR, 'template')))

environment.filters.update(
    number_to_word_ru=partial(
        number_to_word.number_to_word,
        uom_integer=number_to_word.ruble,
        uom_fraction=number_to_word.kopeck,
    )
)


def _reportify_account(account: dict) -> dict:
    """ Compute additional properties for account.
        Return new dict.
    """

    account = copy.deepcopy(account)

    for product in account['products']:
        product['total_price'] = int(product['value'] * product['price'])
        product['value'] = int(product['value'])
        product['price'] = int(product['price'])

    account['total_price'] = \
        int(sum(product['total_price'] for product in account['products']))

    return account


def _generate_account_based_report(account: dict, template_path: str) -> bytes:
    account = _reportify_account(account)

    return weasyprint.HTML(
        string=environment.get_template(template_path).render(account=account)
    ).write_pdf()


def account_as_pdf(account: dict) -> bytes:
    return _generate_account_based_report(account, 'account/html/index.html')


def act_as_pdf(account: dict) -> bytes:
    return _generate_account_based_report(account, 'act/html/index.html')


def invoice_as_pdf(account: dict) -> bytes:
    return _generate_account_based_report(account, 'invoice/html/index.html')
