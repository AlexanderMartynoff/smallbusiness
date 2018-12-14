from os.path import dirname, abspath, join, exists
import locale

import falcon

from smallbusiness.framework.database.adapter import SqliteDatabase
from smallbusiness.framework.plugin.falcon import Request, Response
from smallbusiness.framework.environment import (
    FRAMEWORK_DIR,
    FRAMEWORK_RESOURCE_DIR,
    SQLITE_DB,
    Environment,
)
from smallbusiness.framework import endpoint

MODULE_DIR = dirname(abspath(__file__))
MODULE_RESOURCE_DIR = MODULE_DIR + '/resource'

environment = Environment.get().setup(
    working_dirs=[
        FRAMEWORK_RESOURCE_DIR,
        MODULE_RESOURCE_DIR,
    ],
    parameter_path='./parameters.yaml',
    register_services={
        'database': SqliteDatabase(SQLITE_DB)
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

application.add_route('/api/account', endpoint.Account)
application.add_route('/api/account/{id}', endpoint.Account.ID)
application.add_route('/api/account_product', endpoint.AccountProduct)
application.add_route('/api/bank', endpoint.Bank)
application.add_route('/api/bank/{bank_id}', endpoint.Bank.ID)
application.add_route('/api/partner', endpoint.Partner)
application.add_route('/api/partner/{id}', endpoint.Partner.ID)
application.add_route('/api/time_unit', endpoint.TimeUnit)
application.add_route('/api/currency_unit', endpoint.CurrencyUnit)
application.add_route('/api/number_to_word', endpoint.NumberToWord)
application.add_route('/api/mail', endpoint.Mail)
application.add_route('/api/database/sequence/{table}', endpoint.TableSequence)
application.add_route('/api/configuration', endpoint.Configuration)
application.add_route('/api/report/{entity}/{entity_id}', endpoint.Report.ID)


for static_dir in environment['server']['static_dirs']:
    application.add_static_route('/static', join(MODULE_DIR, static_dir))
