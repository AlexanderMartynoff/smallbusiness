import locale
from os.path import join
import falcon

from .database import SqliteDatabase
from .addon.falcon import Request, Response
from .environment import APPLICATION_DIR, RESOURCE_DIR, SQLITE3_DB, Environment
from .endpoint import (
    Account,
    AccountProduct,
    Partner,
    TimeUnit,
    CurrencyUnit,
    Bank,
    Report,
    NumberToWord,
    Mail,
)

environment = Environment.get().setup(
    working_dir=RESOURCE_DIR,
    parameter_path='./parameters.yaml',
    register_services={
        'database': SqliteDatabase(SQLITE3_DB)
    }
)

locale.setlocale(
    locale.LC_ALL,
    locale.normalize(environment['server']['locale'])
)

application = falcon.API(
    request_type=Request,
    response_type=Response,
)


application.add_route('/api/account', Account)
application.add_route('/api/account/{id}', Account.ID)
application.add_route('/api/account_product', AccountProduct)
application.add_route('/api/bank', Bank)
application.add_route('/api/bank/{bank_id}', Bank.ID)
application.add_route('/api/partner', Partner)
application.add_route('/api/partner/{id}', Partner.ID)
application.add_route('/api/time_unit', TimeUnit)
application.add_route('/api/currency_unit', CurrencyUnit)
application.add_route('/api/number_to_word', NumberToWord)
application.add_route('/api/mail', Mail)
application.add_route('/api/report/{entity}/{entity_id}', Report.ID)


for static_dir in environment['server']['static_dirs']:
    application.add_static_route('/static', join(APPLICATION_DIR, static_dir))
