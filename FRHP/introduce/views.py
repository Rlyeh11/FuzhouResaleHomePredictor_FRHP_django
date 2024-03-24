from django.shortcuts import HttpResponse, render
# from django.views.decorators.csrf import csrf_exempt


def introduceIndex(request):
    response = render(request, 'index.html')
    response["Set-Cookie"] = "SameSite=None;Secure"
    return response



def predictIndex(request):
    response = render(request, 'predict.html')
    response["Set-Cookie"] = "SameSite=None;Secure"
    return response


def testIndex(request):
    return render(request, 'test.html')