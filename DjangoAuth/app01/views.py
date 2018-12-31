from django.http import HttpResponse
from libs.json_response import json_response
from itsdangerous import TimedJSONWebSignatureSerializer


def login(reqeust):
    s = TimedJSONWebSignatureSerializer(secret_key="hard to guess", expires_in=60)
    auth_token = s.dumps({"id": 1}).decode("utf-8")

    result = {
        "auth_token": auth_token,
    }

    return json_response(cookies=result)


def index(reqeust):
    return HttpResponse("登陆成功")


def logout(reqeust):
    return HttpResponse("登陆成功")
