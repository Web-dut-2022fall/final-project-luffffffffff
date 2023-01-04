from .models import User
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'id': user.id,
        'name': user.username,
        'stated': user.stated
    }


def get_user_by_account(account):
    """
    根据帐号获取user对象s
    :param account: 账号，可以是用户名username，也可以是手机号mobile, 或者其他的数据
    :return: User对象 或者 None
    """
    try:
        user = User.objects.filter(Q(username=account) | Q(mobile=account)).first()
    except User.DoesNotExist:
        return None
    else:
        return user


# 实现多条件登录
class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password) and user.is_authenticated:
            return user
        else:
            return None


def save(flag, information):
    dic = {}
    if flag == 1:
        dic = {'username': information}
    elif flag == 2:
        dic = {'first_name': information.split(',')[0], 'last_name': information.split(',')[1]}
    elif flag == 3:
        dic = {'email': information}
    elif flag == 4:
        dic = {'mobile': information}
    elif flag == 5:
        dic = {'sex': information}
    elif flag == 6:
        dic = {'rom_num': information}
    elif flag == 7:
        dic = {'build_num': information}
    elif flag == 8:
        dic = {'uni_num': information}
    else:
        dic = {'car_num': information}
    return dic
