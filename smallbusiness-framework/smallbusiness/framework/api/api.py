from typing import Dict, Any
import attr

from .account import Account
from .account_product import AccountProduct
from .bank import Bank
from .currency_unit import CurrencyUnit
from .time_unit import TimeUnit
from .partner import Partner
from .configuration import Configuration
from .user import User
from ..resource import Resource
from ..security import SecurityServer


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
