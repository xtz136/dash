from rest_framework import serializers

from django.contrib.auth import get_user_model
from core.models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('mobile', 'avatar', 'headimgurl', 'nickname',
                  'display_name', 'sex', 'country', 'province', 'city', 'prefs')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    display_name = serializers.SerializerMethodField()

    def get_display_name(self, obj):
        if obj.profile.display_name:
            return obj.profile.display_name
        if obj.profile.nickname:
            return obj.profile.nickname
        return obj.username

    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'email', 'profile', 'display_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        password = data.pop('password')
        user = User(username=data['username'])
        user.set_password(password)
        user.save()
        return user
