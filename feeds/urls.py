from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name='feeds'

urlpatterns=[
    path("",views.index,name="index"),
    path("feed1",views.feed1,name="feed1"),

    #cameras
    path("camera",views.mask_detection,name="mask_detection")
]
