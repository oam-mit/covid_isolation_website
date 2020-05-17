from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


app_name='feeds'

urlpatterns=[
    path("",views.index,name="index"),
    path("feed/<slug:feed_slug>",views.feed,name="feed"),

    #cameras
    path("camera/<slug:feed_slug>",views.mask_detection,name="mask_detection"),
]
