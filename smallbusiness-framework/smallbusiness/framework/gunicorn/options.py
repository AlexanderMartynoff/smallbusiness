def pre_request(worker, request):
    if request.path == '/':
        request.path = '/static/entry/authorized.html'
    elif request.path in ['/public', '/login']:
        request.path = '/static/entry/unauthorized.html'


threads = 1
worker_class = 'sync'
workers = 1
bind = '127.0.0.1'
