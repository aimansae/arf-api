from rest_framework import serializers
from .models import Post
from likes.models import Likes


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.imageurl')
    like_id = serializers.SerializerMethodField()  # to add to fields
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    
    # field name in post model is image
    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger thar 2MB!!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image with larger than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px'
            )

        return value

    def get_like_id(self, obj):
        # to get the current user from context object
        user = self.context['request'].user
        # check if user is authenticated
        if user.is_authenticated:
            like = Likes.objects.filter(
                owner=user, post=obj
            ).first()
            print(like)
            return like.id if like else None
        return None

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'image_filter', 'like_id', 'comments_count', 'likes_count'  # added method here
        ]
