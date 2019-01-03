from sqlbuilder.smartsql import T, Q

from ..database import Service
from .permission import Permission


class User(Service):
    def selectone_by_pair(self, login, password):

        with self.sqlbuilder.result() as result:
            user = Q(result=result).tables(T.user) \
                .fields(
                    T.user.id,
                    T.user.login,
                ) \
                .where((T.user.login == login) & (T.user.password == password)) \
                .select() \
                .fetchone()

            if user:
                user.update(permissions=Permission(state=result.state()).selectall(
                    user['id']
                ))

            return user

    def selectone_by_login(self, login):

        with self.sqlbuilder.result() as result:
            user = Q(result=result).tables(T.user) \
                .fields(
                    T.user.id,
                    T.user.login,
                    T.user.sudo,
                ) \
                .where(T.user.login == login) \
                .select() \
                .fetchone()

            if user:
                user.update(permissions=Permission(state=result.state()).selectall(
                    user['id']
                ))

            return user
