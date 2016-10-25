# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from rest_framework import routers

from rest_framework_swagger.views import get_swagger_view


###############  USERS IMPORTS  ###################
from exo_sketchfab.users.serializers import AllUsersViewSet
from exo_sketchfab.users.views import UserDetailAPIView, AllUsersListAPIView, api_home
###############  END USERS IMPORTS  ###################
###############  SOCIAL IMPORTS  ###################
from exo_sketchfab.socialaccounts.views import FacebookLogin, AllUsersSocialAccountsListAPIView, SpecificUserSocialAccountsListAPIView
###############  END SOCIAL IMPORTS  ###################
###############  FRIENDSHIPS IMPORTS  ###################
from exo_sketchfab.friendships.views import FollowCreateAPIView, UnfollowCreateAPIView, UserFollowedListAPIView, \
    UserFollowingListAPIView
###############  END FRIENDSHIPS IMPORTS  ###################
###############  MODEL 3D  IMPORTS  ###################
from exo_sketchfab.models3d.views import Model3DCreateAPIView, UserModel3DListAPIView, AllModel3DListAPIView, SpecificModel3DListAPIView
###############  END MODEL 3D IMPORTS  ###################
###############  BADGES  IMPORTS  ###################
from exo_sketchfab.badges.views import UserBadgesListAPIView
###############  BADGES  IMPORTS  ###################

schema_view = get_swagger_view(title='Sketchfab API')




# One Viewset, another GET method just for fun
router = routers.DefaultRouter()
router.register(r"users", AllUsersViewSet)



urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('exo_sketchfab.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here

    #########################################
    #########################################
    ##############  PACKAGES  ###############

    #  Django-friendship
    #  https://github.com/revsys/django-friendship
    url(r'^friendship/', include('friendship.urls')),



    ##########################################
    ##########################################
    ##############      API     ##############

    ##############    API DOC    ##############

    #  Django-rest-swagger
    #  http://django-rest-swagger.readthedocs.io/en/latest/
    url(r'^docs/', schema_view),


    ##############  API ROOT    ##############

    url(r'^api/$', api_home, name='api_home'),

    # One Viewset, another GET method just for fun
    url(r'^api2/', include(router.urls)),

    ##############  USER MGMT    ##############

    #  List every users with all theirs details
    url(r'^api/users/$', AllUsersListAPIView.as_view(), name='user_list_api'),

    #  List every infos/details of the current user
    url(r'^api/users/current_user/$', UserDetailAPIView.as_view(), name='user_detail_api'),

    #  List social accounts of every users
    url(r'^api/social_accounts/all_users_list/$', AllUsersSocialAccountsListAPIView.as_view(),
        name='all_users_social_accounts_api'),

    #  List social account of specific user when given her uid
    url(r'^api/social_accounts/specific_user/(?P<uid>[0-9]+)/$', SpecificUserSocialAccountsListAPIView.as_view(),
        name='specific_user_social_accounts_api'),


    ############  AUTHENTICATION    ############

    #  django-rest-auth - http://django-rest-auth.readthedocs.io/en/latest/installation.html

    # Allow to both register and login with FB (fb_connect)
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),


    ##############  FRIENDSHIP    ##############

    # Create new follow relationship. Current user follow another one
    url(r'^api/relationdship/current_user_new_follow/$', FollowCreateAPIView.as_view(),
        name='relationdship_create_follow_api'),

    # Delete follow relationship ie current user unfollow user with id=followee_id
    url(r'^api/relationdship/current_user_unfollow/(?P<followee_id>\d+)/$', UnfollowCreateAPIView.as_view(),
        name='relationdship_unfollow_api'),

    # List current user followers
    url(r'^api/relationdship/current_user_followers/$', UserFollowedListAPIView.as_view(),
        name='relationdship_followers_api'),

    # List current user followees
    url(r'^api/relationdship/current_user_following/$', UserFollowingListAPIView.as_view(),
        name='relationdship_following_api'),


    ##############  MODEL 3D    ##############

    # Current user create new model3D
    url(r'^api/models_3d/create/$', Model3DCreateAPIView.as_view(),
        name='models_3d_create_api'),

    # List current user's model3D
    url(r'^api/models_3d/current_user_list/$', UserModel3DListAPIView.as_view(),
        name='models_3d_current_user_list_api'),

    # List every model3D (from every users)
    url(r'^api/models_3d/list_all_models3d/$', AllModel3DListAPIView.as_view(),
        name='list_all_models3d_api'),

    # View specific model3D with id=model_id
    url(r'^api/models_3d/specific_model_details/(?P<model_id>\d+)/$', SpecificModel3DListAPIView.as_view(),
        name='specific_model_details_api'),


    ##############  BADGES    ##############

    # List current user's Badges
    url(r'^api/badges/current_user_list/$', UserBadgesListAPIView.as_view(),
        name='badges_current_user_list_api'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
