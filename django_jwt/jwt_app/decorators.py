import jwt
from functools import wraps
from django_jwt.settings import SECRET_KEY
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied


UserModel = get_user_model()


def auth_permission_required(perm):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # 格式化此权限
            perms = (perm,) if isinstance(perm, str) else perm
            
            if request.user.is_authenticated:
                # 正常登陆用户判断是否有权限,没权限就报错
                if not request.user.has_perms(perms):
                    raise PermissionDenied
            else:
                try:
                    auth = request.META.get('HTTP_AUTHORIZATION').split()
                    print(auth)
                    print(auth[0].lower())
                except AttributeError:
                    return JsonResponse({"code": 401, "message": "No authenticate header"})
                
                # 用户通过API获取数据验证流程
                if auth[0].lower() == 'token':
                    try:
                        dict = jwt.decode(auth[1], SECRET_KEY, algorithm="HS256")
                        username = dict.get('data').get('username')
                    except jwt.ExpiredSignatureError:
                        return JsonResponse({"status_code": 401, "message": "Token expired."})
                    except jwt.InvalidTokenError:
                        return JsonResponse({"status_code": 401, "message": "Invalid token."})
                    except Exception as e:
                        return JsonResponse({"status_code": 401, "message": "Can not get user object."})

                    try:
                        user = UserModel.objects.get(username=username)
                    except UserModel.DoesNotExist:
                        return JsonResponse({"status_code": 401, "message": "User does not exist."})

                    if not user.is_active:
                        return JsonResponse({"status_code": 401, "message": "User inactive or deleted."})

                    if not user.has_perms(perms):
                        return JsonResponse({"status_code": 403, "message": "PermissionDenied."})
                else:
                    return JsonResponse({"status_code": 401, "message": "Not support auth type."})
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
