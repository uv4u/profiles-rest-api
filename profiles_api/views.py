from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from . import models
from . import permissions

from profiles_api import serializers


class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """list of api features"""
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional django view',
            'Gives you the most control over your application logic',
            'Is Mapped manually to URLs',
        ]

        return Response({'mesasge': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """Creates hello message """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """updating object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """partial update"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """viewsets"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """return a hello msg"""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automaticcally maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        return Response({'msg': 'hello', 'viewset': a_viewset})

    def create(self, request):
        """create a new hello msg"""
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """handle getting an object by its id"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        return Response({'http_method': 'DELETE'})


class UserProfileViewset(viewsets.ModelViewSet):
    """handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
    """handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
