from django.conf.urls import patterns, url

from getdbinfo import views

urlpatterns = patterns('',
    # ex: /getdbinfo/
    url(r'^$', views.index, name='index'),
    # ex: /getdbinfo/bill/
    url(r'^(?P<name>[a-zA-z]+)/$', views.query_name, name='query_name'),
)