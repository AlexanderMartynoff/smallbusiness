from os.path import dirname, abspath, join, exists
import locale
import falcon

from smallbusiness import framework
from smallbusiness.framework.api import api as frameworkapi
from smallbusiness.framework.database.adapter import SqliteDatabase, PostgresDatabase
from smallbusiness.framework.plugin.falcon import Request, Response
from smallbusiness.framework import endpoint
from smallbusiness.framework.security import (
    SecurityServer,
    JWTAuthenticationPolicy,
    AuthenticationMiddleware,
    CockieSession,
)
from smallbusiness.framework.resource import Resource, SQLITE_DB

MODULE_DIR = dirname(__file__)

resource = Resource([
    dirname(framework.__file__),
    dirname(__file__)
])
settings = resource.load_yaml('./resource/settings.yaml')

security = SecurityServer(
    JWTAuthenticationPolicy(settings['security']['secret']),
    CockieSession(),
)
database = SqliteDatabase(SQLITE_DB)

api = frameworkapi.API(
    account=frameworkapi.Account(database),
    account_product=frameworkapi.AccountProduct(database),
    bank=frameworkapi.Bank(database),
    configuration=frameworkapi.Configuration(database),
    currency_unit=frameworkapi.CurrencyUnit(database),
    partner=frameworkapi.Partner(database),
    time_unit=frameworkapi.TimeUnit(database),
    user=frameworkapi.User(database),
    security=security,
    settings=settings,
    resource=resource,
)

application = falcon.API(
    request_type=Request,
    response_type=Response,
    middleware=[AuthenticationMiddleware(security)],
)

application.add_route('/api/account', endpoint.Account(api))
application.add_route('/api/account/{id}', endpoint.Account.ID(api))
application.add_route('/api/account_product', endpoint.AccountProduct(api))
application.add_route('/api/bank', endpoint.Bank(api))
application.add_route('/api/bank/{bank_id}', endpoint.Bank.ID(api))
application.add_route('/api/partner', endpoint.Partner(api))
application.add_route('/api/partner/{id}', endpoint.Partner.ID(api))
application.add_route('/api/time_unit', endpoint.TimeUnit(api))
application.add_route('/api/currency_unit', endpoint.CurrencyUnit(api))
application.add_route('/api/configuration', endpoint.Configuration(api))
application.add_route('/api/report/{entity}/{entity_id}', endpoint.Report.ID(api))
application.add_route('/api/security/authenticate', endpoint.Security(api))

application.add_route('/api/number_to_word', endpoint.Number2Word(api))
application.add_route('/api/mail', endpoint.Mail(api))


for static_dir in settings['server']['static_dirs']:
    application.add_static_route('/static', join(MODULE_DIR, static_dir))
