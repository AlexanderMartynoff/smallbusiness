from typing import Any
from functools import wraps
from inspect import isfunction
from falcon import Request, Response


_error_msg = 'Incorrect decorator usage, expect decorated function like: ' \
    '``def (request, response, ...)`` or ' \
    '``def (self, request, response, ...)`` or ' \
    '``def (cls, request, response, ...)``'


def haspermission(permission):
    def wrapper(wrapped):

        if not isfunction(wrapped):
            raise RuntimeError(_error_msg)

        @wraps(wrapped)
        def security(*args: Any, **kwargs: Any):

            if len(args) == 2:
                request, response = args
            elif len(args) == 3:
                _head, request, response = args
            else:
                raise RuntimeError(_error_msg)

            assert isinstance(request, Request), \
                TypeError(f'Unexpected request type - {type(request)}')

            assert isinstance(response, Response), \
                TypeError(f'Unexpected response type - {type(response)}')

            assert 'security' in request.context, \
                KeyError('Expected ``security`` key in ``request.context``')

            security = request.context['security']
            usercontext = security.get_context(request, response)

            # There is a place for error raising
            security.authorization.checkpermission(permission, usercontext)

            return wrapped(*args, **kwargs)

        return security

    return wrapper
