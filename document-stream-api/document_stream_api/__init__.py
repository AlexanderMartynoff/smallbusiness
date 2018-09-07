import falcon

from .addon.falcon import Request, Response
from .configurator import Configurator
from .environment import APPLICATION_DIR, RESOURCE_DIR
from .endpoint import (
    Account,
    AccountProduct,
    Partner,
    TimeUnit,
    CurrencyUnit,
    Bank,
    Report,
)


config = Configurator(dirs=[RESOURCE_DIR], name='config.yaml')

api = falcon.API(
    request_type=Request,
    response_type=Response
)


api.add_route('/api/account', Account)
api.add_route('/api/account/{id}', Account.ID)
api.add_route('/api/account_product', AccountProduct)
api.add_route('/api/bank', Bank)
api.add_route('/api/partner', Partner)
api.add_route('/api/partner/{id}', Partner.ID)
api.add_route('/api/time_unit', TimeUnit)
api.add_route('/api/currency_unit', CurrencyUnit)
api.add_route('/api/report/{entity}/{entity_id}/{type}/{format}', Report.ID)


for static_dir in config['server']['static_dirs']:
    api.add_static_route('/static', static_dir)
