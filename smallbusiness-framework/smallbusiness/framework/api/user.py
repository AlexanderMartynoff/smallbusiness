from typing import Dict, Any, Union, List
from sqlbuilder.smartsql import T, Q

from ..service import authorization
from ..database import Service
from .permission import Permission


class User(Service):
    def selectone_by_login_password(self, login, password) -> Dict[str, Any]:
        return self._selectone_by_where(
            (T.user.login == login) & (T.user.password == password))

    def selectone_by_login(self, login) -> Dict[str, Any]:
        return self._selectone_by_where(T.user.login == login)

    def selectone(self, user_id: int) -> Dict[str, Any]:
        return self._selectone_by_where(T.user.id == user_id, [
            T.user.id,
            T.user.login,
            T.user.sudo,
            T.user.password,
        ])

    def _selectone_by_where(self, where, fields=None) -> Dict[str, Any]:

        if fields is None:
            fields = [T.user.id, T.user.login, T.user.sudo]

        with self.sqlbuilder.result() as result:
            user = Q(result=result).tables(T.user) \
                .fields(*fields) \
                .where(where) \
                .select() \
                .fetchone()

            if user:
                user.update(permissions=Permission().selectall(user['id']))

            return user

    def selectall(self) -> List[Dict[str, Any]]:

        with self.sqlbuilder.result() as result:
            return Q(result=result).tables(T.user) \
                .fields(
                    T.user.id,
                    T.user.login,
                    T.user.sudo,
                ) \
                .select() \
                .fetchall()

    def updateone(self, user_id: int, user: Dict[str, Any]) -> None:

        with self.sqlbuilder.result() as result:
            Q(result=result) \
                .tables(T.user) \
                .where(T.user.id == user_id) \
                .update({
                    T.user.sudo: user['sudo'],
                    T.user.login: user['login'],
                    T.user.password: user['password'],
                }) \
                .execute()

            return Permission().updatemany(user.get('permissions', []))

    def deleteone(self, user_id: int) -> None:

        with self.sqlbuilder.result() as result:
            return Q(result=result) \
                .tables(T.user) \
                .where(T.user.id == user_id) \
                .delete() \
                .execute()

    def insertone(self, user: Dict[str, Any]) -> Dict[str, Any]:
        with self.sqlbuilder.result() as result:
            user = Q(result=result) \
                .tables(T.user) \
                .insert({
                    T.user.login: user['login'],
                    T.user.password: user['password'],
                    T.user.sudo: user.get('sudo', False),
                }) \
                .fetchinsertid()

            self._activate(user['id'])

            return user

    def _activate(self, user_id: int) -> None:
        with self.sqlbuilder.result() as _result:
            Permission().insertmany(authorization.permission.entries(user_id))
