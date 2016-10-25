# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'leomaltrait'


from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response as RestResponse
from rest_framework.reverse import reverse as api_reverse


from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User
from .serializers import AllUserSerializer, UserDetailsSerializer

from ..badges.signals import user_signedup


# API home
@api_view(["GET"])
def api_home(request):
    data = {
        "users": {
            "url": api_reverse("user_list_api"),
            "count": User.objects.all().count(),
        },
    }
    return RestResponse(data)


#  List every infos/details of the current user
class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self):
        pk = self.request.user.pk
        obj = get_object_or_404(User, pk=pk)

        # Signal for Pionneer Badge
        user_signedup.send(sender=None, user=obj)

        return obj


#  List every users with all theirs details
class AllUsersListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication ] # override the default from common settings for DRF
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = AllUserSerializer







###########  COOKIE-CUTTER  ############

##### Used for User Viewset


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
