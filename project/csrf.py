from django.middleware.csrf import CsrfViewMiddleware as DjangoCsrfViewMiddleware


class CsrfMiddleware(DjangoCsrfViewMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        request.is_mobile = False

        if "Expo" in request.META['HTTP_USER_AGENT'] or "okhttp/3.6.0" in request.META['HTTP_USER_AGENT']:
            request.is_mobile = True
            return

        response = super().process_view(request, callback, callback_args, callback_kwargs)
        if response is not None:
            pass
