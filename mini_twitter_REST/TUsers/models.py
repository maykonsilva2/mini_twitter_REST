from django.db import models
from datetime import datetime

get_cur_time = datetime.now().strftime('%m/%d/%Y %I:%M %S %p')


class TUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    modified_time = models.DateTimeField(default=get_cur_time)
    token = models.CharField(max_length=10000, null=True)
