__author__ = 'leomaltrait'

from rest_framework import serializers

from allauth.socialaccount.models import SocialAccount


class FacebookSocialAccountSerializer(serializers.ModelSerializer):

    """
    SocialAccount model
    """


    gender = serializers.CharField(source='extra_data.gender', read_only=True)
    link = serializers.CharField(source='extra_data.link', read_only=True)
    locale = serializers.CharField(source='extra_data.locale', read_only=True)
    timezone = serializers.CharField(source='extra_data.timezone', read_only=True)
    picture = serializers.CharField(source='extra_data.picture.data.url', read_only=True)

    class Meta:
        model = SocialAccount
        fields = (
            'user', # user_id
            'provider',
            'uid',
            'last_login',
            'date_joined',
            'extra_data',
            'gender',
            'locale', # language chosen by user
            'timezone',
            'link',
            'picture', # small picture
            'get_avatar_url', # big picture
        )

