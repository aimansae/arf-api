# import models here
from rest_framework import serializers
from .models import Followers
from django.db import IntegrityError  # to handle duplication errors


class FollowersSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model
    Create method handles the unique constraint on 'owner' and 'followed'
    """

    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Followers
        fields = ['id', 'created_at', 'owner', 'followed_name']

   # to handle duplcation errors
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})
