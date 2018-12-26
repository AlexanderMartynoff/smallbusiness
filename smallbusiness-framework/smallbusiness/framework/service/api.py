from typing import Dict, Any, Collection, get_type_hints
from functools import wraps
import inspect
import attr

from ..api.account import Account
from ..api.account_product import AccountProduct
from ..api.bank import Bank
from ..api.currency_unit import CurrencyUnit
from ..api.time_unit import TimeUnit
from ..api.partner import Partner
from ..api.configuration import Configuration
from ..api.user import User
from ..resource import Resource
from ..security import SecurityServer
from ..database import Database

from .. import i18n


@attr.s(frozen=True, kw_only=True)
class API:
    account: Account = attr.ib()
    account_product: AccountProduct = attr.ib()
    bank: Bank = attr.ib()
    configuration: Configuration = attr.ib()
    currency_unit: CurrencyUnit = attr.ib()
    partner: Partner = attr.ib()
    time_unit: TimeUnit = attr.ib()
    user: User = attr.ib()
    resource: Resource = attr.ib()
    security: SecurityServer = attr.ib()
    settings: Dict[str, Any] = attr.ib()


class ContextMiddleware:

    def __init__(self, settings: Dict[str, Any],
                 database: Database,
                 security: SecurityServer,
                 resource: Resource):

        self._settings = settings
        self._database = database
        self._security = security
        self._resource = resource

        self._api = API(
            account=Account(database),
            account_product=AccountProduct(database),
            bank=Bank(database),
            configuration=Configuration(database),
            currency_unit=CurrencyUnit(database),
            partner=Partner(database),
            time_unit=TimeUnit(database),
            user=User(database),
            security=security,
            settings=settings,
            resource=resource,
        )

    def process_request(self, request, response):
        request.context['settings'] = self._settings
        request.context['database'] = self._database
        request.context['security'] = self._security
        request.context['resource'] = self._resource
        request.context['api'] = self._api


class _Endpointmethod:
    def __init__(self, method):
        self._method = method

    def __get__(self, instance, cls):
        if instance is None:
            instance = cls

        def function(*args, **kwargs):
            return self._method(instance, cls, args, kwargs)

        return function


def _endpointmethod(wrapped):
    return _Endpointmethod(wrapped)


def endpoint(cls):
    assert type(cls) is type, f'For only with class use not for ``{type(cls)}``'

    class Endpoint(cls):
        @_endpointmethod
        def on_get(instance, cls, args, kwargs):
            return _injector(super(cls, instance).on_get)(*args, **kwargs)

        @_endpointmethod
        def on_post(instance, cls, args, kwargs):
            return _injector(super(cls, instance).on_post)(*args, **kwargs)

        @_endpointmethod
        def on_put(instance, cls, args, kwargs):
            return _injector(super(cls, instance).on_put)(*args, **kwargs)

        @_endpointmethod
        def on_delete(instance, cls, args, kwargs):
            return _injector(super(cls, instance).on_delete)(*args, **kwargs)

    return Endpoint


def _injector(wrapped):
    """ Special decorator that make decomposition
        for ``falcon`` dict ``request.context``.
        Wait for exists the next key in ``request.context``:
        ???
    """

    signature = inspect.signature(wrapped)

    @wraps(wrapped)
    def wrapper(*args, **kwargs):

        request, response = args

        assert 'settings' in request.context and \
            'database' in request.context and \
            'security' in request.context and \
            'resource' in request.context and \
            'api' in request.context, TypeError('Incorrect ``request.context`` given')

        if 'api' in signature.parameters:
            kwargs.update(api=request.context['api'])

        if 'settings' in signature.parameters:
            kwargs.update(settings=request.context['settings'])

        if 'context' in signature.parameters:
            kwargs.update(context=request.context)

        if '_' in signature.parameters:
            kwargs.update(_=i18n.translator())

        return wrapped(*args, **kwargs)

    return wrapper
