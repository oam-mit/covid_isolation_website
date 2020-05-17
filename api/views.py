from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import FeedSerializer
from feeds.models import Feed
# Create your views here.

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_feeds(request):
    context={}
    feeds=Feed.objects.all()
    if feeds.count()==0:
        context['status']="not found"
    else:
        context['status']="found"
    feeds=FeedSerializer(feeds,many=True)
    context['feeds']=feeds.data
    return Response(context)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        context={}
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data['user']
            if user.is_staff:
                context['status']="successful"
                token, created = Token.objects.get_or_create(user=user)
                context['status']="successful"
                context['token']=token.key
                context['username']=user.username
                context['email']=user.email
                context['first_name']=user.first_name
                context['last_name']=user.last_name
            else:
                context['status']="unsuccessful"
                context['errors']={"authentication":["Only staff is allowed to login"]}

            
        else:
            context['status']="unsuccessful"
            context['errors']=serializer.errors
        return Response(context)

from .serializers import UserCreationSerializer
@api_view(['POST'])
def userRegistration(request):
    serializer=UserCreationSerializer(data=request.data)
    data={}
    if serializer.is_valid():
        user=serializer.save()
        data['status']="successful"
        data['details']={
            'username':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            'token':user.auth_token.key,
        }

    else:
        data['status']="error"
        data['errors']=serializer.errors
        data['details']=[]

    return Response(data)
