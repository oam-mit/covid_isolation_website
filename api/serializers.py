from rest_framework import serializers
from feeds.models import Feed

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feed
        fields=['name','slug']

from django.contrib.auth.models import User
class UserCreationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self):
        user=User(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
        )
        password1=self.validated_data['password']
        password2=self.validated_data['password2']
        if password1!=password2:
            raise serializers.ValidationError({'status':"Error",'errors':{'password':['Passwords did not match']}})
        if len(password1)>=8:
            user.set_password(password1)
            user.save()
            return user
        raise serializers.ValidationError({'status':"Error",'errors':{'password':['Password is too short']}})
