from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add',views.add_note),
    url(r'^home',views.home),
    url(r'^show',views.show),
]