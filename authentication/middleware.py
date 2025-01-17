from django.utils.deprecation import MiddlewareMixin

class CaptureIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        request.ip_address = ip