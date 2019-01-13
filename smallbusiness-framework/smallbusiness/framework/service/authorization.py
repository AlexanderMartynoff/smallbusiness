from typing import List, Any, Dict, Optional
from falcon import errors
import attr

from .. import api
from ..database import Database
from ..security import AuthorizationPolicy
from ..logger import getlogger

logger = getlogger(__name__)


@attr.s(frozen=True)
class Permission:

    @attr.s(frozen=True)
    class Operation:
        _entity: str = attr.ib()

        @property
        def create(self):
            return self._entity + '.create'

        @property
        def read(self):
            return self._entity + '.read'

        @property
        def update(self):
            return self._entity + '.update'

        @property
        def delete(self):
            return self._entity + '.delete'

    def entities(self):
        properties = []

        for property_name in dir(self):
            property = getattr(self, property_name)

            if isinstance(property, self.Operation):
                properties += [property_name]

        return properties

    def entries(self, user_id):
        return [{
            'entity': entity,
            'user_id': user_id,
            'create': False,
            'read': False,
            'update': False,
            'delete': False,
        } for entity in self.entities()]

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
    permission = Operation('permission')


permission = Permission()


class DBAuthorizationPolicy(AuthorizationPolicy):
    def __init__(self, database: Database):
        self._userapi = api.User(database)

    def checkpermission(self, permission: str,
                        usercontext: Optional[Dict[str, Any]]) -> None:

        if not usercontext:
            raise errors.HTTPUnauthorized()

        user = self._userapi.selectone_by_login(usercontext['login'])

        if user is None:
            raise errors.HTTPUnauthorized()

        user_permissions = []

        for user_permission in user['permissions']:
            for operation in 'create', 'read', 'update', 'delete':
                if user_permission[operation]:
                    user_permissions.append(user_permission['entity'] + '.' + operation)

        if not user['sudo'] and permission not in user_permissions:
            raise errors.HTTPForbidden(f'For the resource must have permission ``{permission}``')
