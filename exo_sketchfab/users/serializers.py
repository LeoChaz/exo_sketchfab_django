__author__ = 'leomaltrait'


from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')

# Import is needed only if we are using social login, in which
# case the allauth.socialaccount will be declared

if 'allauth.socialaccount' in settings.INSTALLED_APPS:
    try:
        from allauth.socialaccount.helpers import complete_social_login
    except ImportError:
        pass


from .models import User
from ..socialaccounts.serializers import FacebookSocialAccountSerializer
from ..friendships.serializers import FollowSerializer
from ..models3d.serializers import Model3DListSerializer
from ..badges.serializers import BadgeListSerializer

UserModel = get_user_model()



# Every users infos
class AllUserSerializer(serializers.HyperlinkedModelSerializer):


    followers = FollowSerializer(many=True, read_only=True)
    following = FollowSerializer(many=True, read_only=True)
    socialaccount_set = FacebookSocialAccountSerializer(many=True, read_only=True)
    model3d_owner = Model3DListSerializer(many=True, read_only=True)
    badge_owner = BadgeListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'date_joined',
            'email',
            'username',
            'followers',
            'following',
            'socialaccount_set',
            'model3d_owner',
            'badge_owner',
        ]


# Current user infos
class UserDetailsSerializer(serializers.ModelSerializer):

    """
    User model w/o password
    """

    followers = FollowSerializer(many=True, read_only=True)
    following = FollowSerializer(many=True, read_only=True)
    socialaccount_set = FacebookSocialAccountSerializer(many=True, read_only=True)
    model3d_owner = Model3DListSerializer(many=True, read_only=True)
    badge_owner = BadgeListSerializer(many=True, read_only=True)


    class Meta:
        model = User
        fields = ('id', 'url', 'date_joined', 'username', 'email', 'followers', 'following', 'socialaccount_set',
                  'model3d_owner', 'badge_owner', )
        read_only_fields = ('email', )



class AllUsersViewSet(viewsets.ModelViewSet):

    # override the default from common settings for DRF
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication ]

    permission_classes = [permissions.IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = AllUserSerializer








###################
# override django-rest-auth: rest_auth.register.serializers.RegisterSerializer
# Register/create new user.

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    #password1 = serializers.CharField(required=False, write_only=True)
    #password2 = serializers.CharField(required=False, write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    # def validate_password1(self, password):
    #     return get_adapter().clean_password(password)

    # def validate(self, data):
    #     if data['password1'] != data['password2']:
    #         raise serializers.ValidationError(_("The two password fields didn't match."))
    #     return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            #'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()



class AuthUserDetailsSerializer(serializers.ModelSerializer):

    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'first_name', 'last_name', 'name')
        read_only_fields = ('email', )


# Response when authBackend
class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    user = AuthUserDetailsSerializer()
