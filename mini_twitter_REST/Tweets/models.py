from django.db import models
from TUsers.models import TUser
from datetime import datetime

get_cur_time = datetime.now().strftime('%m/%d/%Y %I:%M %S %p')


class TCtweets(models.Model):
    username = models.ForeignKey(TUser, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=280, null=True)
    time = models.DateTimeField(default=get_cur_time)
