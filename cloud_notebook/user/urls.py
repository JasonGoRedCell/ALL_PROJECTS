from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^login',views.mylogin),
    url(r'^register',views.myregister),
    url(r'^logout',views.mylogout),
]