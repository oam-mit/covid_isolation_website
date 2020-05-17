from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views



from . import views

app_name="api"

urlpatterns=[
    path("feeds",views.get_feeds,name="get_feeds"),
    
    #Authentication
    path("login",views.CustomLogin.as_view(),name="login"),
    path("register",views.userRegistration,name="register"),
]