from .extension import falcon
from .endpoint import Account
from .configurator import Configurator
from .environment import APPLICATION_DIR, RESOURCE_DIR


config = Configurator(dirs=[RESOURCE_DIR], name='config.yaml')

api = falcon.API(
    request_type=falcon.Request,
    response_type=falcon.Response
)

api.add_route([
    '/api/account',
    '/api/account/{id}'
], Account)

for static_dir in config['server']['static_dirs']:
    api.add_static_route('/static', static_dir)
