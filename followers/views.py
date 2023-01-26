
# Create your views here.
from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Followers
from .serializers import FollowersSerializer

# FollowerList: call upon the subclass to GET and POST


class FollowerList(generics.ListCreateAPIView):
    """
    List all followers, i.e. all instances of a user
    following another user'.
    Create a follower, i.e. follow a user if logged in.
    Perform_create: associate the current logged in user with a follower.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Followers.objects.all()
    serializer_class = FollowersSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# FollowerDetail: call upon the subclass to RETRIEVE and DELETE


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower
    No Update view, as we either follow or unfollow users
    Destroy a follower, i.e. unfollow someone if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Followers.objects.all()
    serializer_class = FollowersSerializer
