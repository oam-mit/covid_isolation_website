from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FeedSerializer
from feeds.models import Feed
# Create your views here.

@api_view(['GET'])
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