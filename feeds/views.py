from django.shortcuts import render,reverse
from django.http import HttpResponse,StreamingHttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages as mess
from .models import Feed
import cv2 as cv


from .Camera import Camera

# Create your views here.




@login_required
def index(request):
    feeds=Feed.objects.all()
    context={'feeds':feeds}
    return render(request,'feeds/index.html',context=context)

def feed(request,feed_slug):
    context={'feed_name':feed_slug}
    return render(request,'feeds/feed1.html',context=context)


def mask_detection(request,feed_slug):
    feed=Feed.objects.get(slug=feed_slug)
    try:
        location=int(feed.location)
    except:
        location=feed.location
    return StreamingHttpResponse(read_cam(Camera(location)),content_type="multipart/x-mixed-replace;boundary=frame")


def read_cam(camera):
    while True:
        frame=camera.run_on_video(conf_thresh=0.5,video_path=0)
        yield(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') 
        
