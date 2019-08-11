


from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^login', views.mylogin),
    url(r'^reg', views.myregister),
    url(r'^logout', views.mylogout),
    url(r'^test_form', views.test_form),
]

