# from django.shortcuts import render
# from rest_framework import status, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Post
# from .serializers import PostSerializer
# from django.http import Http404
# from drf_api.permissions import IsOwnerOrReadOnly
# # Create your views here.


# class PostList(APIView):
#     serializer_class = PostSerializer  # (to get a proper form)
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(
#             posts, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(
#             data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     permission_classes = [IsOwnerOrReadOnly]
#     serializer_class = PostSerializer

#     def get_object(self, pk):
#         try:
#             posts = Post.objects.get(id=pk)
#             self.check_object_permissions(self.request, posts)
#             return posts
#         except Post.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         post= self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# refactoring code
from rest_framework import generics, permissions, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer
from django.db.models import Count  # to count filters
from django_filters.rest_framework import DjangoFilterBackend

class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = Post.objects.all()
    # using annotate to inert filters fields
    # distinct = true to avoid duplicates
    queryset = Post.objects.annotate(
        comments_count=Count('likes', distinct=True),
        likes_count=Count('comment', distinct=True)

    ).order_by('-created_at')
    
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    # add filterset_field to use DjangoFilterBackend
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    #queryset = Post.objects.all()
    queryset = Post.objects.annotate(
        comments_count=Count('likes', distinct=True),
        likes_count=Count('comment', distinct=True)

    ).order_by('-created_at')
    