from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required
import cv2 as cv


from .Camera import Camera

# Create your views here.

@login_required
def index(request):
    return render(request,'feeds/index.html')

def feed1(request):
    return render(request,'feeds/feed1.html')


def mask_detection(request):
    return StreamingHttpResponse(read_cam(Camera()),content_type="multipart/x-mixed-replace;boundary=frame")


def read_cam(camera):
    while True:
        frame=camera.run_on_video(conf_thresh=0.5,video_path=0)
        yield(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') 
        
