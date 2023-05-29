from django.urls import path
from . import views

urlpatterns = [
    path('create', views.CreateTweet),
    path('<str:username>', views.Timeline),
    path('all_tweets', views.all_tweets),  # debugging
]
