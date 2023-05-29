from rest_framework import serializers
from Tweets.models import TCtweets
from django import forms


class TCtweersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TCtweets
        fields = '__all__'


class TCValidator(forms.Form):
    username = forms.CharField()
    tweet_text = forms.CharField()  # max_length=280
