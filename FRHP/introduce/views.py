import re

from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt


def check_cookie(request, key):
    status = request.COOKIES.get(key)
    return status

def check_background(request):
    color = check_cookie(request, 'background_color')
    if color == None:
        color = '#c0ccda'
    return color


@csrf_exempt
def introduceIndex(request):
    color = check_background(request)
    response = render(request, 'index.html')
    response["Set-Cookie"] = f"SameSite=None;Secure;background_color={color}"
    return response


@csrf_exempt
def predictIndex(request):
    response = render(request, 'predict.html')
    response["Set-Cookie"] = "SameSite=None;Secure"
    return response

@csrf_exempt
def testIndex(request):
    return render(request, 'test.html')

