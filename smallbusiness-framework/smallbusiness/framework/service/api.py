from typing import (
    Dict,
    Any,
    Collection,
    Tuple,
    Type,
    TypeVar,
    Callable,
    Union,
    cast,
)
from contextvars import ContextVar
from functools import wraps
from falcon import Request, Response
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
from ..database import Database, Cursor
from .. import i18n

_T_co = TypeVar('_T_co', covariant=True)
_T = TypeVar('_T')


@attr.s(frozen=True, auto_attribs=True, kw_only=True)
class API:
    account: Account
    account_product: AccountProduct
    bank: Bank
    configuration: Configuration
    currency_unit: CurrencyUnit
    partner: Partner
    time_unit: TimeUnit
    user: User
    resource: Resource
    security: SecurityServer
    settings: Dict[str, Any]


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
        request.context['i18n'] = i18n.Translator()


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


def endpoint(wrapped: Type[_T]) -> Type[_T]:

    class Endpoint(wrapped):  # type: ignore
        @endpointmethod
        def on_get(instance, cls, args, kwargs):
            return injector(super(cls, instance).on_get)(*args, **kwargs)

        @endpointmethod
        def on_post(instance, cls, args, kwargs):
            return injector(super(cls, instance).on_post)(*args, **kwargs)

        @endpointmethod
        def on_put(instance, cls, args, kwargs):
            return injector(super(cls, instance).on_put)(*args, **kwargs)

        @endpointmethod
        def on_delete(instance, cls, args, kwargs):
            return injector(super(cls, instance).on_delete)(*args, **kwargs)

    return Endpoint


def injector(wrapped: Callable[..., _T_co]) -> Callable[..., _T_co]:
    """ Special decorator that make decomposition
        for ``falcon`` dict ``request.context``.
        Expect for next keys in ``request.context``:
        - settings
        - database
        - security
        - resource
        - api
    """

    signature = inspect.signature(wrapped)

    @wraps(wrapped)
    def wrapper(*args: Any, **kwargs: Any) -> _T_co:

        request, response = args

        assert 'settings' in request.context and \
            'database' in request.context and \
            'resource' in request.context and \
            'api' in request.context and \
            'i18n' in request.context, KeyError('Incorrect ``request.context``')

        if 'api' in signature.parameters:
            kwargs.update(api=request.context['api'])

        if 'settings' in signature.parameters:
            kwargs.update(settings=request.context['settings'])

        if '_' in signature.parameters:
            kwargs.update(_=request.context['i18n'])

        if 'i18n' in signature.parameters:
            kwargs.update(i18n=request.context['i18n'])

        return wrapped(*args, **kwargs)

    return wrapper
