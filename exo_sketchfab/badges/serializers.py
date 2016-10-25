__author__ = 'leomaltrait'

from rest_framework import serializers

from .models import Badges, BadgesExtended


class BadgeListSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.CharField(source='badge.name')

    class Meta:
            model = BadgesExtended
            fields = [
                #'id',
                'name',
            ]
