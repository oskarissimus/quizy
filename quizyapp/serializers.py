from .models import UserPoints
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class UserPointsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserPoints
        fields = ['user', 'points']
