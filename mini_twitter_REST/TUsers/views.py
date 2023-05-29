from TUsers.models import TUser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from TUsers.serializer import TUserSerializer

import logging
import datetime
from django.conf import settings
import jwt

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

#  TODO: Token that expires in 60 minutes
EXP_TIME = datetime.timedelta(minutes=5)


def GetToken(username):
    """
    Purpose: Get access token for user
    Input:
    username:
    password:
    Output: Token that expires in 60 minutes
    """
    try:
        user = TUser.objects.get(username=username)
        if user:
            try:
                payload = {
                    'id': user.id,
                    'username': user.username,
                    'exp': datetime.datetime.utcnow() + EXP_TIME
                }
                token = {
                    'token': jwt.encode(payload, settings.AUTH_TOKEN).decode('utf8')
                }
                return token
            except Exception as e:
                error = {
                    'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_message': "Error generating Auth Token"
                }
                logger.error(e)
                return Response(error, status=status.HTTP_403_FORBIDDEN)
        else:
            error = {
                'Error_code': status.HTTP_400_BAD_REQUEST,
                'Error_Message': 'Invalid username or password'
            }
            return Response(error, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        error = {
            'Error_code': status.HTTP_400_BAD_REQUEST,
            'Error_Message': "Internal Server Error"
        }
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


def Auth(request, username):
    """
    Purpose: Login to the Application
    Input:
    token
    Output: User object of the logged in user
    """
    try:
        #  obter o token JWT da sessão do request
        token = request.session.get('authtoken').get('token')
        # contém as informações do do user codificadas no token
        payload = jwt.decode(token, settings.AUTH_TOKEN)

        user = TUser.objects.get(username=username)

        if payload.get('username') == user.username:
            serializer = TUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {
                'Error_code': status.HTTP_403_FORBIDDEN,
                'Error_Message': "Invalid User"
            }
            logger.error(error)
            return Response(error, status=status.HTPP_403_FORBIDDEN)

    except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError) as e:
        error = {
            'Error_code': status.HTTP_403_FORBIDDEN,
            'Error_Message': "Token is Invalid/Expired"
        }
        logger.error(e)
        return Response(error, status=status.HTTP_403_FORBIDDEN)

    except Exception as e:
        error = {
            'Error_code': status.HTTP_403_FORBIDDEN,
            'Error_Message': "Internal Server Error"
        }
        logger.error(e)
        return Response(error, status=status.HTTP_403_FORBIDDEN)


def is_autherized(request, username):
    validation = Auth(request, username)
    if validation.status_code == 200:
        return True
    else:
        return False


@api_view(['POST'])
def AccountSignup(request):
    """
    Purpose: Create a new user
    Input:
    username
    password
    Output: User object of the created user
    """
    serializer = TUserSerializer(data=request.query_params)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Login(request, username=None, password=None):
    """
    purpose: Authenticate if username and password is correct
    Input:
    Output: return User object or Error
    """
    username = request.query_params.get('username')
    password = request.query_params.get('password')
    try:
        user = TUser.objects.get(username=username)
        if user.password == password:
            token = GetToken(username)
            user.token = token['token']
            user.save()
            request.session['authtoken'] = token
            serializer = TUserSerializer(user)
            return Response(serializer.data, status=status.HTPP_200_OK)
        else:
            error = {
                'Error_code': status.HTTP_400_BAD_REQUEST,
                'Error_Message': "Invalid username or password"
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {
            'Error_code': status.HTTP_400_BAD_REQUEST,
            'Error_Message': "Invalid username or password"
        }
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def users(request):
    """
    Purpose: Get all users for debugging
    """
    if request.method == 'GET':
        users = TUser.objects.all()
        serializer = TUserSerializer(users, many=True)
        return Response(serializer.data)
