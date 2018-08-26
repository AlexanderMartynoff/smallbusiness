import falcon

from .addon.falcon import Request, Response
from .configurator import Configurator
from .environment import APPLICATION_DIR, RESOURCE_DIR
from .endpoint import Account, AccountProduct, Partner, TimeUnit


config = Configurator(dirs=[RESOURCE_DIR], name='config.yaml')

api = falcon.API(
    request_type=Request,
    response_type=Response
)


api.add_route('/api/account', Account)
api.add_route('/api/account/{id}', Account.Element)

api.add_route('/api/account_product', AccountProduct)
api.add_route('/api/partner', Partner)
api.add_route('/api/time_unit', TimeUnit)


for static_dir in config['server']['static_dirs']:
    api.add_static_route('/static', static_dir)
