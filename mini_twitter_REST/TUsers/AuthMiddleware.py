from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.response import Response

from rest_framework import status

from TUsers.models import TUser
from TUsers.serializer import TUserSerializer

import logging
import jwt

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class AuthMiddleware(BaseBackend):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.auth(request)
        return self.get_response(request)

    def auth(self, request):
        exclusion_list = ['/signup', '/login']
        if request.path not in exclusion_list:
            try:
                urlstr = request.path
                user = urlstr.split('/')[1]
                token = request.session.get('authtoken').get('token')
                payload = jwt.decode(token,  settings.AUTH_TOKEN)
                userObj = TUser.objects.get(username=user)
                if payload.get('username') == userObj.username:
                    return True
                else:
                    raise PermissionDenied

            except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError) as e:
                error = {
                    'Error_code': status.HTTP_403_FORBIDDEN,
                    'Error_message': "Invalid Token or Expired"
                }
                logger.error(e)
                raise PermissionDenied(error)

            except Exception as e:
                error = {
                    'Error_code': status.HTTP_403_FORBIDDEN,
                    'Error_message': "Invalid user"
                }
                logger.error(e)
                raise PermissionDenied(error)
        else:  # Se o caminho do request estiver na lista de exclusão, não é necessário verficar o token
            return True
