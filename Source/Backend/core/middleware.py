from django.contrib.sessions.middleware import SessionMiddleware

def dummy_middleware(get_response):
    def middleware(request):
        request.session = {}
        response = get_response(request)
        return response
    return middleware
