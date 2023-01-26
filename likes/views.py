from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Likes
from .serializers import LikesSerializer
# Create your views here.
# https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview


class LikeList(generics.ListCreateAPIView):
    # to make sure onlu auth users can like the posts
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikesSerializer
    queryset = Likes.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# to retrieve and delete a like
#https://www.django-rest-framework.org/api-guide/generic-views/#retrievedestroyapiview
class LikeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikesSerializer
    queryset = Likes.objects.all()
    
    
