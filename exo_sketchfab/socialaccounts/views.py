__author__ = 'leomaltrait'

from django.http import Http404

from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# django-rest-auth - http://django-rest-auth.readthedocs.io/en/latest/installation.html
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.models import SocialAccount
from rest_auth.registration.views import SocialLoginView


from .serializers import FacebookSocialAccountSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


# List social accounts of every users
class AllUsersSocialAccountsListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = SocialAccount.objects.all()
    serializer_class = FacebookSocialAccountSerializer


# List social account of specific user when given her uid
class SpecificUserSocialAccountsListAPIView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = SocialAccount.objects.none()
    serializer_class = FacebookSocialAccountSerializer
    lookup_field = 'uid'

    def get_object(self):
            try:
                social_account = SocialAccount.objects.get(uid=self.kwargs['uid'])
                return social_account
            except SocialAccount.DoesNotExist:
                raise Http404