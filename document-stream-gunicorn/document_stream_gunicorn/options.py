def pre_request(worker, request):
    if request.path == '/':
        request.path = '/static/index.html'
