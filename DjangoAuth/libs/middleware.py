from django.utils.deprecation import MiddlewareMixin

from DjangoAuth.settings import EXCLUDE_URL

from django.shortcuts import HttpResponseRedirect

import re

exclued_path = [re.compile(item) for item in EXCLUDE_URL]

from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature


class AuthMiddleWare(MiddlewareMixin):
    # 拦截request
    def process_request(self, request):
        url_path = request.path
        for each in exclued_path:
            if re.match(each, url_path):
                return None
        auth_token = request.COOKIES.get("auth_token", None)
        if not auth_token:
            return HttpResponseRedirect('/auth/login')

        s = TimedJSONWebSignatureSerializer(secret_key="hard to guess", expires_in=60)

        try:
            data = s.loads(auth_token)
            id = data.get("id", None)
        except(BadSignature, SignatureExpired):
            return HttpResponseRedirect('/auth/login')
        print(id)
        if id != 1:
            return HttpResponseRedirect('/auth/login')

        else:
            return None

    # 处理response
    def process_response(self, request, response):
        auth_token = request.COOKIES.get("auth_token", None)

        # 加上后面代码可实现token未过期时刷新token的有效期
        if auth_token:
            s = TimedJSONWebSignatureSerializer(secret_key="hard to guess", expires_in=60)
            try:
                data = s.loads(auth_token)
                id = data.get("id", None)
                print(id)
                if id:
                    flush_token = s.dumps({"id": 1}).decode("utf-8")
                    response.set_cookie("auth_token", flush_token)
            except(BadSignature, SignatureExpired):
                pass

        return response
