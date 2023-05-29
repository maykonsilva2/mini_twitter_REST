
from TUsers.models import TUser
from TUsers.views import is_autherized

from Tweets.models import TCtweets
from Tweets.serializer import TCValidator, TCtweersSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.paginator import Paginator

import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


def get_user_obj(user=None):
    # Purpose: return the User Objects corresponding to the username
    return TUser.objects.get(username=user)


@api_view(['POST'])
def CreateTweet(request):
    """
    Purpose: Create a new tweet
    Input: <str> username, <str> tweet_text
    Output: TCtweet Object of the created tweet
    """
    if request.method == 'POST':
        username = request.query_params.get('username')
        text = request.query_params.get('tweet_text')
        # check if the user is authorized to tweet
        if is_autherized(request, username):
            validate = TCValidator(request.query_params, request.FILES)
            if not validate.is_valid():
                error = {
                    'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "Invalid username or tweet_text"
                }
                logger.error(error)
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
            try:
                user = get_user_obj(username)
                new_tweet = TCtweets(username=user, tweet_text=text)
                new_tweet.save()
                serializer = TCtweersSerializer(new_tweet)
                return Response(serializer.date, status=status.HTTP_201_CREATED)
            except Exception as e:
                error = {
                    'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "User Does not exist"
                }
                logger.error(e)
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
        # if the user is not authorized to tweet
        else:
            error = {
                'Error_code': status.HTTP_400_BAD_REQUEST,
                'Error_Message': "Authentication failed. Please login"
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def Timeline(request, username):
    '''
    Purpose: Return the Timeline of the user in a paginated Fashion
    Input: page
    Output: Tweet Object with all the tweets in the page
    '''
    # check if the user is authorized to acess the timeline
    if is_autherized(request, username):
        try:
            page_no = int(request.query_params.get('page', 1))
            userObj = get_user_obj(username)

            if page_no < 1:
                error = {
                    'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "Invalid page number, Please pass an integer value as Page Number(Starting with 1))"
                }
                logger.error(error)
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

            # get all the tweets of the user
            tweets = TCtweets.objects.filter(username=userObj)
            #  filter tweets so users don't see their own posts
            tweets = tweets.exclude(username=request.user.username)
            paginator = Paginator(tweets, 10)
            page_num = paginator.get_page([page_no])
            tweet_objs = page_num.object_list
            serializer = TCtweersSerializer(tweet_objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            error = {
                'Error_code': status.HTTP_400_BAD_REQUEST,
                'Error_Message': "No Tweets to show"
            }
        logger.error(e)
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
    # if the is not authorized to acess the timeline
    else:
        error = {
            'Error_code': status.HTTP_400_BAD_REQUEST,
            'Error_Message': "Authentication failed. Please login"
        }
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_tweets(request):
    '''
    Debugging
    '''
    tweet = TCtweets.objects.all()
    serializer = TCtweersSerializer(tweet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
