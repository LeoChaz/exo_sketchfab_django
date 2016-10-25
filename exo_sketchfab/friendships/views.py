__author__ = 'leomaltrait'

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import Response
from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from friendship.models import  Follow

from .serializers import FollowCreateSerializer, FollowSerializer

User = get_user_model()



# Create new follow relationship. Current user follow another one
class FollowCreateAPIView(generics.CreateAPIView):

    serializer_class = FollowCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    # SessionAuthentication enable Cookies so CSRF-token -> Take it off for POST, PUT, DELETE
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]


# Delete follow relationship ie current user unfollow user with id=followee_id
class UnfollowCreateAPIView(generics.DestroyAPIView):

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]

    lookup_field = 'followee_id'

    def get_queryset(self):
        follow = Follow.objects.filter(follower=self.request.user).all()
        return follow

    def destroy(self, request, *args, **kwargs):

        followee = User.objects.get(pk=self.kwargs['followee_id'])
        Follow.objects.remove_follower(follower=self.request.user, followee=followee)

        return Response(status=status.HTTP_204_NO_CONTENT)


# List current user followers
class UserFollowedListAPIView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.request.user.followers.all()


# List current user followees
class UserFollowingListAPIView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.request.user.following.all()

