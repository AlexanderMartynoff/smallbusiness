def pre_request(worker, request):
    if request.path == '/':
        request.path = '/static/index.html'


threads = 16
worker_class = 'sync'
workers = 8
bind = '127.0.0.1:8001'

# WITHOUT 8.539716243743896
