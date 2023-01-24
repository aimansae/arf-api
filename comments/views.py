# Generic views
# https://www.django-rest-framework.org/api-guide/serializers/#serializers
# https://www.django-rest-framework.org/api-guide/filtering/
from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
# Create your views here.

# get post mehods not needed. Extend generics.ListCreateAPIView
# List takes care og the get method, create of the post method


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    # to associate comment to that specific user, when created
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
# Retrieve Update Destroy API
# https://www.django-rest-framework.org/api-guide/generic-views/#retrieveupdatedestroyapiview


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    # only the owner should be edit or delete
    permission_classes = [IsOwnerOrReadOnly]
    # to avoid sendind post id for editing
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
