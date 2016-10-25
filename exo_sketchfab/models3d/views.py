__author__ = 'leomaltrait'

from django.http import Http404

from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Model3d
from .serializers import Model3DCreateSerializer, Model3DListSerializer

from ..badges.signals import model_viewed


# Current user create new model3D
class Model3DCreateAPIView(generics.CreateAPIView):

    serializer_class = Model3DCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    # SessionAuthentication enable Cookies so CSRF-token -> Take it off for POST, PUT, DELETE
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]


# List current user's model3D
class UserModel3DListAPIView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Model3DListSerializer
    queryset = Model3d.objects.none()

    def get_queryset(self):

        user_models = Model3d.objects.filter(model3d_owner=self.request.user)

        return user_models


# List every model3D (from every users)
class AllModel3DListAPIView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Model3DListSerializer

    queryset = Model3d.objects.all()


# View specific model3D with id=model_id
class SpecificModel3DListAPIView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Model3DListSerializer
    queryset = Model3d.objects.none()

    lookup_field = 'model_id'

    def get_queryset(self):
        try:
            models = Model3d.objects.filter(pk=self.kwargs[self.lookup_field])

            for model in models:
                model.view_count += 1
                model.save()

                # Signal for Star Badge
                model_viewed.send(sender=None, model=model, model3d_owner=model.model3d_owner)

            return models
        except:
            raise Http404

