__author__ = 'leomaltrait'


from django.contrib.auth import get_user_model

from rest_framework import serializers

from friendship.exceptions import AlreadyExistsError
from friendship.models import Follow

User = get_user_model()


# Current user start to follow another one
class FollowCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        exclude = ('created', 'follower', )

    def create(self, validated_data):
        try:
            new_relationship = Follow.objects.add_follower(follower=self._context['request'].user, followee=validated_data['followee'])

        except AlreadyExistsError:
            raise serializers.ValidationError("User already followed")

        if new_relationship:
            return Follow.objects.get(follower=self._context['request'].user.pk, followee=validated_data['followee'])



# Details appearing when get followers/followees relationships
class UserDetailsSerializer(serializers.ModelSerializer):

    """
    User model w/o password
    """

    #socialaccount_set = FacebookSocialAccountSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'name',
            #'socialaccount_set'
        )
        read_only_fields = ('email', )



class FollowSerializer(serializers.ModelSerializer):

    follower_details = UserDetailsSerializer(source='follower')
    followee_details = UserDetailsSerializer(source='followee')


    class Meta:
        model = Follow
        fields = ('id', 'created', 'follower_details', 'followee_details', )

