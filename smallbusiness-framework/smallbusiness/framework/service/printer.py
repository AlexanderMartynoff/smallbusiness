from typing import Dict, Any, List
import locale
from os.path import join
from functools import partial
from datetime import datetime
import weasyprint
import jinja2


from .. environment import FRAMEWORK_RESOURCE_DIR
from .. instrument import number2words


def _account_product_total_price(product: List[Dict[str, Any]]):
    return product['value'] * product['price']


def _account_total_price(account: Dict[str, Any]):
    return sum(map(_account_product_total_price, account['products']))


def _generate_account_based_report(account: dict, template_path: str) -> bytes:
    return weasyprint.HTML(
        string=environment.get_template(template_path).render(account=account)
    ).write_pdf()


def account_as_pdf(account: dict) -> bytes:
    return _generate_account_based_report(account, 'html/account.html')


def act_as_pdf(account: dict) -> bytes:
    return _generate_account_based_report(account, 'html/act.html')


def invoice_as_pdf(account: dict) -> bytes:
    return _generate_account_based_report(account, 'html/invoice.html')


environment = jinja2.Environment(loader=jinja2.FileSystemLoader(
    join(FRAMEWORK_RESOURCE_DIR, 'template')))


environment.globals.update(
    get_account_total_price=_account_total_price,
    get_account_product_total_price=_account_product_total_price,
    convert_number_to_word=lambda number: number2words(number, lang='ru', to='currency', currency='RUB', cents=False, seperator=' '),
    strftimestamp=lambda ts, format='%Y/%m/%d': datetime.fromtimestamp(ts / 1000).strftime(format),
    format_currency=lambda number: locale.format('%.2f', number, grouping=True)
)
