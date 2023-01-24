from rest_framework import serializers
from .models import Likes
from django.db import IntegrityError


class LikesSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    The create method handles the unique constraint on 'owner' and 'post'
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Likes
        fields = ['id', 'created_at', 'owner', 'post']
# to avoid duplicate likes
# Django integrityerror exception is thrown when the data's relational integrity is violated. A duplicate key was inserted, for example, or a foreign key restriction might fail.

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})
