class MyMiddleware:
    def __init__(self, get_response):
        print('mi1')
        self.get_response = get_response

    def __call__(self, request):
        print('mi2')
        response = self.get_response(request)
        return response

    def process_view(request, view_func, view_args, view_kwargs):
        print('m3')
    def process_exception(self, request, exception):
        print('exptions!!!')