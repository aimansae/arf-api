from django.http import Http404
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly
# Create your views here.


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        # manu=true cause this is a queryset
        serializer = ProfileSerializer(profiles, many=True, context={'request':request})
        return Response(serializer.data)


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer  # for a better form
    permission_classes = [IsOwnerOrReadOnly]  # for permissions

    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # many =true non required as this is 1 object, not a queryset
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile,context={'request':request})
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
