
from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^contact/$', views.contact, name='contact'),
    url(r'^register/$', views.register, name='register'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchiveView.as_view(), name='archive'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^comment/(?P<post_pk>[0-9]+)/$', views.comment, name='comment'),
]