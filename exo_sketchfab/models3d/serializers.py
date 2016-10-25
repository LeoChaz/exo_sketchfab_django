__author__ = 'leomaltrait'

from rest_framework import serializers

from ..badges.signals import model_created

from .models import Model3d


# Current user create new model3D
class Model3DCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Model3d
        fields = [
            'id',
            'name',
            'description',
        ]

    def create(self, validated_data):
        """
        Create and return a new `Model3D` instance, given the validated data. Current user becomes the owner.
        """

        model3d_owner = self._context['request'].user

        model3d = Model3d.objects.create(model3d_owner=model3d_owner, **validated_data)

        # Signal for Collector Badge
        model_created.send(sender=None, model=model3d, model3d_owner=model3d_owner)

        return model3d


# List 3D models
class Model3DListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
            model = Model3d
            fields = [
                'id',
                'name',
                'model3d_owner',
                'description',
                'date_added',
                'view_count',

            ]