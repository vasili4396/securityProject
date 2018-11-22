import json
from functools import wraps
from django.http import HttpResponse
from .settings import *


class JsonResponse(object):
    @classmethod
    def success(cls, data=None, additional_info=None):
        return cls.__base_response(200, data, additional_info)

    @classmethod
    def method_error(cls, current_method, expected_method):
        return cls.__base_error_response(
            400,
            'MethodException',
            'Invalid method <{}>, expected <{}>'.format(current_method, expected_method)
        )

    @classmethod
    def value_error(cls, msg):
        return cls.__base_error_response(400, 'ValueException', msg)

    @classmethod
    def internal_error(cls, msg=''):
        return cls.__base_error_response(500, 'InternalError', msg)

    @classmethod
    def algo_internal_error(cls, msg=''):
        return cls.__base_error_response(500, 'AlgorithmInternalError', msg)

    @classmethod
    def __base_error_response(cls, code, error_type, error_message=''):
        response_data = {
            'error_type': error_type,
            'error_message': error_message
        }
        return cls.__base_response(code, response_data)

    @classmethod
    def __base_response(cls, code, data, additional_info=None):
        response_data = {
            'code': code,
            'data': data,
            'info': additional_info
        }
        return HttpResponse(json.dumps(response_data, separators=(',', ':'), ensure_ascii=False), content_type='application/json')


def api_method(
        method,
        form_cls=None
    ):

    def decor(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):

            if request.method != method:
                return JsonResponse.method_error(request.method, method)

            form = None

            if form_cls is not None:
                if request.method == 'GET':
                    form_params = request.GET
                elif request.method == 'POST':
                    if "Expo" in request.META['HTTP_USER_AGENT'] or "okhttp/3.6.0" in request.META['HTTP_USER_AGENT']:
                        form_params = json.loads(request.body.decode())
                    else:
                        form_params = request.POST
                else:
                    form_params = {}

                form = form_cls(form_params)
                if not form.is_valid():
                    return JsonResponse.value_error(str(list(form.errors.items())))

                kwargs['form'] = form.cleaned_data
            else:
                kwargs.pop('form', None)

            try:
                return func(request, *args, **kwargs)
            except Exception as e:
                print(e)
                if DEBUG:
                    raise e
                else:
                    # todo: add logging at DEBUG = False
                    return JsonResponse.internal_error()

        return wrapper

    return decor
