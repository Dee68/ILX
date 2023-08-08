from account.models import Profile
from .serializers import ProfileSerializer
from rest_framework import generics


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'
<<<<<<< HEAD

class ProfileUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'
=======
>>>>>>> 9384d32 (Add profile endpoint to project.)
