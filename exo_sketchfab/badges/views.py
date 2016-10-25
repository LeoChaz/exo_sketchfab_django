__author__ = 'leomaltrait'


from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import  BadgesExtended
from .serializers import BadgeListSerializer

User = get_user_model()


class UserBadgesListAPIView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BadgeListSerializer

    def get_queryset(self):
        current_user = self.request.user
        current_user_badges = BadgesExtended.objects.filter(badge_owners=current_user)
        return current_user_badges
