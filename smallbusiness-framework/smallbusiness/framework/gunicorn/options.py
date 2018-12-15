def pre_request(worker, request):
    if request.path == '/':
        request.path = '/static/entry/application.html'
    elif request.path == '/login':
        request.path = '/static/entry/application.security.html'


threads = 1
worker_class = 'sync'
workers = 1
bind = '127.0.0.1'
