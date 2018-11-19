def pre_request(worker, request):
    if request.path == '/':
        request.path = '/static/index.html'


threads = 1
worker_class = 'sync'
workers = 1
bind = '127.0.0.1:8000'
