from sqlbuilder.smartsql import T, Q

from ..database import Service


class Permission(Service):
    def selectall(self, user_id):

        with self.sqlbuilder.result() as result:
            return Q(result=result).tables(
                    T.user +
                    T.user_permission.on(T.user_permission.user_id == T.user.id)
                ) \
                .fields(T.user_permission.name) \
                .where(T.user.id == user_id) \
                .select() \
                .fetchall()
