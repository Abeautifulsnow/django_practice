from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from .decorators import auth_permission_required

ModelUser = get_user_model()

# Create your views here.


@auth_permission_required('select_user')
def user(request):
    if request.method == 'GET':
        _jsondata = {
            "user": "runstone",
            "site": "www.runstone.top",
        }
        
        return JsonResponse({"state": 1, "message": _jsondata})
    else:
        return JsonResponse({"state": 0, "message": "Request method 'POST' not supported"})
