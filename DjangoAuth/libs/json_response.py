# encoding=utf8

from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import HttpResponse


def json_response(cookies=None, **kwargs):
    if 'status' not in kwargs:
        kwargs['status'] = 200
    response = HttpResponse(
        json.dumps(kwargs, cls=DjangoJSONEncoder, ensure_ascii=False),
        content_type="application/json"
    )
    if cookies:
        for k, v in cookies.items():
            response.set_cookie(k, v)
    return response
