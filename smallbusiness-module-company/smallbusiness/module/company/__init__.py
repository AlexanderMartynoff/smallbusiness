from os.path import dirname, abspath, join, exists
import locale
import falcon
from falcon.http_error import HTTPError

from smallbusiness import framework
from smallbusiness.framework.service.api import ContextMiddleware
from smallbusiness.framework.service.authorization import DBAuthorizationPolicy
from smallbusiness.framework.database.adapter import SqliteDatabase, PostgresDatabase
from smallbusiness.framework.plugin.falcon import Request, Response
from smallbusiness.framework.security import (
    SecurityServer,
    JWTAuthenticationPolicy,
    SecurityMiddleware,
    SessionMiddleware,
    CockieSessionStorage,
)
from smallbusiness.framework.resource import Resource, SQLITE_DB, FRAMEWORK_DIR
from smallbusiness.framework import error
from smallbusiness.framework import logger
from smallbusiness.framework import endpoint


MODULE_DIR = dirname(__file__)

logger.setup()

resource = Resource([
    dirname(framework.__file__),
    dirname(__file__)
])
settings = resource.load_settings('resource/settings.yaml')
database = SqliteDatabase(SQLITE_DB)

security = SecurityServer(
    JWTAuthenticationPolicy(settings['security']['secret']),
    DBAuthorizationPolicy(database)
)
session = CockieSessionStorage()

application = falcon.API(
    request_type=Request,
    response_type=Response,
    middleware=[
        SessionMiddleware(session),
        SecurityMiddleware(security),
        ContextMiddleware(settings, database, security, resource)
    ],
)

application.add_error_handler(Exception, error.exception_handler)
application.add_error_handler(HTTPError, error.httperror_handler)

application.add_route('/api/account', endpoint.Account)
application.add_route('/api/account/{id}', endpoint.Account.ID)
application.add_route('/api/account_product', endpoint.AccountProduct)
application.add_route('/api/bank', endpoint.Bank())
application.add_route('/api/bank/{bank_id}', endpoint.Bank.ID)
application.add_route('/api/partner', endpoint.Partner)
application.add_route('/api/partner/{id}', endpoint.Partner.ID)
application.add_route('/api/time_unit', endpoint.TimeUnit)
application.add_route('/api/currency_unit', endpoint.CurrencyUnit)
application.add_route('/api/configuration', endpoint.Configuration)
application.add_route('/api/report/{entity}/{entity_id}', endpoint.Report.ID)
application.add_route('/api/security/authenticate', endpoint.Security)
application.add_route('/api/session', endpoint.Session)
application.add_route('/api/number2word', endpoint.Number2Word)
application.add_route('/api/mail', endpoint.Mail)
application.add_route('/api/user', endpoint.User)
application.add_route('/api/user/{user_id}', endpoint.User.ID)
application.add_route('/api/user/{user_id}/activate', endpoint.User.Activation)
application.add_route('/api/permission', endpoint.Permission)
application.add_route('/api/migration', endpoint.Migration)


for static_dir in settings['server']['static_dirs']:
    application.add_static_route('/static', join(MODULE_DIR, static_dir))
