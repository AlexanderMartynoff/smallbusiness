from typing import (
    Dict, Any, Collection, Tuple, Type,
    TypeVar, Callable, Union, get_type_hints
)
from functools import wraps
import inspect
import attr
from falcon import Request, Response

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

A = TypeVar('A')
B = TypeVar('B')


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

    def process_request(self, request, response):
        request.context['settings'] = self._settings
        request.context['database'] = self._database
        request.context['security'] = self._security
        request.context['resource'] = self._resource
        request.context['api'] = API(
            account=Account(self._database),
            account_product=AccountProduct(self._database),
            bank=Bank(self._database),
            configuration=Configuration(self._database),
            currency_unit=CurrencyUnit(self._database),
            partner=Partner(self._database),
            time_unit=TimeUnit(self._database),
            user=User(self._database),
            security=self._security,
            settings=self._settings,
            resource=self._resource,
        )


class _Endpointmethod:
    def __init__(self, method):
        self._method = method

    def __get__(self, instance, cls):
        if instance is None:
            instance = cls

        def function(*args, **kwargs):
            try:
                return self._method(instance, cls, args, kwargs)
            except AttributeError as error:
                raise NotImplementedError from error

        return function

    def __set__(self):
        raise NotImplementedError

    def __delete__(self):
        raise NotImplementedError


def endpointmethod(wrapped):
    return _Endpointmethod(wrapped)


def endpoint(cls: Type[A]) -> Type[A]:

    assert type(cls) is type, f'For only with classes use not for ``{type(cls)}``'

    class Endpoint(cls):
        @endpointmethod
        def on_get(instance, cls, args, kwargs):
            return _injector(super(cls, instance).on_get)(*args, **kwargs)

        @endpointmethod
        def on_post(instance, cls, args, kwargs):
            return _injector(super(cls, instance).on_post)(*args, **kwargs)

        @endpointmethod
        def on_put(instance, cls, args, kwargs):
            return _injector(super(cls, instance).on_put)(*args, **kwargs)

        @endpointmethod
        def on_delete(instance, cls, args, kwargs):
            return _injector(super(cls, instance).on_delete)(*args, **kwargs)

    return Endpoint


def _injector(wrapped: Callable[..., A]) -> Callable[..., A]:
    """ Special decorator that make decomposition
        for ``falcon`` dict ``request.context``.
        Wait for exists the next key in ``request.context``:
        - settings
        - database
        - security
        - resource
        - api
    """

    signature = inspect.signature(wrapped)

    @wraps(wrapped)
    def wrapper(*args, **kwargs) -> A:

        request, response = args

        assert 'settings' in request.context and \
            'database' in request.context and \
            'resource' in request.context and \
            'api' in request.context, KeyError('Incorrect ``request.context``')

        if 'api' in signature.parameters:
            kwargs.update(api=request.context['api'])

        if 'settings' in signature.parameters:
            kwargs.update(settings=request.context['settings'])

        if 'context' in signature.parameters:
            kwargs.update(context=request.context)

        # request.context['session']
        if '_' in signature.parameters:
            kwargs.update(_=i18n.Translator())

        if 'i18n' in signature.parameters:
            kwargs.update(i18n=i18n.Translator())

        return wrapped(*args, **kwargs)

    return wrapper
