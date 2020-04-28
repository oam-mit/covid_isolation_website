from rest_framework import serializers
from feeds.models import Feed

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feed
        fields=['name','slug']