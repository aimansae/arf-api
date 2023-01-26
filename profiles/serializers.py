from rest_framework import serializers
from .models import Profile
from followers.models import Followers


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(
        source='owner.username')  # to prepopulate
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()  # define lollowing method
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_following_id(self, obj):   
        # to get the current user from context object
        user = self.context['request'].user
        # check if user is authenticated
        if user.is_authenticated:
            # check if user is following any profile
            # filter follower obj

            following = Followers.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            print(following)
            return following.id if following else None
        return None

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
        ]
