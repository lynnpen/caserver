from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.fields import CurrentUserDefault
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    #queryset = User.objects.get(username=CurrentUserDefault())
    serializer_class = UserSerializer

    def get(self, request, slug='email'):
        queryset = User.objects.get(username=self.request.user)
        content = {
            'name': queryset.username,
            'username': queryset.username,
            'email': queryset.email
        }
        return Response(content)
