# from django.http import Http404
# from rest_framework import status

# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Profile
# from .serializers import ProfileSerializer
# from drf_api.permissions import IsOwnerOrReadOnly
# # Create your views here.


# class ProfileList(APIView):
#     def get(self, request):
#         profiles = Profile.objects.all()
#         # manu=true cause this is a queryset
#         serializer = ProfileSerializer(profiles, many=True, context={'request':request})
#         return Response(serializer.data)


# class ProfileDetail(APIView):
#     serializer_class = ProfileSerializer  # for a better form
#     permission_classes = [IsOwnerOrReadOnly]  # for permissions

#     def get_object(self, pk):
#         try:
#             profile = Profile.objects.get(pk=pk)
#             self.check_object_permissions(self.request, profile)
#             return profile
#         except Profile.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         # many =true non required as this is 1 object, not a queryset
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(profile,context={'request':request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(profile, data=request.data, context={'request':request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Refactored code:
from rest_framework import generics, filters #for filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer
from django.db.models import Count # to count filters
from django_filters.rest_framework import DjangoFilterBackend
class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    # queryset = Profile.objects.all()
    # annotate instead of .all() to define extra fields to be added to quetyset
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    # create the filters
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend, # added import here
    ]
    filterset_fields = [
        'owner__following__followed__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        ' following_count',
        'owner__following__created_at',
        'owner_followed__created_at',

    ]
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    #queryset = Profile.objects.all()
    # to see the newly created fileds pasted from liestview
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
