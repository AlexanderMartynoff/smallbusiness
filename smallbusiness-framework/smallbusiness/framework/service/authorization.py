from typing import List, Any, Dict
from falcon import errors
import attr

from ..security import AuthorizationPolicy
from ..api import User
from ..logger import getlogger

logger = getlogger(__name__)


@attr.s(frozen=True)
class Permission:

    @attr.s(frozen=True)
    class Operation:
        _entity: str = attr.ib()

        _read: str = 'read'
        _write: str = 'write'
        _update: str = 'update'
        _delete: str = 'delete'

        @property
        def read(self):
            return self._entity + '.' + self._read

        @property
        def write(self):
            return self._entity + '.' + self._write

        @property
        def update(self):
            return self._entity + '.' + self._update

        @property
        def delete(self):
            return self._entity + '.' + self._delete

    bank = Operation('bank')
    currencyunit = Operation('currencyunit')
    timeunit = Operation('timeunit')
    account = Operation('account')
    accountproduct = Operation('accountproduct')
    configuration = Operation('configuration')
    partner = Operation('partner')
    user = Operation('user')
    mail = Operation('mail')
    number2word = Operation('number2word')
    report = Operation('report')
    session = Operation('session')


permission = Permission()


class DBAuthorizationPolicy(AuthorizationPolicy):
    def __init__(self, database):
        self._database = database

    def checkpermission(self, permission: str,
                        usercontext: Dict[str, Any]) -> None:

        if not usercontext:
            raise errors.HTTPUnauthorized()

        user = User(self._database).selectone_by_login(usercontext['login'])

        if user is None:
            raise errors.HTTPUnauthorized()

        if not user['sudo'] and permission not in user['permissions']:
            raise errors.HTTPForbidden(f'For the resource must have permission ``{permission}``')
